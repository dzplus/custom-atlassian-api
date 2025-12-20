"""
Issue Models - Issue 相关数据模型
"""

from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from atlassian.jira.models.user import User


class StatusCategory(BaseModel):
    """状态分类"""
    self_url: Optional[str] = Field(None, alias="self")
    id: Optional[int] = None
    key: Optional[str] = None
    color_name: Optional[str] = Field(None, alias="colorName")
    name: Optional[str] = None

    model_config = {"populate_by_name": True}


class Status(BaseModel):
    """Issue 状态"""
    self_url: Optional[str] = Field(None, alias="self")
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = Field(None, alias="iconUrl")
    status_category: Optional[StatusCategory] = Field(None, alias="statusCategory")

    model_config = {"populate_by_name": True}


class Priority(BaseModel):
    """Issue 优先级"""
    self_url: Optional[str] = Field(None, alias="self")
    id: Optional[str] = None
    name: Optional[str] = None
    icon_url: Optional[str] = Field(None, alias="iconUrl")

    model_config = {"populate_by_name": True}


class Resolution(BaseModel):
    """Issue 解决方案"""
    self_url: Optional[str] = Field(None, alias="self")
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

    model_config = {"populate_by_name": True}


class IssueType(BaseModel):
    """Issue 类型"""
    self_url: Optional[str] = Field(None, alias="self")
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = Field(None, alias="iconUrl")
    subtask: Optional[bool] = None
    avatar_id: Optional[int] = Field(None, alias="avatarId")

    model_config = {"populate_by_name": True}


class IssueFields(BaseModel):
    """Issue 字段"""
    summary: Optional[str] = None
    description: Optional[str] = None
    issuetype: Optional[IssueType] = None
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    resolution: Optional[Resolution] = None
    assignee: Optional[User] = None
    reporter: Optional[User] = None
    creator: Optional[User] = None
    created: Optional[str] = None
    updated: Optional[str] = None
    resolved: Optional[str] = Field(None, alias="resolutiondate")
    due_date: Optional[str] = Field(None, alias="duedate")
    labels: Optional[list[str]] = None
    components: Optional[list[dict]] = None
    fix_versions: Optional[list[dict]] = Field(None, alias="fixVersions")
    versions: Optional[list[dict]] = None
    parent: Optional[dict] = None
    subtasks: Optional[list[dict]] = None
    issuelinks: Optional[list[dict]] = None
    attachment: Optional[list[dict]] = None
    comment: Optional[dict] = None
    worklog: Optional[dict] = None
    project: Optional[dict] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class Issue(BaseModel):
    """Issue 完整信息"""
    id: Optional[str] = None
    key: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    expand: Optional[str] = None
    fields: Optional[IssueFields] = None
    rendered_fields: Optional[dict] = Field(None, alias="renderedFields")
    names: Optional[dict] = None
    schema_: Optional[dict] = Field(None, alias="schema")
    transitions: Optional[list[dict]] = None
    operations: Optional[dict] = None
    editmeta: Optional[dict] = None
    changelog: Optional[dict] = None

    model_config = {"populate_by_name": True}


class IssueTransition(BaseModel):
    """Issue 转换"""
    id: Optional[str] = None
    name: Optional[str] = None
    to: Optional[Status] = None
    has_screen: Optional[bool] = Field(None, alias="hasScreen")
    is_global: Optional[bool] = Field(None, alias="isGlobal")
    is_initial: Optional[bool] = Field(None, alias="isInitial")
    is_conditional: Optional[bool] = Field(None, alias="isConditional")
    fields: Optional[dict] = None

    model_config = {"populate_by_name": True}


class IssueComment(BaseModel):
    """Issue 评论"""
    id: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    author: Optional[User] = None
    body: Optional[str] = None
    update_author: Optional[User] = Field(None, alias="updateAuthor")
    created: Optional[str] = None
    updated: Optional[str] = None
    visibility: Optional[dict] = None

    model_config = {"populate_by_name": True}


class IssueComments(BaseModel):
    """Issue 评论列表"""
    start_at: Optional[int] = Field(None, alias="startAt")
    max_results: Optional[int] = Field(None, alias="maxResults")
    total: Optional[int] = None
    comments: Optional[list[IssueComment]] = None

    model_config = {"populate_by_name": True}


class CreateIssueRequest(BaseModel):
    """创建 Issue 请求"""
    fields: dict
    update: Optional[dict] = None

    model_config = {"populate_by_name": True}


class CreateIssueResponse(BaseModel):
    """创建 Issue 响应"""
    id: str
    key: str
    self_url: str = Field(alias="self")

    model_config = {"populate_by_name": True}


class UpdateIssueRequest(BaseModel):
    """更新 Issue 请求"""
    fields: Optional[dict] = None
    update: Optional[dict] = None

    model_config = {"populate_by_name": True}


class Worklog(BaseModel):
    """工作日志"""
    id: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    author: Optional[User] = None
    update_author: Optional[User] = Field(None, alias="updateAuthor")
    comment: Optional[str] = None
    created: Optional[str] = None
    updated: Optional[str] = None
    started: Optional[str] = None
    time_spent: Optional[str] = Field(None, alias="timeSpent")
    time_spent_seconds: Optional[int] = Field(None, alias="timeSpentSeconds")
    visibility: Optional[dict] = None

    model_config = {"populate_by_name": True}


class WorklogList(BaseModel):
    """工作日志列表"""
    start_at: Optional[int] = Field(None, alias="startAt")
    max_results: Optional[int] = Field(None, alias="maxResults")
    total: Optional[int] = None
    worklogs: Optional[list[Worklog]] = None

    model_config = {"populate_by_name": True}


class Watchers(BaseModel):
    """监视者"""
    self_url: Optional[str] = Field(None, alias="self")
    is_watching: Optional[bool] = Field(None, alias="isWatching")
    watch_count: Optional[int] = Field(None, alias="watchCount")
    watchers: Optional[list[User]] = None

    model_config = {"populate_by_name": True}


class Votes(BaseModel):
    """投票"""
    self_url: Optional[str] = Field(None, alias="self")
    votes: Optional[int] = None
    has_voted: Optional[bool] = Field(None, alias="hasVoted")
    voters: Optional[list[User]] = None

    model_config = {"populate_by_name": True}


class RemoteObject(BaseModel):
    """远程对象"""
    url: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    icon: Optional[dict] = None
    status: Optional[dict] = None

    model_config = {"populate_by_name": True}


class RemoteLink(BaseModel):
    """远程链接"""
    id: Optional[int] = None
    self_url: Optional[str] = Field(None, alias="self")
    global_id: Optional[str] = Field(None, alias="globalId")
    application: Optional[dict] = None
    relationship: Optional[str] = None
    object: Optional[RemoteObject] = None

    model_config = {"populate_by_name": True}


class EditMeta(BaseModel):
    """编辑Issue元数据"""
    fields: Optional[dict] = None

    model_config = {"populate_by_name": True}


class CreateMeta(BaseModel):
    """创建Issue元数据"""
    expand: Optional[str] = None
    projects: Optional[list[dict]] = None

    model_config = {"populate_by_name": True}


class IssuePickerSuggestion(BaseModel):
    """Issue选择器建议项"""
    id: Optional[int] = None
    key: Optional[str] = None
    key_html: Optional[str] = Field(None, alias="keyHtml")
    img: Optional[str] = None
    summary: Optional[str] = None
    summary_text: Optional[str] = Field(None, alias="summaryText")

    model_config = {"populate_by_name": True}


class IssuePickerSection(BaseModel):
    """Issue选择器分组"""
    label: Optional[str] = None
    sub: Optional[str] = None
    id: Optional[str] = None
    msg: Optional[str] = None
    issues: Optional[list[IssuePickerSuggestion]] = None

    model_config = {"populate_by_name": True}


class IssuePickerResults(BaseModel):
    """Issue选择器结果"""
    sections: Optional[list[IssuePickerSection]] = None

    model_config = {"populate_by_name": True}
