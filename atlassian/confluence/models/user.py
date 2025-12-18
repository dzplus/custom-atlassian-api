"""
User Models - Confluence 用户相关数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field


class ProfilePicture(BaseModel):
    """用户头像"""
    path: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    is_default: Optional[bool] = Field(None, alias="isDefault")

    model_config = {"populate_by_name": True}


class User(BaseModel):
    """Confluence 用户"""
    type: Optional[str] = None
    username: Optional[str] = None
    user_key: Optional[str] = Field(None, alias="userKey")
    account_id: Optional[str] = Field(None, alias="accountId")
    profile_picture: Optional[ProfilePicture] = Field(None, alias="profilePicture")
    display_name: Optional[str] = Field(None, alias="displayName")
    _links: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class UserWatch(BaseModel):
    """用户监视状态"""
    watching: bool = False

    model_config = {"populate_by_name": True}
