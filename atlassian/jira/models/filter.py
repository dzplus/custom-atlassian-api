"""
Filter Models - 过滤器相关数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field

from atlassian.jira.models.user import User


class FilterPermission(BaseModel):
    """
    过滤器权限模型
    """
    id: Optional[int] = None
    type: Optional[str] = None  # "group", "project", "projectRole", "global", "authenticated"
    project: Optional[dict] = None
    role: Optional[dict] = None
    group: Optional[dict] = None
    user: Optional[User] = None

    model_config = {"populate_by_name": True}


class FilterSubscription(BaseModel):
    """
    过滤器订阅模型
    """
    id: Optional[int] = None
    user: Optional[User] = None
    group: Optional[dict] = None

    model_config = {"populate_by_name": True}


class Filter(BaseModel):
    """
    过滤器模型
    """
    id: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    name: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[User] = None
    jql: Optional[str] = None
    view_url: Optional[str] = Field(None, alias="viewUrl")
    search_url: Optional[str] = Field(None, alias="searchUrl")
    favourite: Optional[bool] = None
    favourited_count: Optional[int] = Field(None, alias="favouritedCount")
    share_permissions: Optional[list[FilterPermission]] = Field(None, alias="sharePermissions")
    subscriptions: Optional[list[FilterSubscription]] = None
    editable: Optional[bool] = None

    model_config = {"populate_by_name": True}


class Column(BaseModel):
    """
    列定义模型
    """
    label: Optional[str] = None
    value: Optional[str] = None

    model_config = {"populate_by_name": True}
