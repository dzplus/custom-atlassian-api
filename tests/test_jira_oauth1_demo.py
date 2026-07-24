import asyncio
from pathlib import Path

import httpx
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from atlassian import JiraClient, OAuth1Config, OAuth1Token
from examples.confluence_oauth1_demo import (
    DEFAULT_TOKEN_FILE as CONFLUENCE_TOKEN_FILE,
)
from examples.jira_oauth1_demo import (
    DEFAULT_API_PATH,
    DEFAULT_TOKEN_FILE,
    PRODUCT,
    build_parser,
)
from examples.oauth1_demo_common import DemoSettings, load_token, save_token


def make_private_key() -> str:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()


def test_jira_demo_has_product_specific_defaults() -> None:
    assert PRODUCT.name == "Jira"
    assert PRODUCT.env_prefix == "JIRA"
    assert DEFAULT_API_PATH == "/rest/api/2/myself"
    assert DEFAULT_TOKEN_FILE.name == "jira-oauth1.json"
    assert DEFAULT_TOKEN_FILE != CONFLUENCE_TOKEN_FILE


def test_jira_parser_reads_jira_environment(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    private_key_file = tmp_path / "jira-private.pem"
    private_key_file.write_text(make_private_key(), encoding="utf-8")
    monkeypatch.setenv("JIRA_URL", "https://jira.example.test")
    monkeypatch.setenv("JIRA_OAUTH_CONSUMER_KEY", "jira-consumer")
    monkeypatch.setenv(
        "JIRA_OAUTH_PRIVATE_KEY_FILE",
        str(private_key_file),
    )

    args = build_parser().parse_args(["request"])

    assert args.base_url == "https://jira.example.test"
    assert args.consumer_key == "jira-consumer"
    assert args.private_key_file == private_key_file
    assert args.token_file == DEFAULT_TOKEN_FILE
    assert args.api_path == "/rest/api/2/myself"


def test_token_file_rejects_a_different_product(tmp_path: Path) -> None:
    confluence_settings = DemoSettings(
        base_url="https://confluence.example.test",
        consumer_key="shared-client",
        private_key=make_private_key(),
    )
    jira_settings = DemoSettings(
        base_url="https://jira.example.test",
        consumer_key="shared-client",
        private_key=confluence_settings.private_key,
    )
    token_file = tmp_path / "oauth1.json"
    save_token(
        token_file,
        confluence_settings,
        OAuth1Token(
            oauth_token="confluence-token",
            oauth_token_secret="confluence-secret",
        ),
    )

    with pytest.raises(ValueError, match="token file belongs to"):
        load_token(token_file, jira_settings)


def test_token_file_rejects_a_different_consumer(tmp_path: Path) -> None:
    original_settings = DemoSettings(
        base_url="https://jira.example.test",
        consumer_key="first-client",
        private_key=make_private_key(),
    )
    other_settings = DemoSettings(
        base_url=original_settings.base_url,
        consumer_key="second-client",
        private_key=original_settings.private_key,
    )
    token_file = tmp_path / "jira-oauth1.json"
    save_token(
        token_file,
        original_settings,
        OAuth1Token(
            oauth_token="jira-token",
            oauth_token_secret="jira-secret",
        ),
    )

    with pytest.raises(ValueError, match="belongs to consumer first-client"):
        load_token(token_file, other_settings)


def test_token_file_refuses_to_overwrite_a_different_product(
    tmp_path: Path,
) -> None:
    confluence_settings = DemoSettings(
        base_url="https://confluence.example.test",
        consumer_key="shared-client",
        private_key=make_private_key(),
    )
    jira_settings = DemoSettings(
        base_url="https://jira.example.test",
        consumer_key="shared-client",
        private_key=confluence_settings.private_key,
    )
    token_file = tmp_path / "shared-oauth1.json"
    confluence_token = OAuth1Token(
        oauth_token="confluence-token",
        oauth_token_secret="confluence-secret",
    )
    save_token(token_file, confluence_settings, confluence_token)

    with pytest.raises(ValueError, match="Refusing to overwrite"):
        save_token(
            token_file,
            jira_settings,
            OAuth1Token(
                oauth_token="jira-token",
                oauth_token_secret="jira-secret",
            ),
        )

    assert load_token(token_file, confluence_settings) == confluence_token


def test_jira_client_signs_resource_requests() -> None:
    oauth1 = OAuth1Config(
        consumer_key="jira-consumer",
        private_key=make_private_key(),
        access_token="jira-access-token",
    )

    def handler(request: httpx.Request) -> httpx.Response:
        authorization = request.headers["Authorization"]
        assert request.url.path == "/rest/api/2/myself"
        assert 'oauth_signature_method="RSA-SHA1"' in authorization
        assert 'oauth_consumer_key="jira-consumer"' in authorization
        assert 'oauth_token="jira-access-token"' in authorization
        return httpx.Response(200, json={"name": "demo-user"})

    async def request() -> dict:
        client = JiraClient(
            base_url="https://jira.example.test",
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
            return await client.get_json("/rest/api/2/myself")
        finally:
            await client._client.aclose()

    assert asyncio.run(request()) == {"name": "demo-user"}
