"""
Tempo Core 资源

API: /rest/tempo-core/1/

包含:
- Expense: 费用管理
- ExpenseCategory: 费用分类
- User Schedule: 用户日程
- Work Attribute: 工作属性
- Activity Sources: 活动来源（完成计划）
"""

from typing import Optional
from atlassian.common.base import BaseResource
from atlassian.tempo.models.core import (
    Expense,
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseCategory,
    UserSchedule,
    WorkAttribute,
    WorkAttributeCreate,
    WorkAttributeType,
    StaticListValue,
    ActivitySourceCreate,
)


class CoreResource(BaseResource):
    """
    Tempo Core 资源

    API 端点:
    - Expense Category:
      - GET /expense/category - 获取费用分类列表
      - POST /expense/category - 创建费用分类
      - PUT /expense/category/{id} - 更新费用分类
      - DELETE /expense/category/{id} - 删除费用分类

    - Expense:
      - GET /expense - 获取费用列表
      - POST /expense - 创建费用
      - GET /expense/{id} - 获取费用
      - PUT /expense/{id} - 更新费用
      - DELETE /expense/{id} - 删除费用

    - User Schedule:
      - GET /user/schedule - 获取用户日程

    - Work Attribute:
      - GET /work-attribute - 获取工作属性列表
      - POST /work-attribute - 创建工作属性
      - GET /work-attribute/{id} - 获取工作属性
      - PUT /work-attribute/{id} - 更新工作属性
      - DELETE /work-attribute/{id} - 删除工作属性
      - GET /work-attribute/type - 获取工作属性类型列表
      - GET /work-attribute/{id}/static-list-value - 获取静态列表值
      - POST /work-attribute/{id}/static-list-value - 创建静态列表值
      - PUT /work-attribute/{id}/static-list-value/{valueId} - 更新静态列表值

    - Activity Sources:
      - POST /activitysources - 完成计划（将计划转换为工时记录）
    """

    BASE_PATH = "/rest/tempo-core/1"

    # ========== Expense Category API ==========

    async def get_expense_categories(
        self,
        query: Optional[str] = None,
        include_expenses: bool = False,
    ) -> list[ExpenseCategory]:
        """
        获取费用分类列表

        Args:
            query: 过滤文本
            include_expenses: 是否返回费用分类下的费用

        Returns:
            list[ExpenseCategory]: 费用分类列表
        """
        params = {}
        if query:
            params["query"] = query
        if include_expenses:
            params["includeExpenses"] = "true"

        data = await self._client.get_json(
            f"{self.BASE_PATH}/expense/category",
            params=params if params else None,
        )
        return [ExpenseCategory.model_validate(item) for item in data]

    async def create_expense_category(self, name: str) -> ExpenseCategory:
        """
        创建费用分类

        Args:
            name: 分类名称

        Returns:
            ExpenseCategory: 创建的费用分类
        """
        data = await self._client.post_json(
            f"{self.BASE_PATH}/expense/category",
            data={"name": name},
        )
        return ExpenseCategory.model_validate(data)

    async def update_expense_category(
        self,
        category_id: int,
        name: str,
    ) -> ExpenseCategory:
        """
        更新费用分类

        Args:
            category_id: 分类 ID
            name: 新名称

        Returns:
            ExpenseCategory: 更新后的费用分类
        """
        data = await self._client.put_json(
            f"{self.BASE_PATH}/expense/category/{category_id}",
            data={"name": name},
        )
        return ExpenseCategory.model_validate(data)

    async def delete_expense_category(self, category_id: int) -> bool:
        """
        删除费用分类

        Args:
            category_id: 分类 ID

        Returns:
            bool: 是否成功
        """
        result = await self._client.delete_json(
            f"{self.BASE_PATH}/expense/category/{category_id}"
        )
        return result is True

    # ========== Expense API ==========

    async def get_expenses(
        self,
        scope_type: Optional[str] = None,
        scope_id: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> list[Expense]:
        """
        获取费用列表

        Args:
            scope_type: 范围类型 (ISSUE)
            scope_id: 范围 ID (Issue ID)
            date_from: 开始日期 "yyyy-MM-dd"
            date_to: 结束日期 "yyyy-MM-dd"

        Returns:
            list[Expense]: 费用列表
        """
        params = {}
        if scope_type:
            params["scopeType"] = scope_type
        if scope_id:
            params["scopeId"] = str(scope_id)
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to

        data = await self._client.get_json(
            f"{self.BASE_PATH}/expense",
            params=params if params else None,
        )
        return [Expense.model_validate(item) for item in data]

    async def create_expense(
        self,
        date: str,
        amount: float,
        scope_id: int,
        expense_category_id: int,
        scope_type: str = "ISSUE",
        description: Optional[str] = None,
        created_by_username: Optional[str] = None,
        created_by_key: Optional[str] = None,
    ) -> Expense:
        """
        创建费用

        Args:
            date: 日期 "yyyy-MM-dd"
            amount: 金额
            scope_id: 范围 ID (Issue ID)
            expense_category_id: 费用分类 ID
            scope_type: 范围类型 (默认 "ISSUE")
            description: 描述
            created_by_username: 创建者用户名
            created_by_key: 创建者 key

        Returns:
            Expense: 创建的费用
        """
        expense = ExpenseCreate(
            date=date,
            amount=amount,
            scope_id=scope_id,
            scope_type=scope_type,
            expense_category_id=expense_category_id,
            description=description,
            created_by_username=created_by_username,
            created_by_key=created_by_key,
        )
        data = await self._client.post_json(
            f"{self.BASE_PATH}/expense",
            data=expense.to_api_dict(),
        )
        return Expense.model_validate(data)

    async def get_expense(self, expense_id: int) -> Expense:
        """
        获取费用

        Args:
            expense_id: 费用 ID

        Returns:
            Expense: 费用
        """
        data = await self._client.get_json(f"{self.BASE_PATH}/expense/{expense_id}")
        return Expense.model_validate(data)

    async def update_expense(
        self,
        expense_id: int,
        date: Optional[str] = None,
        amount: Optional[float] = None,
        scope_id: Optional[int] = None,
        scope_type: Optional[str] = None,
        expense_category_id: Optional[int] = None,
        description: Optional[str] = None,
    ) -> Expense:
        """
        更新费用

        Args:
            expense_id: 费用 ID
            date: 日期 "yyyy-MM-dd"
            amount: 金额
            scope_id: 范围 ID (Issue ID)
            scope_type: 范围类型
            expense_category_id: 费用分类 ID
            description: 描述

        Returns:
            Expense: 更新后的费用
        """
        update = ExpenseUpdate(
            date=date,
            amount=amount,
            scope_id=scope_id,
            scope_type=scope_type,
            expense_category_id=expense_category_id,
            description=description,
        )
        data = await self._client.put_json(
            f"{self.BASE_PATH}/expense/{expense_id}",
            data=update.to_api_dict(),
        )
        return Expense.model_validate(data)

    async def delete_expense(self, expense_id: int) -> bool:
        """
        删除费用

        Args:
            expense_id: 费用 ID

        Returns:
            bool: 是否成功
        """
        result = await self._client.delete_json(
            f"{self.BASE_PATH}/expense/{expense_id}"
        )
        return result is True

    # ========== User Schedule API ==========

    async def get_user_schedule(
        self,
        user: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> UserSchedule:
        """
        获取用户日程

        Args:
            user: 用户名（默认当前登录用户）
            from_date: 开始日期 "yyyy-MM-dd"（默认今天）
            to_date: 结束日期 "yyyy-MM-dd"（默认今天）

        Returns:
            UserSchedule: 用户日程
        """
        params = {}
        if user:
            params["user"] = user
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        data = await self._client.get_json(
            f"{self.BASE_PATH}/user/schedule",
            params=params if params else None,
        )
        return UserSchedule.model_validate(data)

    # ========== Work Attribute API ==========

    async def get_work_attributes(
        self,
        key: Optional[str] = None,
        type: Optional[str] = None,
    ) -> list[WorkAttribute]:
        """
        获取工作属性列表

        Args:
            key: 工作属性唯一 key
            type: 属性类型 (ACCOUNT, BILLABLE_SECONDS, CHECKBOX, DYNAMIC_DROPDOWN,
                  INPUT_FIELD, INPUT_NUMERIC, STATIC_LIST)

        Returns:
            list[WorkAttribute]: 工作属性列表
        """
        params = {}
        if key:
            params["key"] = key
        if type:
            params["type"] = type

        data = await self._client.get_json(
            f"{self.BASE_PATH}/work-attribute",
            params=params if params else None,
        )
        return [WorkAttribute.model_validate(item) for item in data]

    async def create_work_attribute(
        self,
        name: str,
        type_value: str,
        required: bool = False,
    ) -> WorkAttribute:
        """
        创建工作属性

        需要 Tempo 管理员权限

        Args:
            name: 属性名称
            type_value: 属性类型 (CHECKBOX, INPUT_FIELD, INPUT_NUMERIC, STATIC_LIST)
            required: 是否必填

        Returns:
            WorkAttribute: 创建的工作属性
        """
        attr = WorkAttributeCreate(
            name=name,
            type_value=type_value,
            required=required,
        )
        data = await self._client.post_json(
            f"{self.BASE_PATH}/work-attribute",
            data=attr.to_api_dict(),
        )
        return WorkAttribute.model_validate(data)

    async def get_work_attribute(self, attribute_id: int) -> WorkAttribute:
        """
        获取工作属性

        Args:
            attribute_id: 属性 ID

        Returns:
            WorkAttribute: 工作属性
        """
        data = await self._client.get_json(
            f"{self.BASE_PATH}/work-attribute/{attribute_id}"
        )
        return WorkAttribute.model_validate(data)

    async def update_work_attribute(
        self,
        attribute_id: int,
        name: str,
        type_value: str,
        required: bool = False,
    ) -> WorkAttribute:
        """
        更新工作属性

        需要 Tempo 管理员权限

        Args:
            attribute_id: 属性 ID
            name: 属性名称
            type_value: 属性类型
            required: 是否必填

        Returns:
            WorkAttribute: 更新后的工作属性
        """
        attr = WorkAttributeCreate(
            name=name,
            type_value=type_value,
            required=required,
        )
        data = await self._client.put_json(
            f"{self.BASE_PATH}/work-attribute/{attribute_id}",
            data=attr.to_api_dict(),
        )
        return WorkAttribute.model_validate(data)

    async def delete_work_attribute(self, attribute_id: int) -> bool:
        """
        删除工作属性

        需要 Tempo 管理员权限

        Args:
            attribute_id: 属性 ID

        Returns:
            bool: 是否成功
        """
        result = await self._client.delete_json(
            f"{self.BASE_PATH}/work-attribute/{attribute_id}"
        )
        return result is True

    async def get_work_attribute_types(self) -> list[WorkAttributeType]:
        """
        获取所有可用的工作属性类型

        Returns:
            list[WorkAttributeType]: 工作属性类型列表
        """
        data = await self._client.get_json(f"{self.BASE_PATH}/work-attribute/type")
        return [WorkAttributeType.model_validate(item) for item in data]

    async def get_static_list_values(
        self,
        attribute_id: int,
    ) -> list[StaticListValue]:
        """
        获取工作属性的静态列表值

        Args:
            attribute_id: 工作属性 ID

        Returns:
            list[StaticListValue]: 静态列表值列表
        """
        data = await self._client.get_json(
            f"{self.BASE_PATH}/work-attribute/{attribute_id}/static-list-value"
        )
        return [StaticListValue.model_validate(item) for item in data]

    async def create_static_list_value(
        self,
        attribute_id: int,
        name: str,
        value: str,
    ) -> StaticListValue:
        """
        创建静态列表值

        需要 Tempo 管理员权限

        Args:
            attribute_id: 工作属性 ID
            name: 名称
            value: 值

        Returns:
            StaticListValue: 创建的静态列表值
        """
        data = await self._client.post_json(
            f"{self.BASE_PATH}/work-attribute/{attribute_id}/static-list-value",
            data={"name": name, "value": value},
        )
        return StaticListValue.model_validate(data)

    async def update_static_list_value(
        self,
        attribute_id: int,
        value_id: int,
        name: str,
        value: str,
    ) -> StaticListValue:
        """
        更新静态列表值

        需要 Tempo 管理员权限

        Args:
            attribute_id: 工作属性 ID
            value_id: 静态列表值 ID
            name: 名称
            value: 值

        Returns:
            StaticListValue: 更新后的静态列表值
        """
        data = await self._client.put_json(
            f"{self.BASE_PATH}/work-attribute/{attribute_id}/static-list-value/{value_id}",
            data={"name": name, "value": value},
        )
        return StaticListValue.model_validate(data)

    # ========== Activity Sources API (完成计划) ==========

    async def complete_plan_to_worklog(
        self,
        worklog_id: int,
        allocation_id: int,
        source_date: str,
    ) -> dict:
        """
        完成计划 - 将计划转换为工作日志

        Args:
            worklog_id: 工作日志 ID (Tempo worklog ID)
            allocation_id: 计划分配 ID (从 create_plan 返回的 allocation_id)
            source_date: 计划日期 "yyyy-MM-dd"

        Returns:
            dict: API 响应
        """
        activity_source = ActivitySourceCreate(
            target_id=worklog_id,
            source_id=allocation_id,
            source_date=source_date,
        )
        return await self._client.post_json(
            f"{self.BASE_PATH}/activitysources",
            data=activity_source.to_api_dict(),
        )
