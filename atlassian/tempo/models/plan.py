"""
Tempo Plan 数据模型

用于资源计划和分配
"""

from typing import Optional, Union
from pydantic import BaseModel, Field, field_validator


class Allocation(BaseModel):
    """资源分配"""
    id: int
    # 所有字段改为可选，因为实际 API 返回的字段结构可能不同
    assignee_key: Optional[str] = Field(None, alias="assigneeKey")
    assignee_type: Optional[str] = Field(None, alias="assigneeType")  # USER, TEAM
    plan_item_id: Optional[str] = Field(None, alias="planItemId")  # Issue key 或其他
    plan_item_type: Optional[str] = Field(None, alias="planItemType")  # ISSUE, PROJECT, etc.
    start_date: Optional[str] = Field(None, alias="startDate")
    end_date: Optional[str] = Field(None, alias="endDate")
    seconds_per_day: Optional[int] = Field(None, alias="secondsPerDay")
    include_non_working_days: Optional[bool] = Field(None, alias="includeNonWorkingDays")
    description: Optional[str] = None
    recurrence_end_date: Optional[str] = Field(None, alias="recurrenceEndDate")

    # 可能出现的其他字段
    assignee: Optional[dict] = None
    plan_item: Optional[dict] = Field(None, alias="planItem")
    recurrence: Optional[dict] = None

    class Config:
        populate_by_name = True
        extra = "allow"  # 允许额外字段


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
    # 所有字段改为可选，因为实际 API 返回的字段结构可能不同
    id: Optional[int] = None
    allocation_id: Optional[int] = Field(None, alias="allocationId")
    date: Optional[str] = None
    assignee_key: Optional[str] = Field(None, alias="assigneeKey")
    plan_item_id: Optional[Union[str, int]] = Field(None, alias="planItemId")  # 可以是字符串或整数
    plan_item_type: Optional[str] = Field(None, alias="planItemType")
    seconds: Optional[int] = None
    description: Optional[str] = None

    # 可能出现的其他字段
    assignee: Optional[Union[str, dict]] = None  # 可以是字符串或字典
    plan_item: Optional[Union[str, int, dict]] = Field(None, alias="planItem")  # 可以是字符串、整数或字典

    @field_validator('assignee', mode='before')
    @classmethod
    def validate_assignee(cls, v):
        """验证 assignee 字段，如果是字符串则转换为字典"""
        if isinstance(v, str):
            return {"key": v}
        return v

    @field_validator('plan_item', mode='before')
    @classmethod
    def validate_plan_item(cls, v):
        """验证 plan_item 字段"""
        if isinstance(v, (str, int)):
            return {"id": v}
        return v

    class Config:
        populate_by_name = True
        extra = "allow"  # 允许额外字段


class Plan(BaseModel):
    """计划条目"""
    assignee_key: str = Field(alias="assigneeKey")
    plan_item_id: int = Field(alias="planItemId")  # 必须是整数
    plan_item_type: str = Field("ISSUE", alias="planItemType")
    day: str  # 必需字段：当前日期
    start: str  # 开始日期
    end: str  # 结束日期
    start_time: str = Field("09:00", alias="startTime")  # 开始时间，默认 09:00
    seconds_per_day: int = Field(alias="secondsPerDay")
    include_non_working_days: bool = Field(False, alias="includeNonWorkingDays")
    allocation_id: Optional[int] = Field(None, alias="allocationId")  # 更新时必需
    description: Optional[str] = None
    plan_approval: Optional[str] = Field(None, alias="planApproval")

    class Config:
        populate_by_name = True

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式"""
        data = {
            "assigneeKey": self.assignee_key,
            "planItemId": self.plan_item_id,
            "planItemType": self.plan_item_type,
            "day": self.day,
            "start": self.start,
            "end": self.end,
            "startTime": self.start_time,
            "secondsPerDay": self.seconds_per_day,
            "includeNonWorkingDays": self.include_non_working_days,
        }
        if self.allocation_id is not None:
            data["allocationId"] = self.allocation_id
        if self.description:
            data["description"] = self.description
        if self.plan_approval is not None:
            data["planApproval"] = self.plan_approval
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
