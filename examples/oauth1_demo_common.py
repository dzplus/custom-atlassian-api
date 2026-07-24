"""Shared helpers for the Jira and Confluence OAuth 1.0a demos."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import webbrowser
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from atlassian import AtlassianOAuth1Flow, OAuth1Config, OAuth1Token
from atlassian.common.exceptions import AtlassianError


@dataclass(frozen=True)
class DemoSettings:
    base_url: str
    consumer_key: str
    private_key: str
    timeout: float = 30.0
    trust_env: bool = False


@dataclass(frozen=True)
class DemoProduct:
    name: str
    env_prefix: str
    client_type: type[Any]
    default_token_file: Path
    default_api_path: str


def load_private_key(path: Path) -> str:
    """Read an RSA private key without printing it."""

    try:
        private_key = path.expanduser().read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"Unable to read private key file: {path}") from exc
    if "PRIVATE KEY" not in private_key:
        raise ValueError(f"Not a PEM private key: {path}")
    return private_key


def _read_token_payload(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to read token file: {path}") from exc
    if not isinstance(data, dict):
        raise TypeError(f"Token file must contain a JSON object: {path}")
    return data


def _validate_token_owner(
    data: dict[str, Any],
    settings: DemoSettings,
    *,
    action: str,
) -> None:
    expected_url = settings.base_url.rstrip("/")
    stored_url = str(data.get("base_url", "")).rstrip("/")
    if stored_url != expected_url:
        raise ValueError(
            f"{action}: token file belongs to "
            f"{stored_url or 'an unknown provider'}, not {expected_url}"
        )
    stored_consumer = data.get("consumer_key")
    if stored_consumer != settings.consumer_key:
        raise ValueError(
            f"{action}: token file belongs to consumer "
            f"{stored_consumer or 'unknown'}, not {settings.consumer_key}"
        )


def save_token(path: Path, settings: DemoSettings, token: OAuth1Token) -> None:
    """Persist an access token and its provider identity to a private JSON file."""

    token_path = path.expanduser()
    token_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if token_path.exists():
        _validate_token_owner(
            _read_token_payload(token_path),
            settings,
            action="Refusing to overwrite",
        )
    payload = {
        "base_url": settings.base_url.rstrip("/"),
        "consumer_key": settings.consumer_key,
        **token.as_dict(),
    }
    fd = os.open(token_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    token_path.chmod(0o600)


def load_token(
    path: Path,
    settings: DemoSettings | None = None,
) -> OAuth1Token:
    """Load a token and optionally verify that it belongs to this provider."""

    token_path = path.expanduser()
    data = _read_token_payload(token_path)

    if settings is not None:
        _validate_token_owner(data, settings, action="Cannot use token")

    return OAuth1Token.from_mapping(data)


def create_flow(settings: DemoSettings) -> AtlassianOAuth1Flow:
    return AtlassianOAuth1Flow(
        base_url=settings.base_url,
        consumer_key=settings.consumer_key,
        private_key=settings.private_key,
        callback_uri="oob",
        timeout=settings.timeout,
        trust_env=settings.trust_env,
    )


async def request_json(
    product: DemoProduct,
    settings: DemoSettings,
    token: OAuth1Token,
    api_path: str,
) -> Any:
    """Call a product endpoint through the SDK's OAuth-enabled client."""

    oauth1 = OAuth1Config.from_access_token(
        consumer_key=settings.consumer_key,
        private_key=settings.private_key,
        token=token,
    )
    async with product.client_type(
        base_url=settings.base_url,
        auth_mode="oauth1",
        oauth1=oauth1,
        timeout=settings.timeout,
        trust_env=settings.trust_env,
    ) as client:
        return await client.get_json(api_path)


async def authorize(
    product: DemoProduct,
    settings: DemoSettings,
    *,
    token_file: Path,
    api_path: str,
    open_browser: bool,
) -> Any:
    """Run request-token, user authorization, and access-token exchange."""

    flow = create_flow(settings)
    request_token = await flow.fetch_request_token()
    authorization_url = flow.build_authorization_url(request_token)

    print(f"\nAuthorize this application in {product.name}:")
    print(authorization_url)
    if open_browser:
        opened = webbrowser.open(authorization_url)
        if not opened:
            print("The browser did not open automatically; use the URL above.")

    verifier = input(f"\nPaste the verification code shown by {product.name}: ").strip()
    access_token = await flow.exchange_access_token(
        request_token=request_token,
        verifier=verifier,
    )

    save_token(token_file, settings, access_token)
    print(f"Access token saved with mode 0600: {token_file.expanduser()}")
    print(
        "Access token: "
        f"{access_token.oauth_token[:6]}...{access_token.oauth_token[-4:]}"
    )
    return await request_json(product, settings, access_token, api_path)


def print_result(product: DemoProduct, result: Any) -> None:
    """Print a bounded REST response suitable for a terminal demo."""

    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if len(rendered) > 4000:
        rendered = f"{rendered[:4000]}\n... response truncated ..."
    print(f"\nSigned {product.name} REST response:")
    print(rendered)


def build_parser(product: DemoProduct) -> argparse.ArgumentParser:
    prefix = product.env_prefix
    parser = argparse.ArgumentParser(
        description=f"{product.name} OAuth 1.0a (RSA-SHA1) demo"
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv(f"{prefix}_URL"),
        help=f"{product.name} base URL (or {prefix}_URL)",
    )
    parser.add_argument(
        "--consumer-key",
        default=os.getenv(f"{prefix}_OAUTH_CONSUMER_KEY"),
        help="Incoming Application Link consumer key",
    )
    private_key_env = f"{prefix}_OAUTH_PRIVATE_KEY_FILE"
    parser.add_argument(
        "--private-key-file",
        type=Path,
        default=Path(os.environ[private_key_env])
        if os.getenv(private_key_env)
        else None,
        help="RSA private key PEM file",
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument(
        "--trust-env",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Honor HTTP_PROXY/HTTPS_PROXY environment variables",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    authorize_parser = subparsers.add_parser(
        "authorize",
        help="Run the complete interactive three-legged OAuth flow",
    )
    authorize_parser.add_argument(
        "--token-file",
        type=Path,
        default=product.default_token_file,
    )
    authorize_parser.add_argument(
        "--api-path",
        default=product.default_api_path,
    )
    authorize_parser.add_argument(
        "--open-browser",
        action=argparse.BooleanOptionalAction,
        default=True,
    )

    request_parser = subparsers.add_parser(
        "request",
        help="Use a previously saved access token",
    )
    request_parser.add_argument(
        "--token-file",
        type=Path,
        default=product.default_token_file,
    )
    request_parser.add_argument(
        "--api-path",
        default=product.default_api_path,
    )
    return parser


def settings_from_args(
    product: DemoProduct,
    args: argparse.Namespace,
) -> DemoSettings:
    prefix = product.env_prefix
    missing = [
        name
        for name, value in (
            (f"--base-url / {prefix}_URL", args.base_url),
            (
                f"--consumer-key / {prefix}_OAUTH_CONSUMER_KEY",
                args.consumer_key,
            ),
            (
                f"--private-key-file / {prefix}_OAUTH_PRIVATE_KEY_FILE",
                args.private_key_file,
            ),
        )
        if not value
    ]
    if missing:
        raise ValueError(f"Missing required configuration: {', '.join(missing)}")
    return DemoSettings(
        base_url=args.base_url.rstrip("/"),
        consumer_key=args.consumer_key,
        private_key=load_private_key(args.private_key_file),
        timeout=args.timeout,
        trust_env=args.trust_env,
    )


async def async_main(
    product: DemoProduct,
    args: argparse.Namespace,
) -> None:
    settings = settings_from_args(product, args)
    if args.command == "authorize":
        result = await authorize(
            product,
            settings,
            token_file=args.token_file,
            api_path=args.api_path,
            open_browser=args.open_browser,
        )
    else:
        token = load_token(args.token_file, settings)
        result = await request_json(product, settings, token, args.api_path)
    print_result(product, result)


def run_cli(product: DemoProduct) -> int:
    args = build_parser(product).parse_args()
    try:
        asyncio.run(async_main(product, args))
    except (
        AtlassianError,
        TypeError,
        ValueError,
        RuntimeError,
        httpx.HTTPError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0
