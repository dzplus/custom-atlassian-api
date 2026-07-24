"""Interactive Jira OAuth 1.0a demo built on the public SDK API."""

from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from atlassian import JiraClient
from examples import oauth1_demo_common

DEFAULT_TOKEN_FILE = (
    Path.home() / ".config" / "custom-atlassian-api" / "jira-oauth1.json"
)
DEFAULT_API_PATH = "/rest/api/2/myself"
PRODUCT = oauth1_demo_common.DemoProduct(
    name="Jira",
    env_prefix="JIRA",
    client_type=JiraClient,
    default_token_file=DEFAULT_TOKEN_FILE,
    default_api_path=DEFAULT_API_PATH,
)


def build_parser() -> ArgumentParser:
    return oauth1_demo_common.build_parser(PRODUCT)


def main() -> int:
    return oauth1_demo_common.run_cli(PRODUCT)


if __name__ == "__main__":
    raise SystemExit(main())
