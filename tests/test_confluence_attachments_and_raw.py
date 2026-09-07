"""Confluence 附件下载、_links 字段与 *_raw 变体（不访问真实实例）。"""

import asyncio
from typing import Any, Callable

import httpx
import pytest

from atlassian.confluence import ConfluenceClient
from atlassian.confluence.models.content import Attachment, Content, ContentList
from atlassian.confluence.models.space import Space
from atlassian.confluence.models.user import User


def make_client(handler: Callable[[httpx.Request], httpx.Response]) -> ConfluenceClient:
    return ConfluenceClient(
        base_url="https://cf.example.test",
        username="u",
        password="p",
        auth_mode="basic",
        trust_env=False,
        transport=httpx.MockTransport(handler),
    )


def run(client: ConfluenceClient, factory: Callable[[], Any]) -> Any:
    async def main() -> Any:
        try:
            return await factory()
        finally:
            await client.close()

    return asyncio.run(main())


# ========== #14 _links 是真正的 field ==========


@pytest.mark.parametrize(
    "model, payload",
    [
        (Content, {"id": "1", "type": "page", "title": "T"}),
        (ContentList, {"results": []}),
        (Attachment, {"id": "att1", "title": "a.png"}),
        (Space, {"key": "DEV", "name": "Dev"}),
        (User, {"username": "duanzhang"}),
    ],
)
def test_links_is_readable_by_name(model: Any, payload: dict) -> None:
    links = {"webui": "/display/DEV/T", "download": "/download/attachments/1/a.png"}
    obj = model.model_validate({**payload, "_links": links})

    assert "links" in model.model_fields
    assert obj.links == links


def test_links_round_trips_through_alias() -> None:
    content = Content.model_validate(
        {"id": "1", "type": "page", "title": "T", "_links": {"webui": "/x"}}
    )

    assert content.model_dump(by_alias=True)["_links"] == {"webui": "/x"}
    assert content.model_dump()["links"] == {"webui": "/x"}


def test_links_absent_stays_none() -> None:
    assert Content.model_validate({"id": "1", "type": "page", "title": "T"}).links is None


# ========== #15 附件下载 ==========


def test_download_attachment_follows_download_link_with_credentials() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.path == "/rest/api/content/att1":
            return httpx.Response(
                200,
                json={
                    "id": "att1",
                    "title": "a.png",
                    "_links": {"download": "/download/attachments/1/a.png?version=1"},
                },
            )
        return httpx.Response(200, content=b"\x89PNG-bytes")

    client = make_client(handler)
    data = run(client, lambda: client.content.download_attachment("att1"))

    assert data == b"\x89PNG-bytes"
    assert seen[1].url.path == "/download/attachments/1/a.png"
    assert seen[1].url.params["version"] == "1"
    assert seen[1].headers["Authorization"].startswith("Basic ")
    assert seen[1].headers["Accept"] == "*/*"


def test_download_attachment_without_link_raises() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"id": "att1", "title": "a.png", "_links": {}})

    client = make_client(handler)

    with pytest.raises(ValueError, match="no download link"):
        run(client, lambda: client.content.download_attachment("att1"))


def test_same_origin_absolute_url_uses_authenticated_client() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=b"same-origin")

    client = make_client(handler)
    data = run(
        client,
        lambda: client.content.download_attachment_by_url(
            "https://cf.example.test/download/attachments/1/a.png"
        ),
    )

    assert data == b"same-origin"
    assert "Authorization" in seen[0].headers


def test_cross_origin_url_is_fetched_without_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen: list[httpx.Request] = []
    real_client = httpx.AsyncClient

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=b"external")

    def spy(*args: Any, **kwargs: Any) -> httpx.AsyncClient:
        kwargs.setdefault("transport", httpx.MockTransport(handler))
        return real_client(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", spy)

    client = ConfluenceClient(
        base_url="https://cf.example.test",
        username="u",
        password="p",
        auth_mode="basic",
        trust_env=False,
    )
    data = run(
        client,
        lambda: client.content.download_attachment_by_url(
            "https://cdn.example.com/blobs/a.png"
        ),
    )

    assert data == b"external"
    assert "Authorization" not in seen[-1].headers


def test_same_origin_detection() -> None:
    client = ConfluenceClient(
        base_url="https://cf.example.test",
        username="u",
        password="p",
        auth_mode="basic",
        trust_env=False,
    )
    is_same = client.content._is_same_origin

    assert is_same("/download/attachments/1/a.png") is True
    assert is_same("https://cf.example.test/download/a.png") is True
    assert is_same("https://cdn.example.com/a.png") is False
    assert is_same("http://cf.example.test/a.png") is False


# ========== #15 *_raw 变体 ==========


RAW_CASES = [
    ("get_all_raw", ("/rest/api/content",), {}),
    ("search_raw", ("/rest/api/content/search",), {"cql": "type=page"}),
    ("get_children_by_type_raw", ("/rest/api/content/1/child/page",), {"content_id": "1", "child_type": "page"}),
    ("get_attachments_raw", ("/rest/api/content/1/child/attachment",), {"content_id": "1"}),
    ("get_comments_raw", ("/rest/api/content/1/child/comment",), {"content_id": "1"}),
    ("get_descendants_by_type_raw", ("/rest/api/content/1/descendant/page",), {"content_id": "1", "descendant_type": "page"}),
    ("get_labels_raw", ("/rest/api/content/1/label",), {"content_id": "1"}),
    ("get_properties_raw", ("/rest/api/content/1/property",), {"content_id": "1"}),
]


@pytest.mark.parametrize("method, expected_path, kwargs", RAW_CASES)
def test_raw_variants_return_untouched_json(
    method: str, expected_path: tuple[str], kwargs: dict
) -> None:
    payload = {"results": [{"id": "1", "_links": {"webui": "/x"}}], "size": 1}
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=payload)

    client = make_client(handler)
    result = run(client, lambda: getattr(client.content, method)(**kwargs))

    assert result == payload
    assert result["results"][0]["_links"] == {"webui": "/x"}
    assert seen[0].url.path == expected_path[0]


def test_model_variant_still_validates_after_delegation() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "results": [{"id": "att1", "title": "a.png", "_links": {"download": "/d"}}],
                "size": 1,
            },
        )

    client = make_client(handler)
    attachments = run(client, lambda: client.content.get_attachments("1"))

    assert attachments.size == 1
    assert attachments.results[0].title == "a.png"
    assert attachments.results[0].links == {"download": "/d"}
