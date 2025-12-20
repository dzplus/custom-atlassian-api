"""
Permission Models - 权限相关数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field


class PermissionGrant(BaseModel):
    """
    权限授予模型
    """
    id: Optional[int] = None
    self_url: Optional[str] = Field(None, alias="self")
    holder: Optional[dict] = None
    permission: Optional[str] = None

    model_config = {"populate_by_name": True}


class PermissionScheme(BaseModel):
    """
    权限方案模型
    """
    id: Optional[int] = None
    self_url: Optional[str] = Field(None, alias="self")
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[list[PermissionGrant]] = None
    expand: Optional[str] = None

    model_config = {"populate_by_name": True}


class Role(BaseModel):
    """
    角色模型
    """
    id: Optional[int] = None
    self_url: Optional[str] = Field(None, alias="self")
    name: Optional[str] = None
    description: Optional[str] = None
    actors: Optional[list[dict]] = None

    model_config = {"populate_by_name": True}


class RoleActor(BaseModel):
    """
    角色执行者模型
    """
    id: Optional[int] = None
    display_name: Optional[str] = Field(None, alias="displayName")
    type: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = Field(None, alias="avatarUrl")

    model_config = {"populate_by_name": True}


class SecurityLevel(BaseModel):
    """
    安全级别模型
    """
    id: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    name: Optional[str] = None
    description: Optional[str] = None

    model_config = {"populate_by_name": True}
