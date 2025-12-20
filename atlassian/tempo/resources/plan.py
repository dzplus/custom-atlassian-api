"""
Tempo Plan 资源

API: /rest/tempo-planning/1/
"""

from typing import Optional
from atlassian.common.base import BaseResource
from atlassian.tempo.models.plan import (
    Allocation,
    AllocationCreate,
    PlanLog,
    Plan,
    PlanSearchParams,
)


class PlanResource(BaseResource):
    """
    Tempo 计划资源

    包含两种 API:
    - Allocation: 资源分配 (长期计划)
    - Plan: 计划条目 (日级别计划)

    Allocation API 端点:
    - GET /allocation - 获取资源分配
    - POST /allocation - 创建资源分配
    - GET /allocation/{id} - 获取单个资源分配
    - PUT /allocation/{id} - 更新资源分配
    - DELETE /allocation/{id} - 删除资源分配

    Plan API 端点:
    - POST /plan/search - 搜索计划
    - POST /plan - 创建计划
    - PUT /plan - 更新计划
    """

    BASE_PATH = "/rest/tempo-planning/1"
    ALLOCATION_PATH = "/rest/tempo-planning/1/allocation"
    PLAN_PATH = "/rest/tempo-planning/1/plan"

    # ========== Allocation API ==========

    async def get_allocations(
        self,
        start_date: str,
        end_date: str,
        assignee_keys: Optional[list[str]] = None,
        assignee_type: Optional[str] = None,
        plan_item_id: Optional[str] = None,
        plan_item_type: Optional[str] = None,
    ) -> list[Allocation]:
        """
        获取资源分配

        Args:
            start_date: 开始日期 "2024-01-01"
            end_date: 结束日期 "2024-01-31"
            assignee_keys: 分配人用户 key 列表
            assignee_type: 分配人类型 (USER, TEAM)
            plan_item_id: 计划项 ID (如 Issue key)
            plan_item_type: 计划项类型 (ISSUE, PROJECT)

        Returns:
            list[Allocation]: 资源分配列表
        """
        params = {
            "startDate": start_date,
            "endDate": end_date,
        }
        if assignee_keys:
            params["assigneeKeys"] = ",".join(assignee_keys)
        if assignee_type:
            params["assigneeType"] = assignee_type
        if plan_item_id:
            params["planItemId"] = plan_item_id
        if plan_item_type:
            params["planItemType"] = plan_item_type

        data = await self._client.get_json(self.ALLOCATION_PATH, params=params)
        return [Allocation.model_validate(item) for item in data]

    async def get_allocations_raw(
        self,
        start_date: str,
        end_date: str,
        **kwargs,
    ) -> list[dict]:
        """获取资源分配原始数据"""
        params = {
            "startDate": start_date,
            "endDate": end_date,
            **kwargs,
        }
        return await self._client.get_json(self.ALLOCATION_PATH, params=params)

    async def create_allocation(
        self,
        assignee_key: str,
        plan_item_id: str,
        start_date: str,
        end_date: str,
        seconds_per_day: int,
        assignee_type: str = "USER",
        plan_item_type: str = "ISSUE",
        description: Optional[str] = None,
        include_non_working_days: bool = False,
    ) -> Allocation:
        """
        创建资源分配

        Args:
            assignee_key: 分配人用户 key
            plan_item_id: 计划项 ID (如 Issue key)
            start_date: 开始日期
            end_date: 结束日期
            seconds_per_day: 每天分配的秒数
            assignee_type: 分配人类型 (USER, TEAM)
            plan_item_type: 计划项类型 (ISSUE, PROJECT)
            description: 描述
            include_non_working_days: 是否包含非工作日

        Returns:
            Allocation: 创建的资源分配
        """
        allocation = AllocationCreate(
            assignee_key=assignee_key,
            assignee_type=assignee_type,
            plan_item_id=plan_item_id,
            plan_item_type=plan_item_type,
            start_date=start_date,
            end_date=end_date,
            seconds_per_day=seconds_per_day,
            description=description,
            include_non_working_days=include_non_working_days,
        )
        data = await self._client.post_json(
            self.ALLOCATION_PATH,
            data=allocation.to_api_dict(),
        )
        return Allocation.model_validate(data)

    async def get_allocation(self, allocation_id: int) -> Allocation:
        """
        获取单个资源分配

        Args:
            allocation_id: 资源分配 ID

        Returns:
            Allocation: 资源分配
        """
        data = await self._client.get_json(f"{self.ALLOCATION_PATH}/{allocation_id}")
        return Allocation.model_validate(data)

    async def update_allocation(
        self,
        allocation_id: int,
        assignee_key: str,
        plan_item_id: str,
        start_date: str,
        end_date: str,
        seconds_per_day: int,
        assignee_type: str = "USER",
        plan_item_type: str = "ISSUE",
        description: Optional[str] = None,
        include_non_working_days: bool = False,
    ) -> Allocation:
        """
        更新资源分配

        Args:
            allocation_id: 资源分配 ID
            其他参数同 create_allocation

        Returns:
            Allocation: 更新后的资源分配
        """
        allocation = AllocationCreate(
            assignee_key=assignee_key,
            assignee_type=assignee_type,
            plan_item_id=plan_item_id,
            plan_item_type=plan_item_type,
            start_date=start_date,
            end_date=end_date,
            seconds_per_day=seconds_per_day,
            description=description,
            include_non_working_days=include_non_working_days,
        )
        data = await self._client.put_json(
            f"{self.ALLOCATION_PATH}/{allocation_id}",
            data=allocation.to_api_dict(),
        )
        return Allocation.model_validate(data)

    async def delete_allocation(self, allocation_id: int) -> bool:
        """
        删除资源分配

        Args:
            allocation_id: 资源分配 ID

        Returns:
            bool: 是否成功
        """
        await self._client.delete_json(f"{self.ALLOCATION_PATH}/{allocation_id}")
        return True

    # ========== Plan API ==========

    async def search_plans(
        self,
        from_date: str,
        to_date: str,
        assignee_keys: Optional[list[str]] = None,
        plan_item_ids: Optional[list[str]] = None,
    ) -> list[PlanLog]:
        """
        搜索计划

        Args:
            from_date: 开始日期 "2024-01-01"
            to_date: 结束日期 "2024-01-31"
            assignee_keys: 分配人用户 key 列表
            plan_item_ids: 计划项 ID 列表 (如 Issue keys)

        Returns:
            list[PlanLog]: 计划日志列表
        """
        params = PlanSearchParams(
            from_date=from_date,
            to_date=to_date,
            assignee_keys=assignee_keys,
            plan_item_ids=plan_item_ids,
        )
        data = await self._client.post_json(
            f"{self.PLAN_PATH}/search",
            data=params.to_api_dict(),
        )
        return [PlanLog.model_validate(item) for item in data]

    async def search_plans_raw(
        self,
        from_date: str,
        to_date: str,
        assignee_keys: Optional[list[str]] = None,
        plan_item_ids: Optional[list[str]] = None,
    ) -> list[dict]:
        """搜索计划原始数据"""
        params = PlanSearchParams(
            from_date=from_date,
            to_date=to_date,
            assignee_keys=assignee_keys,
            plan_item_ids=plan_item_ids,
        )
        return await self._client.post_json(
            f"{self.PLAN_PATH}/search",
            data=params.to_api_dict(),
        )

    async def create_plan(
        self,
        assignee_key: str,
        plan_item_id: int,
        start_date: str,
        end_date: str,
        seconds_per_day: int,
        plan_item_type: str = "ISSUE",
        description: Optional[str] = None,
        include_non_working_days: bool = False,
        start_time: str = "09:00",
    ) -> list[PlanLog]:
        """
        创建计划

        Args:
            assignee_key: 分配人用户 key
            plan_item_id: 计划项 ID (必须是整数，如 Issue 的内部 ID)
            start_date: 开始日期
            end_date: 结束日期
            seconds_per_day: 每天计划的秒数
            plan_item_type: 计划项类型 (ISSUE, PROJECT)
            description: 描述
            include_non_working_days: 是否包含非工作日
            start_time: 开始时间，默认 09:00

        Returns:
            list[PlanLog]: 创建的计划日志列表
        """
        plan = Plan(
            assignee_key=assignee_key,
            plan_item_id=plan_item_id,
            plan_item_type=plan_item_type,
            day=start_date,  # day 字段使用开始日期
            start=start_date,
            end=end_date,
            start_time=start_time,
            seconds_per_day=seconds_per_day,
            description=description,
            include_non_working_days=include_non_working_days,
        )
        data = await self._client.post_json(
            self.PLAN_PATH,
            data=plan.to_api_dict(),
        )
        return [PlanLog.model_validate(item) for item in data]

    async def update_plan(
        self,
        allocation_id: int,
        assignee_key: str,
        plan_item_id: int,
        start_date: str,
        end_date: str,
        seconds_per_day: int,
        plan_item_type: str = "ISSUE",
        description: Optional[str] = None,
        include_non_working_days: bool = False,
        start_time: str = "09:00",
    ) -> list[PlanLog]:
        """
        更新计划

        Args:
            allocation_id: 资源分配 ID（必需）
            assignee_key: 分配人用户 key
            plan_item_id: 计划项 ID (必须是整数，如 Issue 的内部 ID)
            start_date: 开始日期
            end_date: 结束日期
            seconds_per_day: 每天计划的秒数
            plan_item_type: 计划项类型 (ISSUE, PROJECT)
            description: 描述
            include_non_working_days: 是否包含非工作日
            start_time: 开始时间，默认 09:00

        Returns:
            list[PlanLog]: 更新后的计划日志列表
        """
        plan = Plan(
            assignee_key=assignee_key,
            plan_item_id=plan_item_id,
            plan_item_type=plan_item_type,
            day=start_date,  # day 字段使用开始日期
            start=start_date,
            end=end_date,
            start_time=start_time,
            seconds_per_day=seconds_per_day,
            allocation_id=allocation_id,  # 更新时必需
            description=description,
            include_non_working_days=include_non_working_days,
        )
        data = await self._client.put_json(
            self.PLAN_PATH,
            data=plan.to_api_dict(),
        )
        return [PlanLog.model_validate(item) for item in data]

    async def remove_plan_from_date(
        self,
        plan_id: int,
        date: str,
    ) -> list[PlanLog]:
        """
        从特定日期移除计划

        Args:
            plan_id: 计划 ID
            date: 要移除的日期 "2024-01-15"

        Returns:
            list[PlanLog]: 剩余的计划日志列表
        """
        data = await self._client.put_json(
            f"{self.PLAN_PATH}/remove/planLog/{plan_id}",
            params={"date": date},
        )
        return [PlanLog.model_validate(item) for item in data]
