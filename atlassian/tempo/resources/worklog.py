"""
Tempo Worklog 资源

API: /rest/tempo-timesheets/4/worklogs
"""

from typing import Optional
from atlassian.common.base import BaseResource
from atlassian.tempo.models.worklog import (
    Worklog,
    WorklogCreate,
    WorklogUpdate,
    WorklogSearchParams,
)


class WorklogResource(BaseResource):
    """
    Tempo 工时记录资源

    API 端点:
    - POST /worklogs - 创建工时记录
    - GET /worklogs/{worklogId} - 获取工时记录
    - PUT /worklogs/{worklogId} - 更新工时记录
    - DELETE /worklogs/{worklogId} - 删除工时记录
    - POST /worklogs/search - 搜索工时记录
    """

    BASE_PATH = "/rest/tempo-timesheets/4/worklogs"

    async def create(
        self,
        issue_key: str,
        worker: str,
        started: str,
        time_spent_seconds: int,
        description: Optional[str] = None,
        billable_seconds: Optional[int] = None,
        started_time: Optional[str] = None,
        attributes: Optional[dict] = None,
    ) -> Worklog:
        """
        创建工时记录

        Args:
            issue_key: Issue Key (如 "DEMO-123")
            worker: 工作者用户 key
            started: 开始日期 "2024-01-15"
            time_spent_seconds: 花费时间（秒）
            description: 描述
            billable_seconds: 可计费时间（秒）
            started_time: 开始时间 "09:00:00"
            attributes: 自定义属性

        Returns:
            Worklog: 创建的工时记录
        """
        worklog = WorklogCreate(
            issue_key=issue_key,
            worker=worker,
            started=started,
            time_spent_seconds=time_spent_seconds,
            description=description,
            billable_seconds=billable_seconds,
            started_time=started_time,
            attributes=attributes,
        )
        data = await self._client.post_json(
            self.BASE_PATH,
            data=worklog.to_api_dict(),
        )

        # Tempo API 返回的是数组，取第一个元素
        if isinstance(data, list) and len(data) > 0:
            return Worklog.model_validate(data[0])

        return Worklog.model_validate(data)

    async def get(self, worklog_id: int) -> Worklog:
        """
        获取工时记录

        Args:
            worklog_id: 工时记录 ID

        Returns:
            Worklog: 工时记录
        """
        data = await self._client.get_json(f"{self.BASE_PATH}/{worklog_id}")
        return Worklog.model_validate(data)

    async def get_raw(self, worklog_id: int) -> dict:
        """获取工时记录原始数据"""
        return await self._client.get_json(f"{self.BASE_PATH}/{worklog_id}")

    async def update(
        self,
        worklog_id: int,
        started: Optional[str] = None,
        time_spent_seconds: Optional[int] = None,
        description: Optional[str] = None,
        billable_seconds: Optional[int] = None,
        started_time: Optional[str] = None,
        attributes: Optional[dict] = None,
    ) -> Worklog:
        """
        更新工时记录

        注意: 不能修改 worker 和 originTaskId

        Args:
            worklog_id: 工时记录 ID
            started: 开始日期
            time_spent_seconds: 花费时间（秒）
            description: 描述
            billable_seconds: 可计费时间（秒）
            started_time: 开始时间
            attributes: 自定义属性

        Returns:
            Worklog: 更新后的工时记录
        """
        update = WorklogUpdate(
            started=started,
            time_spent_seconds=time_spent_seconds,
            description=description,
            billable_seconds=billable_seconds,
            started_time=started_time,
            attributes=attributes,
        )
        data = await self._client.put_json(
            f"{self.BASE_PATH}/{worklog_id}",
            data=update.to_api_dict(),
        )
        return Worklog.model_validate(data)

    async def delete(self, worklog_id: int) -> bool:
        """
        删除工时记录

        Args:
            worklog_id: 工时记录 ID

        Returns:
            bool: 是否成功
        """
        await self._client.delete_json(f"{self.BASE_PATH}/{worklog_id}")
        return True

    async def search(
        self,
        from_date: str,
        to_date: str,
        worker: Optional[list[str]] = None,
        task_id: Optional[list[int]] = None,
        task_key: Optional[list[str]] = None,
        project_id: Optional[list[int]] = None,
        project_key: Optional[list[str]] = None,
        team_id: Optional[list[int]] = None,
        role_id: Optional[list[int]] = None,
        account_id: Optional[list[int]] = None,
        account_key: Optional[list[str]] = None,
        filter_id: Optional[list[int]] = None,
        customer_id: Optional[list[int]] = None,
        category_id: Optional[list[int]] = None,
        category_type_id: Optional[list[int]] = None,
        epic_key: Optional[list[str]] = None,
        location_ids: Optional[list[int]] = None,
        include_subtasks: Optional[bool] = None,
    ) -> list[Worklog]:
        """
        搜索工时记录

        API 文档参考：POST /rest/tempo-timesheets/4/worklogs/search (SearchParamsBean)

        Args:
            from_date: 开始日期 "2024-01-01"
            to_date: 结束日期 "2024-01-31"
            worker: 工作者用户 key 列表
            task_id: Issue 数字 ID 列表（注意：不是 key）
            task_key: Issue Key 列表（如 ["NF-433"]）
            project_id: 项目数字 ID 列表
            project_key: 项目 Key 列表
            team_id: 团队 ID 列表
            role_id: 角色 ID 列表
            account_id: 账户数字 ID 列表
            account_key: 账户 Key 列表
            filter_id: 过滤器 ID 列表
            customer_id: 客户 ID 列表
            category_id: 分类 ID 列表
            category_type_id: 分类类型 ID 列表
            epic_key: Epic Key 列表
            location_ids: 位置 ID 列表
            include_subtasks: 是否包含子任务

        Returns:
            list[Worklog]: 工时记录列表
        """
        params = WorklogSearchParams(
            from_date=from_date,
            to_date=to_date,
            worker=worker,
            task_id=task_id,
            task_key=task_key,
            project_id=project_id,
            project_key=project_key,
            team_id=team_id,
            role_id=role_id,
            account_id=account_id,
            account_key=account_key,
            filter_id=filter_id,
            customer_id=customer_id,
            category_id=category_id,
            category_type_id=category_type_id,
            epic_key=epic_key,
            location_ids=location_ids,
            include_subtasks=include_subtasks,
        )
        data = await self._client.post_json(
            f"{self.BASE_PATH}/search",
            data=params.to_api_dict(),
        )
        # API 返回 list
        return [Worklog.model_validate(item) for item in data]

    async def search_raw(
        self,
        from_date: str,
        to_date: str,
        worker: Optional[list[str]] = None,
        task_id: Optional[list[int]] = None,
        task_key: Optional[list[str]] = None,
        project_id: Optional[list[int]] = None,
        project_key: Optional[list[str]] = None,
        team_id: Optional[list[int]] = None,
        role_id: Optional[list[int]] = None,
        account_id: Optional[list[int]] = None,
        account_key: Optional[list[str]] = None,
        filter_id: Optional[list[int]] = None,
        customer_id: Optional[list[int]] = None,
        category_id: Optional[list[int]] = None,
        category_type_id: Optional[list[int]] = None,
        epic_key: Optional[list[str]] = None,
        location_ids: Optional[list[int]] = None,
        include_subtasks: Optional[bool] = None,
    ) -> list[dict]:
        """搜索工时记录原始数据"""
        params = WorklogSearchParams(
            from_date=from_date,
            to_date=to_date,
            worker=worker,
            task_id=task_id,
            task_key=task_key,
            project_id=project_id,
            project_key=project_key,
            team_id=team_id,
            role_id=role_id,
            account_id=account_id,
            account_key=account_key,
            filter_id=filter_id,
            customer_id=customer_id,
            category_id=category_id,
            category_type_id=category_type_id,
            epic_key=epic_key,
            location_ids=location_ids,
            include_subtasks=include_subtasks,
        )
        return await self._client.post_json(
            f"{self.BASE_PATH}/search",
            data=params.to_api_dict(),
        )
