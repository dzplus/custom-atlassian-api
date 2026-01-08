"""
Sprint Resource - Sprint（冲刺）API

POST   /rest/agile/1.0/sprint                     - 创建 Sprint
GET    /rest/agile/1.0/sprint/{sprintId}          - 获取 Sprint
PUT    /rest/agile/1.0/sprint/{sprintId}          - 更新 Sprint（全量）
POST   /rest/agile/1.0/sprint/{sprintId}          - 更新 Sprint（部分）
DELETE /rest/agile/1.0/sprint/{sprintId}          - 删除 Sprint
GET    /rest/agile/1.0/sprint/{sprintId}/issue    - 获取 Sprint Issue
POST   /rest/agile/1.0/sprint/{sprintId}/issue    - 移动 Issue 到 Sprint
POST   /rest/agile/1.0/sprint/{sprintId}/swap     - 交换 Sprint 顺序
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.agile import (
    Sprint,
    AgileIssueList,
)


class SprintResource(BaseResource):
    """
    Sprint 资源

    API: /rest/agile/1.0/sprint
    """

    BASE_PATH = "/rest/agile/1.0/sprint"

    # ==================== Sprint CRUD ====================

    async def create(
        self,
        name: str,
        origin_board_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        goal: Optional[str] = None,
    ) -> Sprint:
        """
        创建 Sprint

        POST /rest/agile/1.0/sprint

        Args:
            name: Sprint 名称
            origin_board_id: 所属看板 ID
            start_date: 开始日期（可选，ISO 8601 格式）
            end_date: 结束日期（可选，ISO 8601 格式）
            goal: Sprint 目标（可选）

        Returns:
            Sprint: 创建的 Sprint
        """
        payload: dict[str, Any] = {
            "name": name,
            "originBoardId": origin_board_id,
        }
        if start_date:
            payload["startDate"] = start_date
        if end_date:
            payload["endDate"] = end_date
        if goal:
            payload["goal"] = goal

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return Sprint.model_validate(data)

    async def create_raw(
        self,
        name: str,
        origin_board_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        goal: Optional[str] = None,
    ) -> dict:
        """创建 Sprint（原始 JSON）"""
        payload: dict[str, Any] = {
            "name": name,
            "originBoardId": origin_board_id,
        }
        if start_date:
            payload["startDate"] = start_date
        if end_date:
            payload["endDate"] = end_date
        if goal:
            payload["goal"] = goal

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def get(self, sprint_id: int) -> Sprint:
        """
        获取 Sprint 详情

        GET /rest/agile/1.0/sprint/{sprintId}

        Args:
            sprint_id: Sprint ID

        Returns:
            Sprint: Sprint 信息
        """
        path = f"{self.BASE_PATH}/{sprint_id}"
        data = await self.client.get_json(path)
        return Sprint.model_validate(data)

    async def get_raw(self, sprint_id: int) -> dict:
        """获取 Sprint 详情（原始 JSON）"""
        path = f"{self.BASE_PATH}/{sprint_id}"
        return await self.client.get_json(path)

    async def update(
        self,
        sprint_id: int,
        name: str,
        state: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        complete_date: Optional[str] = None,
        goal: Optional[str] = None,
    ) -> Sprint:
        """
        更新 Sprint（全量更新）

        PUT /rest/agile/1.0/sprint/{sprintId}

        注意：这是全量更新，所有字段都需要提供

        Args:
            sprint_id: Sprint ID
            name: Sprint 名称
            state: Sprint 状态 (future, active, closed)
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            complete_date: 完成日期（可选，关闭 Sprint 时需要）
            goal: Sprint 目标（可选）

        Returns:
            Sprint: 更新后的 Sprint
        """
        path = f"{self.BASE_PATH}/{sprint_id}"
        payload: dict[str, Any] = {
            "name": name,
            "state": state,
        }
        if start_date:
            payload["startDate"] = start_date
        if end_date:
            payload["endDate"] = end_date
        if complete_date:
            payload["completeDate"] = complete_date
        if goal is not None:
            payload["goal"] = goal

        data = await self.client.put_json(path, data=payload)
        return Sprint.model_validate(data)

    async def update_raw(
        self,
        sprint_id: int,
        name: str,
        state: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        complete_date: Optional[str] = None,
        goal: Optional[str] = None,
    ) -> dict:
        """更新 Sprint（原始 JSON）"""
        path = f"{self.BASE_PATH}/{sprint_id}"
        payload: dict[str, Any] = {
            "name": name,
            "state": state,
        }
        if start_date:
            payload["startDate"] = start_date
        if end_date:
            payload["endDate"] = end_date
        if complete_date:
            payload["completeDate"] = complete_date
        if goal is not None:
            payload["goal"] = goal

        return await self.client.put_json(path, data=payload)

    async def partial_update(
        self,
        sprint_id: int,
        name: Optional[str] = None,
        state: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        complete_date: Optional[str] = None,
        goal: Optional[str] = None,
    ) -> Sprint:
        """
        部分更新 Sprint

        POST /rest/agile/1.0/sprint/{sprintId}

        只更新提供的字段，未提供的字段保持不变

        Args:
            sprint_id: Sprint ID
            name: Sprint 名称（可选）
            state: Sprint 状态（可选）(future, active, closed)
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            complete_date: 完成日期（可选）
            goal: Sprint 目标（可选，传空字符串可清除）

        Returns:
            Sprint: 更新后的 Sprint
        """
        path = f"{self.BASE_PATH}/{sprint_id}"
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if state is not None:
            payload["state"] = state
        if start_date is not None:
            payload["startDate"] = start_date
        if end_date is not None:
            payload["endDate"] = end_date
        if complete_date is not None:
            payload["completeDate"] = complete_date
        if goal is not None:
            payload["goal"] = goal

        data = await self.client.post_json(path, data=payload)
        return Sprint.model_validate(data)

    async def partial_update_raw(
        self,
        sprint_id: int,
        name: Optional[str] = None,
        state: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        complete_date: Optional[str] = None,
        goal: Optional[str] = None,
    ) -> dict:
        """部分更新 Sprint（原始 JSON）"""
        path = f"{self.BASE_PATH}/{sprint_id}"
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if state is not None:
            payload["state"] = state
        if start_date is not None:
            payload["startDate"] = start_date
        if end_date is not None:
            payload["endDate"] = end_date
        if complete_date is not None:
            payload["completeDate"] = complete_date
        if goal is not None:
            payload["goal"] = goal

        return await self.client.post_json(path, data=payload)

    async def delete(self, sprint_id: int) -> None:
        """
        删除 Sprint

        DELETE /rest/agile/1.0/sprint/{sprintId}

        注意：只有 future 状态的 Sprint 可以删除
        删除后，Sprint 中的 Issue 会移到 Backlog

        Args:
            sprint_id: Sprint ID
        """
        path = f"{self.BASE_PATH}/{sprint_id}"
        await self.client.delete(path)

    # ==================== Sprint Issues ====================

    async def get_issues(
        self,
        sprint_id: int,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        validate_query: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> AgileIssueList:
        """
        获取 Sprint 中的 Issue

        GET /rest/agile/1.0/sprint/{sprintId}/issue

        Args:
            sprint_id: Sprint ID
            start_at: 起始位置
            max_results: 最大返回数量
            jql: JQL 过滤条件
            validate_query: 是否验证 JQL
            fields: 返回的字段
            expand: 展开字段

        Returns:
            AgileIssueList: Issue 列表
        """
        path = f"{self.BASE_PATH}/{sprint_id}/issue"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if jql:
            params["jql"] = jql
        if validate_query is not None:
            params["validateQuery"] = validate_query
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return AgileIssueList.model_validate(data)

    async def get_issues_raw(
        self,
        sprint_id: int,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """获取 Sprint Issue（原始 JSON）"""
        path = f"{self.BASE_PATH}/{sprint_id}/issue"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if jql:
            params["jql"] = jql
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    async def move_issues(
        self,
        sprint_id: int,
        issues: list[str],
        rank_before_issue: Optional[str] = None,
        rank_after_issue: Optional[str] = None,
        rank_custom_field_id: Optional[int] = None,
    ) -> None:
        """
        移动 Issue 到 Sprint

        POST /rest/agile/1.0/sprint/{sprintId}/issue

        Args:
            sprint_id: Sprint ID
            issues: Issue Key 或 ID 列表（最多50个）
            rank_before_issue: 排在此 Issue 之前（可选）
            rank_after_issue: 排在此 Issue 之后（可选）
            rank_custom_field_id: 排序字段 ID（可选）
        """
        path = f"{self.BASE_PATH}/{sprint_id}/issue"
        payload: dict[str, Any] = {"issues": issues}
        if rank_before_issue:
            payload["rankBeforeIssue"] = rank_before_issue
        if rank_after_issue:
            payload["rankAfterIssue"] = rank_after_issue
        if rank_custom_field_id:
            payload["rankCustomFieldId"] = rank_custom_field_id

        response = await self.client.post(path, json=payload)
        response.raise_for_status()

    # ==================== Sprint Operations ====================

    async def swap(self, sprint_id: int, sprint_to_swap_with: int) -> None:
        """
        交换两个 Sprint 的位置

        POST /rest/agile/1.0/sprint/{sprintId}/swap

        Args:
            sprint_id: 当前 Sprint ID
            sprint_to_swap_with: 要交换的 Sprint ID
        """
        path = f"{self.BASE_PATH}/{sprint_id}/swap"
        payload = {"sprintToSwapWith": sprint_to_swap_with}
        response = await self.client.post(path, json=payload)
        response.raise_for_status()

    async def start(self, sprint_id: int) -> Sprint:
        """
        启动 Sprint（将 future 状态改为 active）

        Args:
            sprint_id: Sprint ID

        Returns:
            Sprint: 更新后的 Sprint
        """
        return await self.partial_update(sprint_id, state="active")

    async def close(
        self,
        sprint_id: int,
        complete_date: Optional[str] = None,
    ) -> Sprint:
        """
        关闭 Sprint（将 active 状态改为 closed）

        Args:
            sprint_id: Sprint ID
            complete_date: 完成日期（可选，ISO 8601 格式）

        Returns:
            Sprint: 更新后的 Sprint
        """
        return await self.partial_update(
            sprint_id,
            state="closed",
            complete_date=complete_date,
        )

    # ==================== Sprint Properties ====================

    async def get_property_keys(self, sprint_id: int) -> dict:
        """
        获取 Sprint 属性键列表

        GET /rest/agile/1.0/sprint/{sprintId}/properties

        Args:
            sprint_id: Sprint ID

        Returns:
            dict: 属性键列表
        """
        path = f"{self.BASE_PATH}/{sprint_id}/properties"
        return await self.client.get_json(path)

    async def get_property(self, sprint_id: int, property_key: str) -> dict:
        """
        获取 Sprint 属性

        GET /rest/agile/1.0/sprint/{sprintId}/properties/{propertyKey}

        Args:
            sprint_id: Sprint ID
            property_key: 属性键

        Returns:
            dict: 属性值
        """
        path = f"{self.BASE_PATH}/{sprint_id}/properties/{property_key}"
        return await self.client.get_json(path)

    async def set_property(
        self,
        sprint_id: int,
        property_key: str,
        value: Any,
    ) -> None:
        """
        设置 Sprint 属性

        PUT /rest/agile/1.0/sprint/{sprintId}/properties/{propertyKey}

        Args:
            sprint_id: Sprint ID
            property_key: 属性键
            value: 属性值
        """
        path = f"{self.BASE_PATH}/{sprint_id}/properties/{property_key}"
        await self.client.put_json(path, data=value)

    async def delete_property(self, sprint_id: int, property_key: str) -> None:
        """
        删除 Sprint 属性

        DELETE /rest/agile/1.0/sprint/{sprintId}/properties/{propertyKey}

        Args:
            sprint_id: Sprint ID
            property_key: 属性键
        """
        path = f"{self.BASE_PATH}/{sprint_id}/properties/{property_key}"
        await self.client.delete(path)
