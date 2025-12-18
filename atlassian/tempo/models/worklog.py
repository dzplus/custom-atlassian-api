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


class Worklog(BaseModel):
    """工时记录"""
    id: int = Field(alias="tempoWorklogId")
    jira_worklog_id: Optional[int] = Field(None, alias="jiraWorklogId")
    issue_key: str = Field(alias="issue")
    time_spent_seconds: int = Field(alias="timeSpentSeconds")
    billable_seconds: Optional[int] = Field(None, alias="billableSeconds")
    started: str  # ISO date string "2024-01-15"
    started_time: Optional[str] = Field(None, alias="startTime")  # "09:00:00"
    description: Optional[str] = Field(None, alias="comment")
    worker: str  # user key
    author: Optional[str] = None

    # 关联信息
    origin_task_id: Optional[str] = Field(None, alias="originTaskId")
    origin_id: Optional[int] = Field(None, alias="originId")

    # 属性
    attributes: Optional[dict] = Field(default_factory=dict)

    class Config:
        populate_by_name = True


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
    """工时记录搜索参数"""
    from_date: str = Field(alias="from")  # "2024-01-01"
    to_date: str = Field(alias="to")  # "2024-01-31"
    worker: Optional[list[str]] = None  # user keys
    issue_key: Optional[list[str]] = Field(None, alias="taskId")
    project_key: Optional[list[str]] = Field(None, alias="projectKey")
    account_key: Optional[list[str]] = Field(None, alias="accountKey")

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
        if self.issue_key:
            data["taskId"] = self.issue_key
        if self.project_key:
            data["projectKey"] = self.project_key
        if self.account_key:
            data["accountKey"] = self.account_key
        return data
