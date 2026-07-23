#!/usr/bin/env python3
"""Interactive Confluence OAuth 1.0a demo built on the public SDK API."""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import dataclass
import json
import os
from pathlib import Path
import sys
from typing import Any
import webbrowser

import httpx

from atlassian import (
    AtlassianOAuth1Flow,
    ConfluenceClient,
    OAuth1Config,
    OAuth1Token,
)
from atlassian.common.exceptions import AtlassianError


DEFAULT_TOKEN_FILE = (
    Path.home() / ".config" / "custom-atlassian-api" / "confluence-oauth1.json"
)
DEFAULT_API_PATH = "/rest/api/content?limit=1"


@dataclass(frozen=True)
class DemoSettings:
    base_url: str
    consumer_key: str
    private_key: str
    timeout: float = 30.0
    trust_env: bool = False


def load_private_key(path: Path) -> str:
    """Read an RSA private key without printing it."""

    try:
        private_key = path.expanduser().read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"Unable to read private key file: {path}") from exc
    if "PRIVATE KEY" not in private_key:
        raise ValueError(f"Not a PEM private key: {path}")
    return private_key


def save_token(path: Path, settings: DemoSettings, token: OAuth1Token) -> None:
    """Persist an access token to a user-only JSON file."""

    token_path = path.expanduser()
    token_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    payload = {
        "base_url": settings.base_url,
        "consumer_key": settings.consumer_key,
        **token.as_dict(),
    }
    fd = os.open(token_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    token_path.chmod(0o600)


def load_token(path: Path) -> OAuth1Token:
    """Load an access token saved by :func:`save_token`."""

    token_path = path.expanduser()
    try:
        data = json.loads(token_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to read token file: {token_path}") from exc
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
    settings: DemoSettings,
    token: OAuth1Token,
    api_path: str,
) -> Any:
    """Call a Confluence endpoint through the SDK's OAuth-enabled client."""

    oauth1 = OAuth1Config.from_access_token(
        consumer_key=settings.consumer_key,
        private_key=settings.private_key,
        token=token,
    )
    async with ConfluenceClient(
        base_url=settings.base_url,
        auth_mode="oauth1",
        oauth1=oauth1,
        timeout=settings.timeout,
        trust_env=settings.trust_env,
    ) as client:
        return await client.get_json(api_path)


async def authorize(
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

    print("\nAuthorize this application in Confluence:")
    print(authorization_url)
    if open_browser:
        opened = webbrowser.open(authorization_url)
        if not opened:
            print("The browser did not open automatically; use the URL above.")

    verifier = input("\nPaste the verification code shown by Confluence: ").strip()
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
    return await request_json(settings, access_token, api_path)


def print_result(result: Any) -> None:
    """Print a bounded REST response suitable for a terminal demo."""

    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if len(rendered) > 4000:
        rendered = f"{rendered[:4000]}\n... response truncated ..."
    print("\nSigned Confluence REST response:")
    print(rendered)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Confluence OAuth 1.0a (RSA-SHA1) demo"
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("CONFLUENCE_URL"),
        help="Confluence base URL (or CONFLUENCE_URL)",
    )
    parser.add_argument(
        "--consumer-key",
        default=os.getenv("CONFLUENCE_OAUTH_CONSUMER_KEY"),
        help="Incoming Application Link consumer key",
    )
    parser.add_argument(
        "--private-key-file",
        type=Path,
        default=(
            Path(os.environ["CONFLUENCE_OAUTH_PRIVATE_KEY_FILE"])
            if os.getenv("CONFLUENCE_OAUTH_PRIVATE_KEY_FILE")
            else None
        ),
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
        default=DEFAULT_TOKEN_FILE,
    )
    authorize_parser.add_argument("--api-path", default=DEFAULT_API_PATH)
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
        default=DEFAULT_TOKEN_FILE,
    )
    request_parser.add_argument("--api-path", default=DEFAULT_API_PATH)
    return parser


def settings_from_args(args: argparse.Namespace) -> DemoSettings:
    missing = [
        name
        for name, value in (
            ("--base-url / CONFLUENCE_URL", args.base_url),
            ("--consumer-key / CONFLUENCE_OAUTH_CONSUMER_KEY", args.consumer_key),
            (
                "--private-key-file / CONFLUENCE_OAUTH_PRIVATE_KEY_FILE",
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


async def async_main(args: argparse.Namespace) -> None:
    settings = settings_from_args(args)
    if args.command == "authorize":
        result = await authorize(
            settings,
            token_file=args.token_file,
            api_path=args.api_path,
            open_browser=args.open_browser,
        )
    else:
        token = load_token(args.token_file)
        result = await request_json(settings, token, args.api_path)
    print_result(result)


def main() -> int:
    args = build_parser().parse_args()
    try:
        asyncio.run(async_main(args))
    except (AtlassianError, ValueError, RuntimeError, httpx.HTTPError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
