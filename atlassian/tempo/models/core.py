"""
Tempo Core 数据模型

API: /rest/tempo-core/1/

包含:
- Expense: 费用
- ExpenseCategory: 费用分类
- User Schedule: 用户日程
- Work Attribute: 工作属性
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# ========== Expense Category ==========


class ExpenseCategory(BaseModel):
    """费用分类"""
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = None
    name: str


class ExpenseCategoryCreate(BaseModel):
    """创建费用分类"""
    name: str


# ========== Expense ==========


class CreatedBy(BaseModel):
    """创建者信息"""
    model_config = ConfigDict(populate_by_name=True)

    username: str
    display_name: Optional[str] = Field(None, alias="displayName")
    key: Optional[str] = None


class Scope(BaseModel):
    """范围信息"""
    model_config = ConfigDict(populate_by_name=True)

    scope_id: int = Field(alias="scopeId")
    scope_type: str = Field(alias="scopeType")  # ISSUE


class Expense(BaseModel):
    """费用（从 API 响应解析）"""
    model_config = ConfigDict(populate_by_name=True)

    id: int
    description: Optional[str] = None
    date: str  # yyyy-MM-dd
    created_by: Optional[CreatedBy] = Field(None, alias="createdBy")
    scope_type: Optional[str] = Field(None, alias="scopeType")  # ISSUE
    scope_id: Optional[int] = Field(None, alias="scopeId")
    scope: Optional[Scope] = None
    amount: float
    expense_category: Optional[ExpenseCategory] = Field(None, alias="expenseCategory")


class ExpenseCreate(BaseModel):
    """创建费用"""
    model_config = ConfigDict(populate_by_name=True)

    description: Optional[str] = None
    date: str  # yyyy-MM-dd
    scope_id: int = Field(alias="scopeId")
    scope_type: str = Field("ISSUE", alias="scopeType")
    amount: float
    expense_category_id: int = Field(alias="expenseCategoryId")
    created_by_username: Optional[str] = Field(None, alias="createdByUsername")
    created_by_key: Optional[str] = Field(None, alias="createdByKey")

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式"""
        data = {
            "date": self.date,
            "amount": self.amount,
            "scope": {
                "scopeId": self.scope_id,
                "scopeType": self.scope_type,
            },
            "expenseCategory": {
                "id": self.expense_category_id,
            },
        }
        if self.description:
            data["description"] = self.description
        if self.created_by_username or self.created_by_key:
            data["createdBy"] = {}
            if self.created_by_username:
                data["createdBy"]["username"] = self.created_by_username
            if self.created_by_key:
                data["createdBy"]["key"] = self.created_by_key
        return data


class ExpenseUpdate(BaseModel):
    """更新费用"""
    model_config = ConfigDict(populate_by_name=True)

    description: Optional[str] = None
    date: Optional[str] = None
    scope_id: Optional[int] = Field(None, alias="scopeId")
    scope_type: Optional[str] = Field(None, alias="scopeType")
    amount: Optional[float] = None
    expense_category_id: Optional[int] = Field(None, alias="expenseCategoryId")

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式"""
        data = {}
        if self.date:
            data["date"] = self.date
        if self.amount is not None:
            data["amount"] = self.amount
        if self.description:
            data["description"] = self.description
        if self.scope_id or self.scope_type:
            data["scope"] = {}
            if self.scope_id:
                data["scope"]["scopeId"] = self.scope_id
            if self.scope_type:
                data["scope"]["scopeType"] = self.scope_type
        if self.expense_category_id:
            data["expenseCategory"] = {"id": self.expense_category_id}
        return data


# ========== User Schedule ==========


class Holiday(BaseModel):
    """假日信息"""
    model_config = ConfigDict(populate_by_name=True)

    name: str
    description: Optional[str] = None
    duration_seconds: Optional[int] = Field(None, alias="durationSeconds")


class DaySchedule(BaseModel):
    """日程条目"""
    model_config = ConfigDict(populate_by_name=True)

    date: str  # yyyy-MM-dd
    required_seconds: int = Field(alias="requiredSeconds")
    type: str  # WORKING_DAY, NON_WORKING_DAY, HOLIDAY, HOLIDAY_AND_NON_WORKING_DAY
    holiday: Optional[Holiday] = None


class UserSchedule(BaseModel):
    """用户日程"""
    model_config = ConfigDict(populate_by_name=True)

    number_of_working_days: int = Field(alias="numberOfWorkingDays")
    required_seconds: int = Field(alias="requiredSeconds")
    days: list[DaySchedule]


# ========== Work Attribute ==========


class WorkAttributeType(BaseModel):
    """工作属性类型"""
    model_config = ConfigDict(populate_by_name=True)

    name: str
    value: str  # ACCOUNT, BILLABLE_SECONDS, CHECKBOX, DYNAMIC_DROPDOWN, INPUT_FIELD, INPUT_NUMERIC, STATIC_LIST
    system_type: Optional[bool] = Field(None, alias="systemType")


class StaticListValue(BaseModel):
    """静态列表值"""
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = None
    name: str
    value: str
    removed: Optional[bool] = None
    sequence: Optional[int] = None
    work_attribute_id: Optional[int] = Field(None, alias="workAttributeId")


class WorkAttribute(BaseModel):
    """工作属性"""
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = None
    key: Optional[str] = None
    name: str
    type: WorkAttributeType
    external_url: Optional[str] = Field(None, alias="externalUrl")
    required: bool = False
    sequence: Optional[int] = None
    static_list_values: Optional[list[StaticListValue]] = Field(None, alias="staticListValues")


class WorkAttributeCreate(BaseModel):
    """创建工作属性"""
    model_config = ConfigDict(populate_by_name=True)

    name: str
    type_value: str = Field(alias="typeValue")  # CHECKBOX, INPUT_FIELD, INPUT_NUMERIC, STATIC_LIST
    required: bool = False

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式"""
        return {
            "name": self.name,
            "type": {
                "value": self.type_value,
            },
            "required": self.required,
        }


class WorkAttributeValue(BaseModel):
    """工作属性值"""
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = None
    worklog_id: Optional[int] = Field(None, alias="worklogId")
    work_attribute: Optional[WorkAttribute] = Field(None, alias="workAttribute")
    value: Optional[str] = None
    numeric_value: Optional[float] = Field(None, alias="numericValue")
    system_type: Optional[bool] = Field(None, alias="systemType")
    numeric_attribute: Optional[bool] = Field(None, alias="numericAttribute")
    billable_attribute: Optional[bool] = Field(None, alias="billableAttribute")


# ========== Activity Sources (完成计划) ==========


class ActivitySource(BaseModel):
    """活动来源（用于完成计划）"""
    model_config = ConfigDict(populate_by_name=True)

    worklog_id: int = Field(alias="worklogId")
    source_type: str = Field(alias="sourceType")  # PLAN
    source_id: str = Field(alias="sourceId")
    source_date: str = Field(alias="sourceDate")


class ActivitySourceCreate(BaseModel):
    """创建活动来源（完成计划）"""
    model_config = ConfigDict(populate_by_name=True)

    target_type: str = Field("WORKLOG", alias="targetType")
    target_id: int = Field(alias="targetId")  # worklog_id
    source_type: str = Field("PLAN", alias="sourceType")
    source_id: int = Field(alias="sourceId")  # allocation_id
    source_date: str = Field(alias="sourceDate")  # yyyy-MM-dd

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式"""
        return {
            "targetType": self.target_type,
            "targetId": str(self.target_id),
            "sourceType": self.source_type,
            "sourceId": str(self.source_id),
            "sourceDate": self.source_date,
        }
