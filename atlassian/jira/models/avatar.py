"""
Avatar Models - 头像相关数据模型

包含头像、系统头像、自定义头像等模型
"""

from typing import Optional
from pydantic import BaseModel, Field


class Avatar(BaseModel):
    """
    头像模型

    用于用户、项目、Issue类型等的头像
    """
    id: Optional[str] = None
    owner: Optional[str] = None
    is_system_avatar: Optional[bool] = Field(None, alias="isSystemAvatar")
    is_selected: Optional[bool] = Field(None, alias="isSelected")
    is_deletable: Optional[bool] = Field(None, alias="isDeletable")
    file_name: Optional[str] = Field(None, alias="fileName")
    urls: Optional[dict[str, str]] = None

    model_config = {"populate_by_name": True}


class SystemAvatar(BaseModel):
    """
    系统头像

    Jira提供的预定义头像
    """
    id: str
    is_system_avatar: bool = Field(True, alias="isSystemAvatar")
    is_selected: Optional[bool] = Field(None, alias="isSelected")
    urls: Optional[dict[str, str]] = None

    model_config = {"populate_by_name": True}


class CustomAvatar(BaseModel):
    """
    自定义头像

    用户上传的头像
    """
    id: str
    owner: Optional[str] = None
    is_system_avatar: bool = Field(False, alias="isSystemAvatar")
    is_selected: Optional[bool] = Field(None, alias="isSelected")
    is_deletable: bool = Field(True, alias="isDeletable")
    file_name: Optional[str] = Field(None, alias="fileName")
    urls: Optional[dict[str, str]] = None

    model_config = {"populate_by_name": True}


class TemporaryAvatar(BaseModel):
    """
    临时头像

    上传但未确认的头像
    """
    crop_instructions: Optional[dict] = Field(None, alias="cropInstructions")

    model_config = {"populate_by_name": True}


class AvatarCropping(BaseModel):
    """
    头像裁剪参数

    定义如何裁剪上传的头像
    """
    crop_x: Optional[int] = Field(None, alias="cropX")
    crop_y: Optional[int] = Field(None, alias="cropY")
    crop_width: Optional[int] = Field(None, alias="cropWidth")
    crop_height: Optional[int] = Field(None, alias="cropHeight")

    model_config = {"populate_by_name": True}


class ProjectAvatar(BaseModel):
    """
    项目头像

    项目专用的头像模型
    """
    id: Optional[str] = None
    owner: Optional[str] = None
    is_system_avatar: Optional[bool] = Field(None, alias="isSystemAvatar")
    is_selected: Optional[bool] = Field(None, alias="isSelected")
    urls: Optional[dict[str, str]] = None

    model_config = {"populate_by_name": True}


class IssueTypeAvatar(BaseModel):
    """
    Issue类型头像

    Issue类型专用的头像模型
    """
    id: Optional[str] = None
    is_system_avatar: Optional[bool] = Field(None, alias="isSystemAvatar")
    is_selected: Optional[bool] = Field(None, alias="isSelected")
    urls: Optional[dict[str, str]] = None

    model_config = {"populate_by_name": True}


class UserAvatar(BaseModel):
    """
    用户头像

    用户专用的头像模型
    """
    id: Optional[str] = None
    owner: Optional[str] = None
    is_system_avatar: Optional[bool] = Field(None, alias="isSystemAvatar")
    is_selected: Optional[bool] = Field(None, alias="isSelected")
    is_deletable: Optional[bool] = Field(None, alias="isDeletable")
    urls: Optional[dict[str, str]] = None

    model_config = {"populate_by_name": True}
