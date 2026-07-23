import asyncio
import os
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import httpx
import pytest

from atlassian import (
    AtlassianOAuth1Flow,
    ConfluenceClient,
    JiraClient,
    OAuth1Config,
    OAuth1Token,
)
from atlassian.tempo import TempoClient
from examples.confluence_oauth1_demo import (
    DemoSettings,
    load_token,
    save_token,
)


def make_private_key() -> str:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()


def test_flow_builds_atlassian_oauth_endpoints() -> None:
    flow = AtlassianOAuth1Flow(
        base_url="https://cf.example.test/",
        consumer_key="demo-consumer",
        private_key=make_private_key(),
    )

    assert flow.base_url == "https://cf.example.test"
    assert flow.request_token_url.endswith("/plugins/servlet/oauth/request-token")
    assert flow.authorization_url.endswith("/plugins/servlet/oauth/authorize")
    assert flow.access_token_url.endswith("/plugins/servlet/oauth/access-token")


def test_oauth_config_signs_request_with_rsa_sha1() -> None:
    oauth1 = OAuth1Config(
        consumer_key="demo-consumer",
        private_key=make_private_key(),
        access_token="access-token",
        access_token_secret="token-secret",
    )
    request = httpx.Request(
        "GET",
        "https://cf.example.test/rest/api/content?limit=1",
    )

    signed_request = next(oauth1.create_httpx_auth().auth_flow(request))
    authorization = signed_request.headers["Authorization"]

    assert authorization.startswith("OAuth ")
    assert 'oauth_signature_method="RSA-SHA1"' in authorization
    assert 'oauth_consumer_key="demo-consumer"' in authorization
    assert 'oauth_token="access-token"' in authorization
    assert "oauth_signature=" in authorization
    assert "token-secret" not in authorization


@pytest.mark.parametrize(
    "client_type",
    [ConfluenceClient, JiraClient, TempoClient],
)
def test_product_clients_accept_oauth_without_username_or_password(
    client_type: type,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for prefix in ("ATLASSIAN", "CONFLUENCE", "JIRA", "TEMPO"):
        monkeypatch.delenv(f"{prefix}_USERNAME", raising=False)
        monkeypatch.delenv(f"{prefix}_PASSWORD", raising=False)

    oauth1 = OAuth1Config(
        consumer_key="demo-consumer",
        private_key=make_private_key(),
        access_token="access-token",
    )

    client = client_type(
        base_url="https://cf.example.test",
        auth_mode="oauth1",
        oauth1=oauth1,
        trust_env=False,
    )

    assert client.is_logged_in
    assert client._username is None
    assert client._password is None


def test_confluence_client_requires_oauth_config() -> None:
    with pytest.raises(ValueError, match="oauth1 configuration is required"):
        ConfluenceClient(
            base_url="https://cf.example.test",
            auth_mode="oauth1",
        )


def test_confluence_client_signs_resource_requests() -> None:
    private_key = make_private_key()
    oauth1 = OAuth1Config(
        consumer_key="demo-consumer",
        private_key=private_key,
        access_token="access-token",
    )

    def handler(request: httpx.Request) -> httpx.Response:
        authorization = request.headers["Authorization"]
        assert request.url.path == "/rest/api/content"
        assert 'oauth_signature_method="RSA-SHA1"' in authorization
        assert 'oauth_consumer_key="demo-consumer"' in authorization
        assert 'oauth_token="access-token"' in authorization
        return httpx.Response(200, json={"results": []})

    async def request() -> dict:
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
            return await client.get_json("/rest/api/content")
        finally:
            await client._client.aclose()

    assert asyncio.run(request()) == {"results": []}


def test_three_legged_oauth_token_exchange() -> None:
    seen_paths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_paths.append(request.url.path)
        authorization = request.headers["Authorization"]
        assert request.method == "POST"
        assert 'oauth_signature_method="RSA-SHA1"' in authorization

        if request.url.path.endswith("/request-token"):
            assert 'oauth_callback="oob"' in authorization
            body = (
                "oauth_token=request-token"
                "&oauth_token_secret=request-secret"
                "&oauth_callback_confirmed=true"
            )
        else:
            assert 'oauth_verifier="verification-code"' in authorization
            body = "oauth_token=access-token&oauth_token_secret=access-secret"
        return httpx.Response(
            200,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            text=body,
        )

    flow = AtlassianOAuth1Flow(
        base_url="https://cf.example.test",
        consumer_key="demo-consumer",
        private_key=make_private_key(),
        transport=httpx.MockTransport(handler),
    )

    async def exchange() -> OAuth1Token:
        request_token = await flow.fetch_request_token()
        assert request_token.oauth_token == "request-token"
        authorization_url = flow.build_authorization_url(request_token)
        assert "oauth_token=request-token" in authorization_url
        return await flow.exchange_access_token(
            request_token=request_token,
            verifier="verification-code",
        )

    access_token = asyncio.run(exchange())

    assert access_token == OAuth1Token(
        oauth_token="access-token",
        oauth_token_secret="access-secret",
    )
    assert seen_paths == [
        "/plugins/servlet/oauth/request-token",
        "/plugins/servlet/oauth/access-token",
    ]


def test_demo_token_file_is_private_and_round_trips(tmp_path: Path) -> None:
    settings = DemoSettings(
        base_url="https://cf.example.test",
        consumer_key="demo-consumer",
        private_key=make_private_key(),
    )
    token = OAuth1Token(
        oauth_token="access-token",
        oauth_token_secret="token-secret",
    )
    token_file = tmp_path / "oauth-token.json"

    save_token(token_file, settings, token)

    assert load_token(token_file) == token
    assert os.stat(token_file).st_mode & 0o777 == 0o600
