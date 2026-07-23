"""OAuth 1.0a support for Atlassian Server and Data Center products."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import httpx

from atlassian.common.exceptions import AtlassianOAuthError


def _load_authlib() -> tuple[type[Any], type[Any], type[Exception]]:
    """Load the optional OAuth dependency only when the feature is used."""

    try:
        from authlib.integrations.base_client.errors import OAuthError
        from authlib.integrations.httpx_client import AsyncOAuth1Client, OAuth1Auth
    except ImportError as exc:
        raise AtlassianOAuthError(
            "OAuth 1.0a support requires the optional dependency. "
            'Install it with: pip install "custom-atlassian-api[oauth]"'
        ) from exc
    return AsyncOAuth1Client, OAuth1Auth, OAuthError


@dataclass(frozen=True)
class OAuth1Token:
    """OAuth request or access token returned by an Atlassian product."""

    oauth_token: str
    oauth_token_secret: str = ""

    def __post_init__(self) -> None:
        if not self.oauth_token:
            raise ValueError("oauth_token is required")

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "OAuth1Token":
        """Build a token from an OAuth form response."""

        return cls(
            oauth_token=str(data.get("oauth_token", "")),
            oauth_token_secret=str(data.get("oauth_token_secret", "")),
        )

    def as_dict(self) -> dict[str, str]:
        """Return the serializable token fields."""

        return {
            "oauth_token": self.oauth_token,
            "oauth_token_secret": self.oauth_token_secret,
        }


@dataclass(frozen=True)
class OAuth1Config:
    """Credentials used to sign Atlassian REST requests with RSA-SHA1."""

    consumer_key: str
    private_key: str
    access_token: str
    access_token_secret: str = ""

    def __post_init__(self) -> None:
        if not self.consumer_key:
            raise ValueError("consumer_key is required")
        if "PRIVATE KEY" not in self.private_key:
            raise ValueError("private_key must contain a PEM private key")
        if not self.access_token:
            raise ValueError("access_token is required")

    @classmethod
    def from_access_token(
        cls,
        *,
        consumer_key: str,
        private_key: str,
        token: OAuth1Token,
    ) -> "OAuth1Config":
        """Create request credentials from an exchanged access token."""

        return cls(
            consumer_key=consumer_key,
            private_key=private_key,
            access_token=token.oauth_token,
            access_token_secret=token.oauth_token_secret,
        )

    def create_httpx_auth(self) -> Any:
        """Create an HTTPX auth object that signs every outgoing request."""

        _, oauth1_auth, _ = _load_authlib()
        return oauth1_auth(
            client_id=self.consumer_key,
            token=self.access_token,
            token_secret=self.access_token_secret,
            rsa_key=self.private_key,
            signature_method="RSA-SHA1",
            signature_type="HEADER",
        )


class AtlassianOAuth1Flow:
    """Perform Atlassian's three-legged OAuth 1.0a authorization flow."""

    REQUEST_TOKEN_PATH = "/plugins/servlet/oauth/request-token"
    AUTHORIZE_PATH = "/plugins/servlet/oauth/authorize"
    ACCESS_TOKEN_PATH = "/plugins/servlet/oauth/access-token"

    def __init__(
        self,
        *,
        base_url: str,
        consumer_key: str,
        private_key: str,
        callback_uri: str = "oob",
        timeout: float = 30.0,
        trust_env: bool = True,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        normalized_url = base_url.rstrip("/")
        if not normalized_url.startswith(("http://", "https://")):
            raise ValueError("base_url must start with http:// or https://")
        if not consumer_key:
            raise ValueError("consumer_key is required")
        if "PRIVATE KEY" not in private_key:
            raise ValueError("private_key must contain a PEM private key")
        if not callback_uri:
            raise ValueError("callback_uri is required")

        self.base_url = normalized_url
        self.consumer_key = consumer_key
        self.private_key = private_key
        self.callback_uri = callback_uri
        self.timeout = timeout
        self.trust_env = trust_env
        self.transport = transport

    @property
    def request_token_url(self) -> str:
        return f"{self.base_url}{self.REQUEST_TOKEN_PATH}"

    @property
    def authorization_url(self) -> str:
        return f"{self.base_url}{self.AUTHORIZE_PATH}"

    @property
    def access_token_url(self) -> str:
        return f"{self.base_url}{self.ACCESS_TOKEN_PATH}"

    def _create_client(
        self,
        *,
        token: OAuth1Token | None = None,
        verifier: str | None = None,
    ) -> Any:
        async_oauth1_client, _, _ = _load_authlib()
        return async_oauth1_client(
            client_id=self.consumer_key,
            token=token.oauth_token if token else None,
            token_secret=token.oauth_token_secret if token else None,
            redirect_uri=self.callback_uri,
            verifier=verifier,
            rsa_key=self.private_key,
            signature_method="RSA-SHA1",
            signature_type="HEADER",
            timeout=self.timeout,
            follow_redirects=True,
            trust_env=self.trust_env,
            transport=self.transport,
        )

    async def fetch_request_token(self) -> OAuth1Token:
        """Obtain a short-lived request token from Atlassian."""

        _, _, oauth_error = _load_authlib()
        try:
            async with self._create_client() as client:
                data = await client.fetch_request_token(self.request_token_url)
            return OAuth1Token.from_mapping(data)
        except (httpx.HTTPError, oauth_error, ValueError) as exc:
            raise AtlassianOAuthError(
                f"Failed to fetch OAuth request token: {exc}"
            ) from exc

    def build_authorization_url(self, request_token: OAuth1Token) -> str:
        """Build the URL a user must open to authorize a request token."""

        query = urlencode({"oauth_token": request_token.oauth_token})
        return f"{self.authorization_url}?{query}"

    async def exchange_access_token(
        self,
        *,
        request_token: OAuth1Token,
        verifier: str,
    ) -> OAuth1Token:
        """Exchange an authorized request token and verifier for an access token."""

        if not verifier:
            raise ValueError("verifier is required")
        _, _, oauth_error = _load_authlib()
        try:
            async with self._create_client(
                token=request_token,
                verifier=verifier,
            ) as client:
                data = await client.fetch_access_token(
                    self.access_token_url,
                    verifier=verifier,
                )
            return OAuth1Token.from_mapping(data)
        except (httpx.HTTPError, oauth_error, ValueError) as exc:
            raise AtlassianOAuthError(
                f"Failed to exchange OAuth access token: {exc}"
            ) from exc
