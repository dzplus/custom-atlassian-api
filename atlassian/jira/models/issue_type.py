"""
Issue Type Models - Issue类型相关数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field


class IssueTypeScheme(BaseModel):
    """
    Issue类型方案模型
    """
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    default_issue_type_id: Optional[str] = Field(None, alias="defaultIssueTypeId")
    is_default: Optional[bool] = Field(None, alias="isDefault")

    model_config = {"populate_by_name": True}


class IssueTypeSchemeMapping(BaseModel):
    """
    Issue类型方案映射
    """
    issue_type_scheme_id: Optional[str] = Field(None, alias="issueTypeSchemeId")
    issue_type_id: Optional[str] = Field(None, alias="issueTypeId")

    model_config = {"populate_by_name": True}


class IssueTypeSchemeProjects(BaseModel):
    """
    Issue类型方案关联项目
    """
    issue_type_scheme: Optional[IssueTypeScheme] = Field(None, alias="issueTypeScheme")
    project_ids: Optional[list[str]] = Field(None, alias="projectIds")

    model_config = {"populate_by_name": True}


class PriorityScheme(BaseModel):
    """
    优先级方案模型
    """
    id: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    name: Optional[str] = None
    description: Optional[str] = None
    default_option_id: Optional[str] = Field(None, alias="defaultOptionId")
    option_ids: Optional[list[str]] = Field(None, alias="optionIds")

    model_config = {"populate_by_name": True}
