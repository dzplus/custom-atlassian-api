"""
Component Models - 组件相关数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field

from atlassian.jira.models.user import User


class Component(BaseModel):
    """
    项目组件模型
    """
    id: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    name: Optional[str] = None
    description: Optional[str] = None
    lead: Optional[User] = None
    lead_user_name: Optional[str] = Field(None, alias="leadUserName")
    assignee_type: Optional[str] = Field(None, alias="assigneeType")
    assignee: Optional[User] = None
    real_assignee_type: Optional[str] = Field(None, alias="realAssigneeType")
    real_assignee: Optional[User] = Field(None, alias="realAssignee")
    is_assignee_type_valid: Optional[bool] = Field(None, alias="isAssigneeTypeValid")
    project: Optional[str] = None
    project_id: Optional[int] = Field(None, alias="projectId")

    model_config = {"populate_by_name": True}


class ComponentIssueCounts(BaseModel):
    """
    组件关联的Issue计数
    """
    issue_count: Optional[int] = Field(None, alias="issueCount")

    model_config = {"populate_by_name": True}
