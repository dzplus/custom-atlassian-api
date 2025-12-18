"""
Issue Link Models - Issue 链接相关数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field


class IssueLinkType(BaseModel):
    """Issue 链接类型"""
    id: Optional[str] = None
    name: Optional[str] = None
    inward: Optional[str] = None
    outward: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")

    model_config = {"populate_by_name": True}


class LinkedIssue(BaseModel):
    """链接的 Issue 简要信息"""
    id: Optional[str] = None
    key: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    fields: Optional[dict] = None

    model_config = {"populate_by_name": True}


class IssueLink(BaseModel):
    """Issue 链接"""
    id: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    type: Optional[IssueLinkType] = None
    inward_issue: Optional[LinkedIssue] = Field(None, alias="inwardIssue")
    outward_issue: Optional[LinkedIssue] = Field(None, alias="outwardIssue")

    model_config = {"populate_by_name": True}


class CreateIssueLinkRequest(BaseModel):
    """创建 Issue 链接请求"""
    type: dict  # {"name": "Blocks"} 或 {"id": "10000"}
    inward_issue: dict = Field(alias="inwardIssue")  # {"key": "HSP-1"}
    outward_issue: dict = Field(alias="outwardIssue")  # {"key": "MKY-1"}
    comment: Optional[dict] = None

    model_config = {"populate_by_name": True}


class IssueLinkTypeList(BaseModel):
    """Issue 链接类型列表"""
    issue_link_types: list[IssueLinkType] = Field(alias="issueLinkTypes")

    model_config = {"populate_by_name": True}
