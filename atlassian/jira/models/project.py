"""
Project Models - 项目相关数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field

from atlassian.jira.models.user import User, AvatarUrls


class ProjectCategory(BaseModel):
    """项目分类"""
    id: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    name: Optional[str] = None
    description: Optional[str] = None

    model_config = {"populate_by_name": True}


class ProjectComponent(BaseModel):
    """项目组件"""
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


class ProjectVersion(BaseModel):
    """项目版本"""
    id: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    name: Optional[str] = None
    description: Optional[str] = None
    archived: Optional[bool] = None
    released: Optional[bool] = None
    release_date: Optional[str] = Field(None, alias="releaseDate")
    overdue: Optional[bool] = None
    user_release_date: Optional[str] = Field(None, alias="userReleaseDate")
    project_id: Optional[int] = Field(None, alias="projectId")

    model_config = {"populate_by_name": True}


class Project(BaseModel):
    """项目信息"""
    id: Optional[str] = None
    key: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    name: Optional[str] = None
    description: Optional[str] = None
    lead: Optional[User] = None
    avatar_urls: Optional[AvatarUrls] = Field(None, alias="avatarUrls")
    project_category: Optional[ProjectCategory] = Field(None, alias="projectCategory")
    project_type_key: Optional[str] = Field(None, alias="projectTypeKey")
    simplified: Optional[bool] = None
    style: Optional[str] = None
    expand: Optional[str] = None
    components: Optional[list[ProjectComponent]] = None
    versions: Optional[list[ProjectVersion]] = None
    issue_types: Optional[list[dict]] = Field(None, alias="issueTypes")
    roles: Optional[dict] = None

    model_config = {"populate_by_name": True}


class StatusCategory(BaseModel):
    """状态分类"""
    self_url: Optional[str] = Field(None, alias="self")
    id: Optional[int] = None
    key: Optional[str] = None
    color_name: Optional[str] = Field(None, alias="colorName")
    name: Optional[str] = None

    model_config = {"populate_by_name": True}


class IssueTypeStatus(BaseModel):
    """Issue 类型下的状态"""
    self_url: Optional[str] = Field(None, alias="self")
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = Field(None, alias="iconUrl")
    status_category: Optional[StatusCategory] = Field(None, alias="statusCategory")

    model_config = {"populate_by_name": True}


class ProjectIssueTypeStatuses(BaseModel):
    """
    项目中某个 Issue 类型的状态列表

    来自 GET /rest/api/2/project/{projectIdOrKey}/statuses
    返回项目中每个 Issue 类型对应的工作流状态
    """
    self_url: Optional[str] = Field(None, alias="self")
    id: Optional[str] = None
    name: Optional[str] = None
    subtask: Optional[bool] = None
    statuses: Optional[list[IssueTypeStatus]] = None

    model_config = {"populate_by_name": True}


class ProjectStatus(BaseModel):
    """项目状态（用于特定 issue type）- 已废弃，请使用 ProjectIssueTypeStatuses"""
    self_url: Optional[str] = Field(None, alias="self")
    id: Optional[str] = None
    name: Optional[str] = None
    subtask: Optional[bool] = None
    statuses: Optional[list[dict]] = None

    model_config = {"populate_by_name": True}
