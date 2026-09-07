"""
Search Models - 搜索相关数据模型
"""

from typing import Any, Optional
from pydantic import BaseModel, Field

from atlassian.jira.models.issue import Issue


class SearchResults(BaseModel):
    """
    JQL搜索结果

    用于搜索Issue的返回结果
    """
    start_at: int = Field(alias="startAt")
    max_results: int = Field(alias="maxResults")
    total: int
    issues: list[Issue]
    expand: Optional[str] = None
    names: Optional[dict[str, str]] = None
    # 字段名避开 BaseModel.schema，用 alias 保持线上 JSON 的 schema 键不变
    schema_: Optional[dict] = Field(default=None, alias="schema")

    model_config = {"populate_by_name": True}
