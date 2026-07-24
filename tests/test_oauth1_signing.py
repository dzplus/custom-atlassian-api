import asyncio
import base64
import hashlib
from collections.abc import Iterator
from urllib.parse import unquote

import httpx
import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from atlassian import (
    AtlassianOAuth1Flow,
    AtlassianOAuthError,
    ConfluenceClient,
    OAuth1Config,
)
from atlassian.common.auth.oauth1 import (
    _AtlassianOAuth1Auth,
    _signature_base_string,
)


def make_private_key() -> tuple[rsa.RSAPrivateKey, str]:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    return key, pem


def parse_oauth_header(request: httpx.Request) -> dict[str, str]:
    scheme, value = request.headers["Authorization"].split(" ", 1)
    assert scheme == "OAuth"
    return {
        unquote(name.strip()): unquote(raw_value.strip().strip('"'))
        for item in value.split(",")
        for name, raw_value in [item.split("=", 1)]
    }


def deterministic_auth(
    private_key: str,
    *,
    token: str = "access-token",
) -> _AtlassianOAuth1Auth:
    return _AtlassianOAuth1Auth(
        consumer_key="demo-consumer",
        private_key=private_key,
        token=token,
        nonce_factory=lambda: "fixed-nonce",
        timestamp_factory=lambda: "1700000000",
    )


def test_unicode_query_matches_atlassian_server_oauth_normalization() -> None:
    request = httpx.Request(
        "GET",
        "https://CF.EXAMPLE.TEST:443/rest/api/content/search"
        "?cql=title%3D%22%E4%B8%AD%E6%96%87%22"
        "&label=b&label=a&empty=",
    )
    oauth_parameters = [
        ("oauth_consumer_key", "consumer"),
        ("oauth_nonce", "fixed-nonce"),
        ("oauth_signature_method", "RSA-SHA1"),
        ("oauth_timestamp", "1700000000"),
        ("oauth_token", "token"),
        ("oauth_version", "1.0"),
    ]

    assert _signature_base_string(request, oauth_parameters, b"") == (
        "GET&https%3A%2F%2Fcf.example.test%2Frest%2Fapi%2Fcontent%2Fsearch&"
        "cql%3Dtitle%253D%2522"
        "%25C3%25A4%25C2%25B8%25C2%25AD"
        "%25C3%25A6%25C2%2596%25C2%2587%2522"
        "%26empty%3D%26label%3Da%26label%3Db"
        "%26oauth_consumer_key%3Dconsumer"
        "%26oauth_nonce%3Dfixed-nonce"
        "%26oauth_signature_method%3DRSA-SHA1"
        "%26oauth_timestamp%3D1700000000"
        "%26oauth_token%3Dtoken"
        "%26oauth_version%3D1.0"
    )


def test_json_body_is_preserved_and_signed_with_oauth_body_hash() -> None:
    private_key, private_key_pem = make_private_key()
    request = httpx.Request(
        "POST",
        "https://cf.example.test/rest/api/content",
        json={"title": "中文页面", "type": "page"},
    )
    original_body = request.content
    original_content_length = request.headers["Content-Length"]

    signed_request = next(deterministic_auth(private_key_pem).auth_flow(request))
    oauth_parameters = parse_oauth_header(signed_request)

    assert signed_request.content == original_body
    assert signed_request.headers["Content-Length"] == original_content_length
    assert (
        oauth_parameters["oauth_body_hash"]
        == base64.b64encode(hashlib.sha1(original_body).digest()).decode()
    )

    signature = base64.b64decode(oauth_parameters.pop("oauth_signature"))
    base_string = _signature_base_string(
        signed_request,
        list(oauth_parameters.items()),
        signed_request.content,
    )
    private_key.public_key().verify(
        signature,
        base_string.encode("ascii"),
        padding.PKCS1v15(),
        hashes.SHA1(),
    )


def test_form_body_parameters_are_signed_without_oauth_body_hash() -> None:
    private_key, private_key_pem = make_private_key()
    request = httpx.Request(
        "POST",
        "https://jira.example.test/plugins/servlet/oauth/access-token?scope=a",
        headers={"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"},
        content="name=%E4%B8%AD%E6%96%87&item=b&item=a",
    )

    signed_request = next(deterministic_auth(private_key_pem).auth_flow(request))
    oauth_parameters = parse_oauth_header(signed_request)

    assert "oauth_body_hash" not in oauth_parameters
    signature = base64.b64decode(oauth_parameters.pop("oauth_signature"))
    base_string = _signature_base_string(
        signed_request,
        list(oauth_parameters.items()),
        signed_request.content,
    )
    assert "name%3D%25E4%25B8%25AD%25E6%2596%2587" in base_string
    assert "item%3Da%26item%3Db" in base_string
    private_key.public_key().verify(
        signature,
        base_string.encode("ascii"),
        padding.PKCS1v15(),
        hashes.SHA1(),
    )


def test_streaming_upload_is_not_consumed_by_signer() -> None:
    _, private_key_pem = make_private_key()

    def chunks() -> Iterator[bytes]:
        yield b"first"
        yield b"-second"

    request = httpx.Request(
        "POST",
        "https://cf.example.test/rest/api/content/1/child/attachment",
        headers={"Content-Type": "multipart/form-data; boundary=demo"},
        content=chunks(),
    )

    signed_request = next(deterministic_auth(private_key_pem).auth_flow(request))
    oauth_parameters = parse_oauth_header(signed_request)

    assert "oauth_body_hash" not in oauth_parameters
    assert signed_request.read() == b"first-second"


def test_signature_cannot_be_verified_with_an_unrelated_key() -> None:
    _, private_key_pem = make_private_key()
    unrelated_key, _ = make_private_key()
    request = httpx.Request("GET", "https://cf.example.test/rest/api/user/current")

    signed_request = next(deterministic_auth(private_key_pem).auth_flow(request))
    oauth_parameters = parse_oauth_header(signed_request)
    signature = base64.b64decode(oauth_parameters.pop("oauth_signature"))
    base_string = _signature_base_string(
        signed_request,
        list(oauth_parameters.items()),
        signed_request.content,
    )

    with pytest.raises(InvalidSignature):
        unrelated_key.public_key().verify(
            signature,
            base_string.encode("ascii"),
            padding.PKCS1v15(),
            hashes.SHA1(),
        )


def test_oauth_config_rejects_an_invalid_rsa_private_key_when_used() -> None:
    oauth1 = OAuth1Config(
        consumer_key="demo-consumer",
        private_key="-----BEGIN PRIVATE KEY-----\ninvalid\n-----END PRIVATE KEY-----",
        access_token="access-token",
    )

    with pytest.raises(AtlassianOAuthError, match="Invalid OAuth RSA private key"):
        oauth1.create_httpx_auth()


def test_token_flow_reports_atlassian_oauth_problem() -> None:
    _, private_key_pem = make_private_key()

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            401,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            text="oauth_problem=consumer_key_unknown",
        )

    flow = AtlassianOAuth1Flow(
        base_url="https://cf.example.test",
        consumer_key="unknown-consumer",
        private_key=private_key_pem,
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(
        AtlassianOAuthError,
        match="Atlassian OAuth error: consumer_key_unknown",
    ):
        asyncio.run(flow.fetch_request_token())


def test_existing_client_calls_support_unicode_query_and_json_body() -> None:
    private_key, private_key_pem = make_private_key()
    oauth1 = OAuth1Config(
        consumer_key="demo-consumer",
        private_key=private_key_pem,
        access_token="access-token",
    )
    seen_methods: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_methods.append(request.method)
        oauth_parameters = parse_oauth_header(request)
        signature = base64.b64decode(oauth_parameters.pop("oauth_signature"))
        base_string = _signature_base_string(
            request,
            list(oauth_parameters.items()),
            request.content,
        )
        private_key.public_key().verify(
            signature,
            base_string.encode("ascii"),
            padding.PKCS1v15(),
            hashes.SHA1(),
        )

        if request.method == "GET":
            assert request.url.params["cql"] == 'title="中文"'
            assert "oauth_body_hash" not in oauth_parameters
            return httpx.Response(200, json={"results": []})

        assert request.content == '{"title":"中文页面","type":"page"}'.encode()
        assert (
            oauth_parameters["oauth_body_hash"]
            == base64.b64encode(hashlib.sha1(request.content).digest()).decode()
        )
        return httpx.Response(200, json={"id": "123"})

    async def make_requests() -> tuple[dict, dict]:
        client = ConfluenceClient(
            base_url="https://cf.example.test",
            auth_mode="oauth1",
            oauth1=oauth1,
            trust_env=False,
        )
        client._client = httpx.AsyncClient(
            base_url=client.base_url,
            auth=oauth1.create_httpx_auth(),
            transport=httpx.MockTransport(handler),
        )
        try:
            search_result = await client.get_json(
                "/rest/api/search",
                params={"cql": 'title="中文"'},
            )
            create_result = await client.post_json(
                "/rest/api/content",
                data={"title": "中文页面", "type": "page"},
            )
            return search_result, create_result
        finally:
            await client._client.aclose()

    assert asyncio.run(make_requests()) == ({"results": []}, {"id": "123"})
    assert seen_methods == ["GET", "POST"]
