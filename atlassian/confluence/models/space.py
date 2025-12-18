"""
Space Models - Confluence 空间相关数据模型
"""

from typing import Any, Optional
from pydantic import BaseModel, Field


class SpaceDescription(BaseModel):
    """空间描述"""
    plain: Optional[dict] = None
    view: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class Space(BaseModel):
    """Confluence 空间"""
    id: Optional[int] = None
    key: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    description: Optional[SpaceDescription] = None
    metadata: Optional[dict] = None
    permissions: Optional[list[dict]] = None
    homepage: Optional[dict] = None
    _links: Optional[dict] = None
    _expandable: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class SpaceList(BaseModel):
    """空间列表"""
    results: list[Space] = []
    start: Optional[int] = None
    limit: Optional[int] = None
    size: Optional[int] = None
    _links: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class SpaceProperty(BaseModel):
    """空间属性"""
    id: Optional[str] = None
    key: Optional[str] = None
    value: Optional[Any] = None
    version: Optional[dict] = None
    space: Optional[Space] = None
    _links: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class SpacePropertyList(BaseModel):
    """空间属性列表"""
    results: list[SpaceProperty] = []
    start: Optional[int] = None
    limit: Optional[int] = None
    size: Optional[int] = None
    _links: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}
