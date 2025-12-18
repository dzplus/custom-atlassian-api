"""
Custom Field Models - 自定义字段相关数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field


class CustomField(BaseModel):
    """自定义字段"""
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    search_key: Optional[str] = Field(None, alias="searchKey")
    project_ids: Optional[list[int]] = Field(None, alias="projectIds")
    screens_count: Optional[int] = Field(None, alias="screensCount")

    model_config = {"populate_by_name": True}


class CustomFieldsResponse(BaseModel):
    """自定义字段列表响应（分页）"""
    start_at: int = Field(alias="startAt")
    max_results: int = Field(alias="maxResults")
    total: int
    values: list[CustomField]

    model_config = {"populate_by_name": True}
