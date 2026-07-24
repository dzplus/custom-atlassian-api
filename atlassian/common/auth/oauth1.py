"""OAuth 1.0a support for Atlassian Server and Data Center products."""

from __future__ import annotations

import base64
import hashlib
import secrets
import time
from collections.abc import Callable, Generator, Mapping
from dataclasses import dataclass
from typing import Any
from urllib.parse import parse_qsl, quote, urlencode

import httpx
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from atlassian.common.exceptions import AtlassianOAuthError

_FORM_CONTENT_TYPE = "application/x-www-form-urlencoded"
_OAUTH_SIGNATURE_METHOD = "RSA-SHA1"
_OAUTH_VERSION = "1.0"


def _percent_encode(value: str) -> str:
    """Encode an OAuth parameter according to RFC 5849 section 3.6."""

    return quote(value, safe="~-._", encoding="utf-8", errors="strict")


def _parse_parameters(
    value: bytes,
    *,
    encoding: str,
) -> list[tuple[str, str]]:
    """Decode a query or form body into OAuth parameter pairs."""

    if not value:
        return []
    return parse_qsl(
        value.decode("utf-8"),
        keep_blank_values=True,
        encoding=encoding,
        errors="strict",
    )


def _content_type(request: httpx.Request) -> str:
    return request.headers.get("Content-Type", "").partition(";")[0].strip().lower()


def _normalized_base_url(url: httpx.URL) -> str:
    """Build the signature base string URI from the exact outgoing URL."""

    scheme = url.scheme.lower()
    host = url.raw_host.decode("ascii").lower()
    if ":" in host and not host.startswith("["):
        host = f"[{host}]"

    port = url.port
    default_port = (scheme == "http" and port == 80) or (
        scheme == "https" and port == 443
    )
    authority = host if port is None or default_port else f"{host}:{port}"

    raw_path = url.raw_path.split(b"?", 1)[0] or b"/"
    path = raw_path.decode("ascii")
    return f"{scheme}://{authority}{path}"


def _normalize_parameters(parameters: list[tuple[str, str]]) -> str:
    """Percent-encode and sort OAuth parameters without losing duplicates."""

    encoded = [
        (_percent_encode(name), _percent_encode(value))
        for name, value in parameters
        if name != "oauth_signature"
    ]
    encoded.sort()
    return "&".join(f"{name}={value}" for name, value in encoded)


def _signature_base_string(
    request: httpx.Request,
    oauth_parameters: list[tuple[str, str]],
    body: bytes | None,
) -> str:
    """Create the RFC 5849 signature base string for an HTTPX request."""

    # Atlassian Server/Data Center's OAuth provider decodes percent-escaped
    # query octets as ISO-8859-1 before normalizing the signature parameters.
    # The REST layer still receives the original UTF-8 URL. Mirroring that
    # OAuth-only behavior avoids signature_invalid for non-ASCII CQL/JQL.
    parameters = _parse_parameters(request.url.query, encoding="latin-1")
    parameters.extend(oauth_parameters)

    if body is not None and _content_type(request) == _FORM_CONTENT_TYPE:
        parameters.extend(_parse_parameters(body, encoding="utf-8"))

    normalized_parameters = _normalize_parameters(parameters)
    return "&".join(
        (
            _percent_encode(request.method.upper()),
            _percent_encode(_normalized_base_url(request.url)),
            _percent_encode(normalized_parameters),
        )
    )


def _buffered_request_body(request: httpx.Request) -> bytes | None:
    """Return an already-buffered body without consuming a streaming upload."""

    try:
        return request.content
    except httpx.RequestNotRead:
        return None


def _load_rsa_private_key(private_key: str) -> rsa.RSAPrivateKey:
    try:
        loaded_key = serialization.load_pem_private_key(
            private_key.encode("utf-8"),
            password=None,
        )
    except (TypeError, ValueError) as exc:
        raise AtlassianOAuthError(f"Invalid OAuth RSA private key: {exc}") from exc

    if not isinstance(loaded_key, rsa.RSAPrivateKey):
        raise AtlassianOAuthError("OAuth private key must be an RSA private key")
    return loaded_key


class _AtlassianOAuth1Auth(httpx.Auth):
    """HTTPX auth implementation for Atlassian's RSA-SHA1 OAuth provider."""

    def __init__(
        self,
        *,
        consumer_key: str,
        private_key: str,
        token: str | None = None,
        oauth_parameters: Mapping[str, str] | None = None,
        nonce_factory: Callable[[], str] | None = None,
        timestamp_factory: Callable[[], str] | None = None,
    ) -> None:
        self._consumer_key = consumer_key
        self._private_key = _load_rsa_private_key(private_key)
        self._token = token
        self._extra_oauth_parameters = dict(oauth_parameters or {})
        self._nonce_factory = nonce_factory or (lambda: secrets.token_urlsafe(24))
        self._timestamp_factory = timestamp_factory or (lambda: str(int(time.time())))

    def _oauth_parameters(
        self,
        request: httpx.Request,
        body: bytes | None,
    ) -> list[tuple[str, str]]:
        parameters = [
            ("oauth_consumer_key", self._consumer_key),
            ("oauth_nonce", self._nonce_factory()),
            ("oauth_signature_method", _OAUTH_SIGNATURE_METHOD),
            ("oauth_timestamp", self._timestamp_factory()),
            ("oauth_version", _OAUTH_VERSION),
        ]
        if self._token:
            parameters.append(("oauth_token", self._token))
        parameters.extend(self._extra_oauth_parameters.items())

        if body and _content_type(request) != _FORM_CONTENT_TYPE:
            digest = hashlib.sha1(body).digest()
            parameters.append(
                ("oauth_body_hash", base64.b64encode(digest).decode("ascii"))
            )
        return parameters

    def auth_flow(
        self,
        request: httpx.Request,
    ) -> Generator[httpx.Request, httpx.Response, None]:
        body = _buffered_request_body(request)
        oauth_parameters = self._oauth_parameters(request, body)

        base_string = _signature_base_string(request, oauth_parameters, body)
        signature = self._private_key.sign(
            base_string.encode("ascii"),
            padding.PKCS1v15(),
            hashes.SHA1(),
        )
        oauth_parameters.append(
            ("oauth_signature", base64.b64encode(signature).decode("ascii"))
        )

        request.headers["Authorization"] = "OAuth " + ", ".join(
            f'{_percent_encode(name)}="{_percent_encode(value)}"'
            for name, value in oauth_parameters
        )
        yield request


@dataclass(frozen=True)
class OAuth1Token:
    """OAuth request or access token returned by an Atlassian product."""

    oauth_token: str
    oauth_token_secret: str = ""

    def __post_init__(self) -> None:
        if not self.oauth_token:
            raise ValueError("oauth_token is required")

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> OAuth1Token:
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
    ) -> OAuth1Config:
        """Create request credentials from an exchanged access token."""

        return cls(
            consumer_key=consumer_key,
            private_key=private_key,
            access_token=token.oauth_token,
            access_token_secret=token.oauth_token_secret,
        )

    def create_httpx_auth(self) -> httpx.Auth:
        """Create an HTTPX auth object that signs every outgoing request."""

        return _AtlassianOAuth1Auth(
            consumer_key=self.consumer_key,
            private_key=self.private_key,
            token=self.access_token,
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

    def _create_auth(
        self,
        *,
        token: OAuth1Token | None = None,
        verifier: str | None = None,
    ) -> httpx.Auth:
        oauth_parameters = (
            {"oauth_verifier": verifier}
            if verifier is not None
            else {"oauth_callback": self.callback_uri}
        )
        return _AtlassianOAuth1Auth(
            consumer_key=self.consumer_key,
            private_key=self.private_key,
            token=token.oauth_token if token else None,
            oauth_parameters=oauth_parameters,
        )

    async def _fetch_token(
        self,
        url: str,
        *,
        token: OAuth1Token | None = None,
        verifier: str | None = None,
    ) -> OAuth1Token:
        auth = self._create_auth(token=token, verifier=verifier)
        async with httpx.AsyncClient(
            auth=auth,
            timeout=self.timeout,
            follow_redirects=True,
            trust_env=self.trust_env,
            transport=self.transport,
        ) as client:
            response = await client.post(url)

        data = dict(
            parse_qsl(
                response.text,
                keep_blank_values=True,
                encoding="utf-8",
                errors="strict",
            )
        )
        if oauth_problem := data.get("oauth_problem"):
            raise AtlassianOAuthError(f"Atlassian OAuth error: {oauth_problem}")
        response.raise_for_status()
        return OAuth1Token.from_mapping(data)

    async def fetch_request_token(self) -> OAuth1Token:
        """Obtain a short-lived request token from Atlassian."""

        try:
            return await self._fetch_token(self.request_token_url)
        except AtlassianOAuthError:
            raise
        except (httpx.HTTPError, UnicodeError, ValueError) as exc:
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
        try:
            return await self._fetch_token(
                self.access_token_url,
                token=request_token,
                verifier=verifier,
            )
        except AtlassianOAuthError:
            raise
        except (httpx.HTTPError, UnicodeError, ValueError) as exc:
            raise AtlassianOAuthError(
                f"Failed to exchange OAuth access token: {exc}"
            ) from exc
