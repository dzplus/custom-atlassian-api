"""
Content Models - Confluence 内容相关数据模型
"""

from typing import Any, Optional
from pydantic import BaseModel, Field

from atlassian.confluence.models.user import User
from atlassian.confluence.models.space import Space


class ContentBody(BaseModel):
    """内容主体"""
    value: Optional[str] = None
    representation: Optional[str] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class ContentBodyContainer(BaseModel):
    """内容主体容器"""
    storage: Optional[ContentBody] = None
    view: Optional[ContentBody] = None
    export_view: Optional[ContentBody] = Field(None, alias="export_view")
    styled_view: Optional[ContentBody] = Field(None, alias="styled_view")
    editor: Optional[ContentBody] = None
    editor2: Optional[ContentBody] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class ContentVersion(BaseModel):
    """内容版本"""
    by: Optional[User] = None
    when: Optional[str] = None
    message: Optional[str] = None
    number: Optional[int] = None
    minor_edit: Optional[bool] = Field(None, alias="minorEdit")

    model_config = {"populate_by_name": True, "extra": "allow"}


class ContentHistory(BaseModel):
    """内容历史"""
    latest: Optional[bool] = None
    created_by: Optional[User] = Field(None, alias="createdBy")
    created_date: Optional[str] = Field(None, alias="createdDate")
    last_updated: Optional[ContentVersion] = Field(None, alias="lastUpdated")
    previous_version: Optional[ContentVersion] = Field(None, alias="previousVersion")
    contributors: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class Content(BaseModel):
    """Confluence 内容（页面/博客）"""
    id: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    title: Optional[str] = None
    space: Optional[Space] = None
    history: Optional[ContentHistory] = None
    version: Optional[ContentVersion] = None
    ancestors: Optional[list[dict]] = None
    operations: Optional[list[dict]] = None
    children: Optional[dict] = None
    descendants: Optional[dict] = None
    container: Optional[dict] = None
    body: Optional[ContentBodyContainer] = None
    restrictions: Optional[dict] = None
    metadata: Optional[dict] = None
    extensions: Optional[dict] = None
    _links: Optional[dict] = None
    _expandable: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class ContentList(BaseModel):
    """内容列表"""
    results: list[Content] = []
    start: Optional[int] = None
    limit: Optional[int] = None
    size: Optional[int] = None
    _links: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class ContentLabel(BaseModel):
    """内容标签"""
    prefix: Optional[str] = None
    name: Optional[str] = None
    id: Optional[str] = None
    label: Optional[str] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class ContentLabelList(BaseModel):
    """内容标签列表"""
    results: list[ContentLabel] = []
    start: Optional[int] = None
    limit: Optional[int] = None
    size: Optional[int] = None
    _links: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class ContentProperty(BaseModel):
    """内容属性"""
    id: Optional[str] = None
    key: Optional[str] = None
    value: Optional[Any] = None
    version: Optional[dict] = None
    content: Optional[Content] = None
    _links: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class ContentPropertyList(BaseModel):
    """内容属性列表"""
    results: list[ContentProperty] = []
    start: Optional[int] = None
    limit: Optional[int] = None
    size: Optional[int] = None
    _links: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class Attachment(BaseModel):
    """附件"""
    id: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    title: Optional[str] = None
    version: Optional[ContentVersion] = None
    container: Optional[dict] = None
    metadata: Optional[dict] = None
    extensions: Optional[dict] = None
    _links: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class AttachmentList(BaseModel):
    """附件列表"""
    results: list[Attachment] = []
    start: Optional[int] = None
    limit: Optional[int] = None
    size: Optional[int] = None
    _links: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class Comment(BaseModel):
    """评论"""
    id: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    title: Optional[str] = None
    version: Optional[ContentVersion] = None
    container: Optional[dict] = None
    body: Optional[ContentBodyContainer] = None
    extensions: Optional[dict] = None
    _links: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class CommentList(BaseModel):
    """评论列表"""
    results: list[Comment] = []
    start: Optional[int] = None
    limit: Optional[int] = None
    size: Optional[int] = None
    _links: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class SearchResult(BaseModel):
    """搜索结果项"""
    content: Optional[Content] = None
    space: Optional[Space] = None
    user: Optional[User] = None
    title: Optional[str] = None
    excerpt: Optional[str] = None
    url: Optional[str] = None
    result_global_container: Optional[dict] = Field(None, alias="resultGlobalContainer")
    entity_type: Optional[str] = Field(None, alias="entityType")
    last_modified: Optional[str] = Field(None, alias="lastModified")

    model_config = {"populate_by_name": True, "extra": "allow"}


class SearchResultList(BaseModel):
    """搜索结果列表"""
    results: list[SearchResult] = []
    start: Optional[int] = None
    limit: Optional[int] = None
    size: Optional[int] = None
    total_size: Optional[int] = Field(None, alias="totalSize")
    cql_query: Optional[str] = Field(None, alias="cqlQuery")
    search_duration: Optional[int] = Field(None, alias="searchDuration")
    _links: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}
