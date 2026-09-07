"""BaseHttpClient 的认证模式与 HTTP 透传行为（不访问真实实例）。"""

import asyncio
from typing import Any, Callable

import httpx
import pytest

from atlassian.common.client import BearerAuthInfo
from atlassian.confluence import ConfluenceClient
from atlassian.jira import JiraClient


def collect(handler_result: Any = None) -> tuple[list[httpx.Request], httpx.MockTransport]:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=handler_result if handler_result is not None else {})

    return seen, httpx.MockTransport(handler)


def run(client: ConfluenceClient, factory: Callable[[], Any]) -> Any:
    async def main() -> Any:
        try:
            return await factory()
        finally:
            await client.close()

    return asyncio.run(main())


# ========== #10 Bearer / PAT ==========


def test_bearer_mode_sends_authorization_header_without_credentials() -> None:
    seen, transport = collect()
    client = ConfluenceClient(
        base_url="https://cf.example.test",
        auth_mode="bearer",
        token="pat-123",
        trust_env=False,
        transport=transport,
    )

    run(client, lambda: client.get_json("/rest/api/user/current"))

    assert seen[0].headers["Authorization"] == "Bearer pat-123"


def test_bearer_mode_reads_token_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CONFLUENCE_TOKEN", "from-env")
    seen, transport = collect()
    client = ConfluenceClient(
        base_url="https://cf.example.test",
        auth_mode="bearer",
        trust_env=False,
        transport=transport,
    )

    run(client, lambda: client.get_json("/rest/api/user/current"))

    assert seen[0].headers["Authorization"] == "Bearer from-env"


def test_bearer_mode_reads_pat_token_alias(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("JIRA_TOKEN", raising=False)
    monkeypatch.setenv("JIRA_PAT_TOKEN", "pat-alias")

    client = JiraClient(
        base_url="https://jira.example.test",
        auth_mode="bearer",
        trust_env=False,
    )

    assert client._get_auth_headers()["Authorization"] == "Bearer pat-alias"


def test_bearer_mode_requires_a_token(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("CONFLUENCE_TOKEN", "CONFLUENCE_PAT_TOKEN", "ATLASSIAN_TOKEN", "ATLASSIAN_PAT_TOKEN"):
        monkeypatch.delenv(name, raising=False)

    with pytest.raises(ValueError, match="TOKEN"):
        ConfluenceClient(
            base_url="https://cf.example.test",
            auth_mode="bearer",
            trust_env=False,
        )


def test_bearer_mode_skips_login_round_trip() -> None:
    seen, transport = collect()
    client = ConfluenceClient(
        base_url="https://cf.example.test",
        auth_mode="bearer",
        token="pat-123",
        trust_env=False,
        transport=transport,
    )

    assert client.is_logged_in is True
    info = run(client, client.login)

    assert isinstance(info, BearerAuthInfo)
    assert seen == []


# ========== #11 multipart / 表单 Content-Type ==========


def test_multipart_upload_keeps_httpx_generated_content_type() -> None:
    seen, transport = collect()
    client = ConfluenceClient(
        base_url="https://cf.example.test",
        username="u",
        password="p",
        auth_mode="basic",
        trust_env=False,
        transport=transport,
    )

    run(
        client,
        lambda: client.post(
            "/rest/api/content/1/child/attachment",
            headers={"X-Atlassian-Token": "no-check"},
            files={"file": ("a.png", b"\x89PNG", "image/png")},
        ),
    )

    content_type = seen[0].headers["Content-Type"]
    assert content_type.startswith("multipart/form-data; boundary=")
    assert seen[0].headers["X-Atlassian-Token"] == "no-check"
    assert b"a.png" in seen[0].content


def test_form_data_request_keeps_urlencoded_content_type() -> None:
    seen, transport = collect()
    client = ConfluenceClient(
        base_url="https://cf.example.test",
        username="u",
        password="p",
        auth_mode="basic",
        trust_env=False,
        transport=transport,
    )

    run(client, lambda: client.post("/rest/whatever", data={"a": "b"}))

    assert seen[0].headers["Content-Type"] == "application/x-www-form-urlencoded"


def test_caller_supplied_content_type_wins_over_httpx_default() -> None:
    seen, transport = collect()
    client = ConfluenceClient(
        base_url="https://cf.example.test",
        username="u",
        password="p",
        auth_mode="basic",
        trust_env=False,
        transport=transport,
    )

    run(
        client,
        lambda: client.post(
            "/rest/whatever",
            headers={"Content-Type": "application/octet-stream"},
            data={"a": "b"},
        ),
    )

    assert seen[0].headers["Content-Type"] == "application/octet-stream"


def test_json_request_still_sends_json_content_type() -> None:
    seen, transport = collect()
    client = ConfluenceClient(
        base_url="https://cf.example.test",
        username="u",
        password="p",
        auth_mode="basic",
        trust_env=False,
        transport=transport,
    )

    run(client, lambda: client.post_json("/rest/api/content", data={"a": "b"}))

    assert seen[0].headers["Content-Type"] == "application/json"


# ========== #12 verify / transport 透传 ==========


def test_transport_is_used_without_replacing_private_client() -> None:
    seen, transport = collect({"ok": True})
    client = ConfluenceClient(
        base_url="https://cf.example.test",
        username="u",
        password="p",
        auth_mode="basic",
        trust_env=False,
        transport=transport,
    )

    result = run(client, lambda: client.get_json("/rest/api/space"))

    assert result == {"ok": True}
    assert len(seen) == 1


def test_verify_is_passed_to_httpx_client(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}
    real_client = httpx.AsyncClient

    def spy(*args: Any, **kwargs: Any) -> httpx.AsyncClient:
        captured.update(kwargs)
        return real_client(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", spy)

    client = ConfluenceClient(
        base_url="https://cf.example.test",
        username="u",
        password="p",
        auth_mode="basic",
        trust_env=False,
        verify=False,
    )
    client._get_client()

    assert captured["verify"] is False
    assert captured["follow_redirects"] is True
    asyncio.run(client.close())


def test_async_context_manager_reuses_configured_transport() -> None:
    seen, transport = collect({"ok": True})

    async def main() -> Any:
        async with ConfluenceClient(
            base_url="https://cf.example.test",
            username="u",
            password="p",
            auth_mode="basic",
            trust_env=False,
            transport=transport,
        ) as client:
            return await client.get_json("/rest/api/space")

    assert asyncio.run(main()) == {"ok": True}
    assert len(seen) == 1


def test_custom_headers_survive_session_relogin() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if request.url.path == "/rest/auth/1/session":
            return httpx.Response(200, json={"session": {"name": "JSESSIONID", "value": "v2"}})
        if len(calls) == 1:
            return httpx.Response(401, json={})
        return httpx.Response(200, json={"ok": True})

    client = ConfluenceClient(
        base_url="https://cf.example.test",
        username="u",
        password="p",
        auth_mode="session",
        auto_login=False,
        trust_env=False,
        transport=httpx.MockTransport(handler),
    )
    client._logged_in = True

    async def main() -> Any:
        try:
            return await client.get_json("/rest/api/space", headers={"X-Trace": "abc"})
        finally:
            await client.close()

    assert asyncio.run(main()) == {"ok": True}
    assert [c.headers.get("X-Trace") for c in calls if c.url.path == "/rest/api/space"] == [
        "abc",
        "abc",
    ]
