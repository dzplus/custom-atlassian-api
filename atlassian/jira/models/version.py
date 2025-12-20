"""
Version Models - 版本相关数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field

from atlassian.jira.models.user import User


class Version(BaseModel):
    """
    项目版本模型
    """
    id: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    name: Optional[str] = None
    description: Optional[str] = None
    archived: Optional[bool] = None
    released: Optional[bool] = None
    start_date: Optional[str] = Field(None, alias="startDate")
    release_date: Optional[str] = Field(None, alias="releaseDate")
    overdue: Optional[bool] = None
    user_start_date: Optional[str] = Field(None, alias="userStartDate")
    user_release_date: Optional[str] = Field(None, alias="userReleaseDate")
    project: Optional[str] = None
    project_id: Optional[int] = Field(None, alias="projectId")
    move_unfixed_issues_to: Optional[str] = Field(None, alias="moveUnfixedIssuesTo")
    operations: Optional[list[dict]] = None
    issues_status_for_fix_version: Optional[dict] = Field(None, alias="issuesStatusForFixVersion")

    model_config = {"populate_by_name": True}


class VersionRemoteLink(BaseModel):
    """
    版本远程链接模型
    """
    self_url: Optional[str] = Field(None, alias="self")
    global_id: Optional[str] = Field(None, alias="globalId")
    application_type: Optional[str] = Field(None, alias="applicationType")
    application_name: Optional[str] = Field(None, alias="applicationName")
    relationship: Optional[str] = None
    object: Optional[dict] = None

    model_config = {"populate_by_name": True}


class VersionIssueCounts(BaseModel):
    """
    版本关联的Issue计数
    """
    issue_count: Optional[int] = Field(None, alias="issueCount")
    issues_fixed_count: Optional[int] = Field(None, alias="issuesFixedCount")
    issues_affected_count: Optional[int] = Field(None, alias="issuesAffectedCount")

    model_config = {"populate_by_name": True}


class VersionUnresolvedIssueCount(BaseModel):
    """
    版本未解决的Issue计数
    """
    issues_unresolved_count: Optional[int] = Field(None, alias="issuesUnresolvedCount")
    issues_count: Optional[int] = Field(None, alias="issuesCount")

    model_config = {"populate_by_name": True}
