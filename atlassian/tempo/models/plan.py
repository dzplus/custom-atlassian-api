"""
Tempo Plan 数据模型

用于资源计划和分配
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# ========== 嵌套对象模型 ==========


class Assignee(BaseModel):
    """分配人信息"""
    model_config = ConfigDict(populate_by_name=True)

    key: str
    type: str
    user_key: Optional[str] = Field(None, alias="userKey")


class IssueStatus(BaseModel):
    """Issue 状态"""
    name: str
    color: str


class EpicIssue(BaseModel):
    """Epic Issue 信息"""
    model_config = ConfigDict(populate_by_name=True)

    summary: str
    icon_url: str = Field(alias="iconUrl")
    estimated_remaining_seconds: Optional[int] = Field(None, alias="estimatedRemainingSeconds")


class PlanItem(BaseModel):
    """计划项信息"""
    model_config = ConfigDict(populate_by_name=True)

    key: str
    id: int
    type: str
    name: str
    summary: str
    description: Optional[str] = None
    icon_name: Optional[str] = Field(None, alias="iconName")
    icon_url: Optional[str] = Field(None, alias="iconUrl")
    project_key: Optional[str] = Field(None, alias="projectKey")
    project_id: Optional[int] = Field(None, alias="projectId")
    plan_item_url: Optional[str] = Field(None, alias="planItemUrl")
    is_resolved: Optional[bool] = Field(None, alias="isResolved")
    issue_status: Optional[IssueStatus] = Field(None, alias="issueStatus")
    estimated_remaining_seconds: Optional[int] = Field(None, alias="estimatedRemainingSeconds")
    original_estimate_seconds: Optional[int] = Field(None, alias="originalEstimateSeconds")
    epic_key: Optional[str] = Field(None, alias="epicKey")
    epic_issue: Optional[EpicIssue] = Field(None, alias="epicIssue")


class Scope(BaseModel):
    """范围信息"""
    id: int
    type: str


class Recurrence(BaseModel):
    """重复规则"""
    model_config = ConfigDict(populate_by_name=True)

    end_date: Optional[str] = Field(None, alias="endDate")
    rule: str


class Location(BaseModel):
    """位置信息"""
    id: int
    name: str


# ========== 主要模型 ==========


class Allocation(BaseModel):
    """资源分配（从 API 响应解析）"""
    model_config = ConfigDict(populate_by_name=True)

    id: int
    assignee: Assignee
    plan_item: PlanItem = Field(alias="planItem")
    scope: Optional[Scope] = None
    commitment: Optional[float] = None
    seconds_per_day: int = Field(alias="secondsPerDay")
    include_non_working_days: bool = Field(False, alias="includeNonWorkingDays")
    start: str  # "2024-01-01"
    start_time: Optional[str] = Field(None, alias="startTime")
    end: str  # "2024-01-31"
    description: Optional[str] = None
    seconds: Optional[int] = None
    created: Optional[str] = None
    created_by: Optional[str] = Field(None, alias="createdBy")
    created_by_key: Optional[str] = Field(None, alias="createdByKey")
    updated: Optional[str] = None
    updated_by: Optional[str] = Field(None, alias="updatedBy")
    recurrence: Optional[Recurrence] = None

    # 便捷属性
    @property
    def assignee_key(self) -> str:
        return self.assignee.key

    @property
    def assignee_type(self) -> str:
        return self.assignee.type

    @property
    def plan_item_id(self) -> str:
        return self.plan_item.key

    @property
    def plan_item_type(self) -> str:
        return self.plan_item.type

    @property
    def start_date(self) -> str:
        return self.start

    @property
    def end_date(self) -> str:
        return self.end


class AllocationCreate(BaseModel):
    """创建资源分配参数"""
    model_config = ConfigDict(populate_by_name=True)

    assignee_key: str = Field(alias="assigneeKey")
    assignee_type: str = Field("USER", alias="assigneeType")
    plan_item_id: int = Field(alias="planItemId")  # 必须是 Issue 的数字 ID
    plan_item_type: str = Field("ISSUE", alias="planItemType")
    start_date: str = Field(alias="startDate")
    end_date: str = Field(alias="endDate")
    seconds_per_day: int = Field(alias="secondsPerDay")
    include_non_working_days: bool = Field(False, alias="includeNonWorkingDays")
    description: Optional[str] = None
    recurrence_end_date: Optional[str] = Field(None, alias="recurrenceEndDate")
    # scope 字段 - API 要求必须提供
    scope_id: Optional[int] = Field(None, alias="scopeId")
    scope_type: str = Field("none", alias="scopeType")  # 默认 "none"

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式（符合 Tempo Planner OpenAPI 规范）"""
        data = {
            # 必填字段
            "start": self.start_date,
            "end": self.end_date,
            "secondsPerDay": self.seconds_per_day,
            # assignee 嵌套对象
            "assignee": {
                "key": self.assignee_key,
                "type": self.assignee_type,
            },
            # planItem 嵌套对象
            "planItem": {
                "id": self.plan_item_id,
                "type": self.plan_item_type,
            },
            # scope 嵌套对象 - 使用 planItem.id 作为 scope.id
            "scope": {
                "id": self.scope_id if self.scope_id else self.plan_item_id,
                "type": self.scope_type,
            },
            "includeNonWorkingDays": self.include_non_working_days,
        }
        if self.description:
            data["description"] = self.description
        if self.recurrence_end_date:
            data["recurrence"] = {
                "endDate": self.recurrence_end_date,
                "rule": "NEVER",
            }
        return data


class PlanLog(BaseModel):
    """计划日志条目（从 API 响应解析）"""
    model_config = ConfigDict(populate_by_name=True)

    allocation_id: int = Field(alias="allocationId")
    assignee: str  # user key
    assignee_type: str = Field(alias="assigneeType")
    plan_item_id: int = Field(alias="planItemId")
    plan_item_type: str = Field(alias="planItemType")
    plan_item_info: Optional[PlanItem] = Field(None, alias="planItemInfo")
    plan_description: Optional[str] = Field(None, alias="planDescription")
    day: str  # "2024-01-15"
    time_planned_seconds: float = Field(alias="timePlannedSeconds")
    seconds_per_day: int = Field(alias="secondsPerDay")
    include_non_working_days: bool = Field(False, alias="includeNonWorkingDays")
    plan_creator: Optional[str] = Field(None, alias="planCreator")
    date_created: Optional[str] = Field(None, alias="dateCreated")
    date_updated: Optional[str] = Field(None, alias="dateUpdated")
    plan_start: Optional[str] = Field(None, alias="planStart")
    plan_start_time: Optional[str] = Field(None, alias="planStartTime")
    plan_end: Optional[str] = Field(None, alias="planEnd")
    location: Optional[Location] = None

    # 便捷属性（兼容旧代码）
    @property
    def id(self) -> int:
        return self.allocation_id

    @property
    def date(self) -> str:
        return self.day

    @property
    def assignee_key(self) -> str:
        return self.assignee

    @property
    def seconds(self) -> int:
        return int(self.time_planned_seconds)

    @property
    def description(self) -> Optional[str]:
        return self.plan_description


class Plan(BaseModel):
    """计划条目（用于创建/更新）"""
    model_config = ConfigDict(populate_by_name=True)

    assignee_key: str = Field(alias="assigneeKey")
    plan_item_id: int = Field(alias="planItemId")  # 内部使用 int，API 会转为字符串
    plan_item_type: str = Field("ISSUE", alias="planItemType")
    start_date: str = Field(alias="startDate")  # "yyyy-MM-dd"
    end_date: str = Field(alias="endDate")  # "yyyy-MM-dd"
    start_time: str = Field("09:00", alias="startTime")  # "HH:MM"
    seconds_per_day: int = Field(alias="secondsPerDay")
    include_non_working_days: bool = Field(True, alias="includeNonWorkingDays")  # 默认 True
    description: Optional[str] = None
    allocation_id: Optional[int] = Field(None, alias="allocationId")  # 更新时需要

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式（符合 Tempo Planner 实际调用格式）"""
        data = {
            "planItemType": self.plan_item_type,
            "planItemId": str(self.plan_item_id),  # API 需要字符串
            "planApproval": None,
            "start": self.start_date,
            "end": self.end_date,
            "day": self.start_date,  # API 要求 day 字段
            "assigneeKey": self.assignee_key,
            "includeNonWorkingDays": self.include_non_working_days,
            "secondsPerDay": self.seconds_per_day,
            "startTime": self.start_time,
        }
        if self.description:
            data["description"] = self.description
        if self.allocation_id:
            data["allocationId"] = self.allocation_id
        return data


class PlanSearchParams(BaseModel):
    """计划搜索参数

    API 文档参考：POST /rest/tempo-planning/1/plan/search (PlanSearchBean)
    """
    model_config = ConfigDict(populate_by_name=True)

    from_date: str = Field(alias="from")
    to_date: str = Field(alias="to")
    worker: Optional[list[str]] = None  # user keys
    task_id: Optional[list[int]] = Field(None, alias="taskId")  # issue 数字 ID
    task_key: Optional[list[str]] = Field(None, alias="taskKey")  # issue key
    include_subtasks: Optional[bool] = Field(None, alias="includeSubtasks")
    project_id: Optional[list[int]] = Field(None, alias="projectId")
    project_key: Optional[list[str]] = Field(None, alias="projectKey")
    team_id: Optional[list[int]] = Field(None, alias="teamId")
    role_id: Optional[list[int]] = Field(None, alias="roleId")
    epic_key: Optional[list[str]] = Field(None, alias="epicKey")
    location_ids: Optional[list[int]] = Field(None, alias="locationIds")

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式（符合 Tempo Planner OpenAPI 规范）"""
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
        if self.include_subtasks is not None:
            data["includeSubtasks"] = self.include_subtasks
        if self.project_id:
            data["projectId"] = self.project_id
        if self.project_key:
            data["projectKey"] = self.project_key
        if self.team_id:
            data["teamId"] = self.team_id
        if self.role_id:
            data["roleId"] = self.role_id
        if self.epic_key:
            data["epicKey"] = self.epic_key
        if self.location_ids:
            data["locationIds"] = self.location_ids
        return data
