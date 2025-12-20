"""
Group Models - 用户组相关数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field

from atlassian.jira.models.user import User


class Group(BaseModel):
    """
    用户组模型
    """
    name: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    users: Optional[dict] = None  # 包含分页信息的用户列表
    expand: Optional[str] = None

    model_config = {"populate_by_name": True}


class GroupMember(BaseModel):
    """
    用户组成员模型
    """
    name: Optional[str] = None
    key: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    display_name: Optional[str] = Field(None, alias="displayName")
    active: Optional[bool] = None

    model_config = {"populate_by_name": True}


class GroupMembers(BaseModel):
    """
    用户组成员列表（分页）
    """
    self_url: Optional[str] = Field(None, alias="self")
    next_page: Optional[str] = Field(None, alias="nextPage")
    max_results: Optional[int] = Field(None, alias="maxResults")
    start_at: Optional[int] = Field(None, alias="startAt")
    total: Optional[int] = None
    is_last: Optional[bool] = Field(None, alias="isLast")
    values: Optional[list[User]] = None

    model_config = {"populate_by_name": True}
