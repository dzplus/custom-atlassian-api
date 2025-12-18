"""
Tempo Plan 数据模型

用于资源计划和分配
"""

from typing import Optional
from pydantic import BaseModel, Field


class Allocation(BaseModel):
    """资源分配"""
    id: int
    assignee_key: str = Field(alias="assigneeKey")
    assignee_type: str = Field(alias="assigneeType")  # USER, TEAM
    plan_item_id: str = Field(alias="planItemId")  # Issue key 或其他
    plan_item_type: str = Field(alias="planItemType")  # ISSUE, PROJECT, etc.
    start_date: str = Field(alias="startDate")
    end_date: str = Field(alias="endDate")
    seconds_per_day: int = Field(alias="secondsPerDay")
    include_non_working_days: bool = Field(False, alias="includeNonWorkingDays")
    description: Optional[str] = None
    recurrence_end_date: Optional[str] = Field(None, alias="recurrenceEndDate")

    class Config:
        populate_by_name = True


class AllocationCreate(BaseModel):
    """创建资源分配参数"""
    assignee_key: str = Field(alias="assigneeKey")
    assignee_type: str = Field("USER", alias="assigneeType")
    plan_item_id: str = Field(alias="planItemId")
    plan_item_type: str = Field("ISSUE", alias="planItemType")
    start_date: str = Field(alias="startDate")
    end_date: str = Field(alias="endDate")
    seconds_per_day: int = Field(alias="secondsPerDay")
    include_non_working_days: bool = Field(False, alias="includeNonWorkingDays")
    description: Optional[str] = None
    recurrence_end_date: Optional[str] = Field(None, alias="recurrenceEndDate")

    class Config:
        populate_by_name = True

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式"""
        data = {
            "assigneeKey": self.assignee_key,
            "assigneeType": self.assignee_type,
            "planItemId": self.plan_item_id,
            "planItemType": self.plan_item_type,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "secondsPerDay": self.seconds_per_day,
            "includeNonWorkingDays": self.include_non_working_days,
        }
        if self.description:
            data["description"] = self.description
        if self.recurrence_end_date:
            data["recurrenceEndDate"] = self.recurrence_end_date
        return data


class PlanLog(BaseModel):
    """计划日志条目"""
    id: int
    date: str
    assignee_key: str = Field(alias="assigneeKey")
    plan_item_id: str = Field(alias="planItemId")
    plan_item_type: str = Field(alias="planItemType")
    seconds: int
    description: Optional[str] = None

    class Config:
        populate_by_name = True


class Plan(BaseModel):
    """计划条目"""
    assignee_key: str = Field(alias="assigneeKey")
    assignee_type: str = Field("USER", alias="assigneeType")
    plan_item_id: str = Field(alias="planItemId")
    plan_item_type: str = Field("ISSUE", alias="planItemType")
    start_date: str = Field(alias="startDate")
    end_date: str = Field(alias="endDate")
    seconds_per_day: int = Field(alias="secondsPerDay")
    include_non_working_days: bool = Field(False, alias="includeNonWorkingDays")
    description: Optional[str] = None

    class Config:
        populate_by_name = True

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式"""
        data = {
            "assigneeKey": self.assignee_key,
            "assigneeType": self.assignee_type,
            "planItemId": self.plan_item_id,
            "planItemType": self.plan_item_type,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "secondsPerDay": self.seconds_per_day,
            "includeNonWorkingDays": self.include_non_working_days,
        }
        if self.description:
            data["description"] = self.description
        return data


class PlanSearchParams(BaseModel):
    """计划搜索参数"""
    from_date: str = Field(alias="from")
    to_date: str = Field(alias="to")
    assignee_keys: Optional[list[str]] = Field(None, alias="assigneeKeys")
    plan_item_ids: Optional[list[str]] = Field(None, alias="planItemIds")

    class Config:
        populate_by_name = True

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式"""
        data = {
            "from": self.from_date,
            "to": self.to_date,
        }
        if self.assignee_keys:
            data["assigneeKeys"] = self.assignee_keys
        if self.plan_item_ids:
            data["planItemIds"] = self.plan_item_ids
        return data
