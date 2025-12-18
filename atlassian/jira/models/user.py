"""
User Models - 用户相关数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field


class AvatarUrls(BaseModel):
    """用户头像 URL"""
    x16: Optional[str] = Field(None, alias="16x16")
    x24: Optional[str] = Field(None, alias="24x24")
    x32: Optional[str] = Field(None, alias="32x32")
    x48: Optional[str] = Field(None, alias="48x48")

    model_config = {"populate_by_name": True}


class User(BaseModel):
    """用户基本信息"""
    self_url: Optional[str] = Field(None, alias="self")
    key: Optional[str] = None
    name: Optional[str] = None
    display_name: Optional[str] = Field(None, alias="displayName")
    email_address: Optional[str] = Field(None, alias="emailAddress")
    avatar_urls: Optional[AvatarUrls] = Field(None, alias="avatarUrls")
    active: Optional[bool] = None
    time_zone: Optional[str] = Field(None, alias="timeZone")

    model_config = {"populate_by_name": True}


class UserDetails(User):
    """用户详细信息 (api/2/myself 返回)"""
    locale: Optional[str] = None
    groups: Optional[dict] = None
    application_roles: Optional[dict] = Field(None, alias="applicationRoles")
    expand: Optional[str] = None

    model_config = {"populate_by_name": True}
