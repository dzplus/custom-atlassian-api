"""Confluence 评论写能力与点赞能力的单元测试（不访问真实实例）。"""

import asyncio
import json
from typing import Any, Callable

import httpx
import pytest

from atlassian.common.exceptions import AtlassianNotFoundError
from atlassian.confluence import ConfluenceClient


def make_client(handler: Callable[[httpx.Request], httpx.Response]) -> ConfluenceClient:
    client = ConfluenceClient(
        base_url="https://cf.example.test",
        username="duanzhang",
        password="secret",
        auth_mode="basic",
        trust_env=False,
    )
    client._client = httpx.AsyncClient(
        base_url=client.base_url,
        transport=httpx.MockTransport(handler),
    )
    return client


def run(client: ConfluenceClient, coro_factory: Callable[[], Any]) -> Any:
    async def main() -> Any:
        try:
            return await coro_factory()
        finally:
            await client._client.aclose()

    return asyncio.run(main())


def body_of(request: httpx.Request) -> dict:
    return json.loads(request.content)


# ========== Footer comment ==========


def test_add_comment_posts_content_of_type_comment() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"id": "1001", "type": "comment"})

    client = make_client(handler)
    comment = run(
        client,
        lambda: client.content.add_comment("223740097", "<p>你好</p>"),
    )

    assert comment.id == "1001"
    assert seen[0].url.path == "/rest/api/content"
    assert body_of(seen[0]) == {
        "type": "comment",
        "container": {"id": "223740097", "type": "page"},
        "body": {"storage": {"value": "<p>你好</p>", "representation": "storage"}},
    }


def test_reply_to_comment_sets_ancestors_and_keeps_page_container() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"id": "1002", "type": "comment"})

    client = make_client(handler)
    run(
        client,
        lambda: client.content.reply_to_comment(
            "1001",
            "<p>回复</p>",
            container_id="223740097",
        ),
    )

    payload = body_of(seen[0])
    assert payload["ancestors"] == [{"id": "1001", "type": "comment"}]
    assert payload["container"] == {"id": "223740097", "type": "page"}


# ========== Inline comment ==========


def test_get_inline_comments_filters_by_location() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"results": [], "size": 0})

    client = make_client(handler)
    run(
        client,
        lambda: client.content.get_inline_comments(
            "223740097",
            expand="extensions.resolution",
        ),
    )

    assert seen[0].url.path == "/rest/api/content/223740097/child/comment"
    assert seen[0].url.params["location"] == "inline"
    assert seen[0].url.params["expand"] == "extensions.resolution"


def test_add_inline_comment_uses_plugin_namespace_with_required_fields() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(
            200,
            json={"id": 223762838, "markerRef": "90dc2366-bbee"},
        )

    client = make_client(handler)
    created = run(
        client,
        lambda: client.content.add_inline_comment(
            "223740097",
            selection="Markdown 语法兼容性测试",
            body="<p>划线批注</p>",
        ),
    )

    assert created["markerRef"] == "90dc2366-bbee"
    assert seen[0].url.path == "/rest/inlinecomments/1.0/comments"

    payload = body_of(seen[0])
    assert payload["containerId"] == 223740097
    assert payload["originalSelection"] == "Markdown 语法兼容性测试"
    assert payload["matchIndex"] == 0
    assert payload["numMatches"] == 1
    assert payload["serializedHighlights"] == ""
    assert isinstance(payload["lastFetchTime"], int)


def test_resolve_inline_comment_puts_full_object_to_resolve_path() -> None:
    raw_comment = {
        "id": 223762838,
        "body": "<p>划线批注</p>",
        "markerRef": "90dc2366-bbee",
        "originalSelection": "Markdown 语法兼容性测试",
        "parentCommentId": 0,
        "resolveProperties": {"resolved": False},
    }
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.method == "GET":
            return httpx.Response(200, json=[raw_comment])
        return httpx.Response(200, json={"id": 223762838})

    client = make_client(handler)
    run(
        client,
        lambda: client.content.resolve_inline_comment("223762838", "223740097"),
    )

    assert seen[0].url.params["containerId"] == "223740097"
    assert seen[1].method == "PUT"
    assert seen[1].url.path == (
        "/rest/inlinecomments/1.0/comments/223762838/resolve/true/dangling/false"
    )

    payload = body_of(seen[1])
    assert payload["markerRef"] == raw_comment["markerRef"]
    assert payload["originalSelection"] == raw_comment["originalSelection"]
    assert payload["containerId"] == 223740097
    assert payload["serializedHighlights"] == ""
    assert payload["deleted"] is False
    assert payload["active"] is True


def test_unresolve_inline_comment_flips_path_segment() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.method == "GET":
            return httpx.Response(200, json=[{"id": 223762838}])
        return httpx.Response(200, json={"id": 223762838})

    client = make_client(handler)
    run(
        client,
        lambda: client.content.resolve_inline_comment(
            "223762838",
            "223740097",
            resolved=False,
            dangling=True,
        ),
    )

    assert seen[1].url.path == (
        "/rest/inlinecomments/1.0/comments/223762838/resolve/false/dangling/true"
    )


def test_resolve_inline_comment_raises_when_comment_not_on_page() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{"id": 1}])

    client = make_client(handler)

    with pytest.raises(AtlassianNotFoundError):
        run(
            client,
            lambda: client.content.resolve_inline_comment("223762838", "223740097"),
        )


# ========== Likes ==========


def test_get_likes_reads_plugin_endpoint() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(
            200,
            json={"likes": [], "content_type": "page", "content_id": "223740097"},
        )

    client = make_client(handler)
    likes = run(client, lambda: client.like.get_likes("223740097"))

    assert likes["content_type"] == "page"
    assert seen[0].url.path == "/rest/likes/1.0/content/223740097/likes"


def test_add_like_defaults_to_authenticated_username() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(
            200,
            json={
                "likes": [{"user": {"name": "duanzhang"}}],
                "content_type": "page",
                "content_id": "223740097",
            },
        )

    client = make_client(handler)
    likes = run(client, lambda: client.like.add_like("223740097"))

    assert seen[0].method == "POST"
    assert body_of(seen[0]) == {"username": "duanzhang"}
    assert likes["likes"][0]["user"]["name"] == "duanzhang"


def test_add_like_is_idempotent_when_already_liked() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.method == "POST":
            return httpx.Response(400, text="The content cannot be liked")
        return httpx.Response(
            200,
            json={
                "likes": [{"user": {"name": "duanzhang"}}],
                "content_type": "page",
                "content_id": "223740097",
            },
        )

    client = make_client(handler)
    likes = run(client, lambda: client.like.add_like("223740097"))

    assert [r.method for r in seen] == ["POST", "GET"]
    assert likes["likes"][0]["user"]["name"] == "duanzhang"


def test_add_like_reraises_when_400_is_not_a_duplicate() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return httpx.Response(400, text="The content cannot be liked")
        return httpx.Response(
            200,
            json={"likes": [], "content_type": "page", "content_id": "223740097"},
        )

    client = make_client(handler)

    with pytest.raises(httpx.HTTPStatusError):
        run(client, lambda: client.like.add_like("223740097"))


def test_remove_like_deletes_plugin_endpoint() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(204)

    client = make_client(handler)
    result = run(client, lambda: client.like.remove_like("223740097"))

    assert result is None
    assert seen[0].method == "DELETE"
    assert seen[0].url.path == "/rest/likes/1.0/content/223740097/likes"
