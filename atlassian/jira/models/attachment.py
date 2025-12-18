"""
Attachment Models - 附件相关数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field

from atlassian.jira.models.user import User


class Attachment(BaseModel):
    """附件信息"""
    id: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    filename: Optional[str] = None
    author: Optional[User] = None
    created: Optional[str] = None
    size: Optional[int] = None
    mime_type: Optional[str] = Field(None, alias="mimeType")
    content: Optional[str] = None  # 下载 URL
    thumbnail: Optional[str] = None  # 缩略图 URL

    model_config = {"populate_by_name": True}


class AttachmentMeta(BaseModel):
    """附件配置信息"""
    enabled: bool
    upload_limit: int = Field(alias="uploadLimit")

    model_config = {"populate_by_name": True}


class ArchiveEntry(BaseModel):
    """归档文件条目"""
    entry_index: Optional[int] = Field(None, alias="entryIndex")
    name: Optional[str] = None
    size: Optional[int] = None
    media_type: Optional[str] = Field(None, alias="mediaType")

    model_config = {"populate_by_name": True}


class ExpandedArchive(BaseModel):
    """展开的归档内容"""
    total_entry_count: int = Field(alias="totalEntryCount")
    entries: list[ArchiveEntry]

    model_config = {"populate_by_name": True}
