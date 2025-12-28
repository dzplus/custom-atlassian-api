"""
Tempo Worklog 数据模型
"""

from datetime import date
from typing import Any, Optional
from pydantic import BaseModel, Field


class WorklogAttributes(BaseModel):
    """工时记录属性"""
    key: Optional[str] = Field(None, alias="_key_")
    value: Optional[Any] = None


class WorklogIssue(BaseModel):
    """工时记录关联的 Issue 信息"""
    key: str
    id: int
    summary: Optional[str] = None

    class Config:
        extra = "allow"  # 允许额外字段


class Worklog(BaseModel):
    """工时记录"""
    id: int = Field(alias="tempoWorklogId")
    jira_worklog_id: Optional[int] = Field(None, alias="jiraWorklogId")
    issue: WorklogIssue  # Issue 对象
    time_spent_seconds: int = Field(alias="timeSpentSeconds")
    billable_seconds: Optional[int] = Field(None, alias="billableSeconds")
    started: str  # ISO date string "2024-01-15"
    started_time: Optional[str] = Field(None, alias="startTime")  # "09:00:00"
    description: Optional[str] = Field(None, alias="comment")
    worker: str  # user key
    author: Optional[str] = None

    # 关联信息
    origin_task_id: Optional[int] = Field(None, alias="originTaskId")  # 实际是 int
    origin_id: Optional[int] = Field(None, alias="originId")

    # 属性
    attributes: Optional[dict] = Field(default_factory=dict)

    @property
    def issue_key(self) -> str:
        """获取 Issue Key（兼容性属性）"""
        return self.issue.key if isinstance(self.issue, WorklogIssue) else str(self.issue)

    class Config:
        populate_by_name = True
        extra = "allow"  # 允许额外字段


class WorklogCreate(BaseModel):
    """创建工时记录参数"""
    issue_key: str = Field(alias="originTaskId")
    worker: str  # user key
    started: str  # "2024-01-15"
    time_spent_seconds: int = Field(alias="timeSpentSeconds")
    billable_seconds: Optional[int] = Field(None, alias="billableSeconds")
    description: Optional[str] = Field(None, alias="comment")
    started_time: Optional[str] = Field(None, alias="startTime")

    # 可选属性
    attributes: Optional[dict] = None

    class Config:
        populate_by_name = True

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式"""
        data = {
            "originTaskId": self.issue_key,
            "worker": self.worker,
            "started": self.started,
            "timeSpentSeconds": self.time_spent_seconds,
        }
        if self.billable_seconds is not None:
            data["billableSeconds"] = self.billable_seconds
        if self.description:
            data["comment"] = self.description
        if self.started_time:
            data["startTime"] = self.started_time
        if self.attributes:
            data["attributes"] = self.attributes
        return data


class WorklogUpdate(BaseModel):
    """更新工时记录参数"""
    started: Optional[str] = None
    time_spent_seconds: Optional[int] = Field(None, alias="timeSpentSeconds")
    billable_seconds: Optional[int] = Field(None, alias="billableSeconds")
    description: Optional[str] = Field(None, alias="comment")
    started_time: Optional[str] = Field(None, alias="startTime")
    attributes: Optional[dict] = None

    class Config:
        populate_by_name = True

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式"""
        data = {}
        if self.started:
            data["started"] = self.started
        if self.time_spent_seconds is not None:
            data["timeSpentSeconds"] = self.time_spent_seconds
        if self.billable_seconds is not None:
            data["billableSeconds"] = self.billable_seconds
        if self.description is not None:
            data["comment"] = self.description
        if self.started_time:
            data["startTime"] = self.started_time
        if self.attributes:
            data["attributes"] = self.attributes
        return data


class WorklogSearchParams(BaseModel):
    """工时记录搜索参数

    API 文档参考：POST /rest/tempo-timesheets/4/worklogs/search

    注意：
    - taskId 必须使用整数 ID，不能使用字符串 key
    - taskKey 可以使用字符串 key（如 "NF-433"）
    """
    from_date: str = Field(alias="from")  # "2024-01-01"
    to_date: str = Field(alias="to")  # "2024-01-31"
    worker: Optional[list[str]] = None  # user keys
    task_id: Optional[list[int]] = Field(None, alias="taskId")  # issue 数字 ID
    task_key: Optional[list[str]] = Field(None, alias="taskKey")  # issue key (如 "NF-433")
    project_id: Optional[list[int]] = Field(None, alias="projectId")
    project_key: Optional[list[str]] = Field(None, alias="projectKey")
    team_id: Optional[list[int]] = Field(None, alias="teamId")
    role_id: Optional[list[int]] = Field(None, alias="roleId")
    account_id: Optional[list[int]] = Field(None, alias="accountId")
    account_key: Optional[list[str]] = Field(None, alias="accountKey")
    filter_id: Optional[list[int]] = Field(None, alias="filterId")
    customer_id: Optional[list[int]] = Field(None, alias="customerId")
    category_id: Optional[list[int]] = Field(None, alias="categoryId")
    category_type_id: Optional[list[int]] = Field(None, alias="categoryTypeId")
    epic_key: Optional[list[str]] = Field(None, alias="epicKey")
    location_ids: Optional[list[int]] = Field(None, alias="locationIds")
    include_subtasks: Optional[bool] = Field(None, alias="includeSubtasks")

    class Config:
        populate_by_name = True

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式"""
        data = {
            "from": self.from_date,
            "to": self.to_date,
        }
        if self.worker:
            data["worker"] = self.worker
        if self.task_id:
            data["taskId"] = self.task_id
        if self.task_key:
            data["taskKey"] = self.task_key
        if self.project_id:
            data["projectId"] = self.project_id
        if self.project_key:
            data["projectKey"] = self.project_key
        if self.team_id:
            data["teamId"] = self.team_id
        if self.role_id:
            data["roleId"] = self.role_id
        if self.account_id:
            data["accountId"] = self.account_id
        if self.account_key:
            data["accountKey"] = self.account_key
        if self.filter_id:
            data["filterId"] = self.filter_id
        if self.customer_id:
            data["customerId"] = self.customer_id
        if self.category_id:
            data["categoryId"] = self.category_id
        if self.category_type_id:
            data["categoryTypeId"] = self.category_type_id
        if self.epic_key:
            data["epicKey"] = self.epic_key
        if self.location_ids:
            data["locationIds"] = self.location_ids
        if self.include_subtasks is not None:
            data["includeSubtasks"] = self.include_subtasks
        return data
