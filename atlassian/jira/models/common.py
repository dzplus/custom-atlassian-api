"""
Common Models - 通用数据模型

包含分页、错误、属性等通用模型
"""

from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel, Field


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    通用分页响应模型

    用于所有返回分页数据的API
    """
    start_at: int = Field(alias="startAt")
    max_results: int = Field(alias="maxResults")
    total: int
    is_last: Optional[bool] = Field(None, alias="isLast")
    values: list[T]

    model_config = {"populate_by_name": True}


class SimpleListResponse(BaseModel, Generic[T]):
    """
    简单列表响应模型

    用于返回简单列表的API（无分页信息）
    """
    values: list[T]


class ErrorMessage(BaseModel):
    """
    错误消息模型
    """
    message: Optional[str] = None
    error_messages: Optional[list[str]] = Field(None, alias="errorMessages")
    errors: Optional[dict[str, str]] = None

    model_config = {"populate_by_name": True}


class EntityProperty(BaseModel):
    """
    实体属性模型

    用于各种资源的属性（Issue Properties, Project Properties等）
    """
    key: str
    value: Any


class EntityPropertyKeys(BaseModel):
    """
    实体属性键列表
    """
    keys: list[dict[str, str]]


class SimpleLink(BaseModel):
    """
    简单链接模型
    """
    id: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")

    model_config = {"populate_by_name": True}


class NamedResource(BaseModel):
    """
    命名资源基类

    包含id, name, self等基本字段
    """
    id: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    name: Optional[str] = None
    description: Optional[str] = None

    model_config = {"populate_by_name": True}


class Visibility(BaseModel):
    """
    可见性模型

    用于评论、工作日志等的可见性设置
    """
    type: Optional[str] = None  # "group" or "role"
    value: Optional[str] = None  # group name or role name
    identifier: Optional[str] = None

    model_config = {"populate_by_name": True}


class TimeTracking(BaseModel):
    """
    时间跟踪模型
    """
    original_estimate: Optional[str] = Field(None, alias="originalEstimate")
    remaining_estimate: Optional[str] = Field(None, alias="remainingEstimate")
    time_spent: Optional[str] = Field(None, alias="timeSpent")
    original_estimate_seconds: Optional[int] = Field(None, alias="originalEstimateSeconds")
    remaining_estimate_seconds: Optional[int] = Field(None, alias="remainingEstimateSeconds")
    time_spent_seconds: Optional[int] = Field(None, alias="timeSpentSeconds")

    model_config = {"populate_by_name": True}


class ServerInfo(BaseModel):
    """
    服务器信息模型
    """
    base_url: Optional[str] = Field(None, alias="baseUrl")
    version: Optional[str] = None
    version_numbers: Optional[list[int]] = Field(None, alias="versionNumbers")
    deployment_type: Optional[str] = Field(None, alias="deploymentType")
    build_number: Optional[int] = Field(None, alias="buildNumber")
    build_date: Optional[str] = Field(None, alias="buildDate")
    server_time: Optional[str] = Field(None, alias="serverTime")
    scm_info: Optional[str] = Field(None, alias="scmInfo")
    server_title: Optional[str] = Field(None, alias="serverTitle")

    model_config = {"populate_by_name": True}


class Scope(BaseModel):
    """
    范围模型

    用于定义资源的作用域（项目、全局等）
    """
    type: Optional[str] = None  # "PROJECT", "GLOBAL"
    project: Optional[dict] = None

    model_config = {"populate_by_name": True}
