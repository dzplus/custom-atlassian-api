"""
Epic Resource - Epic API

GET    /rest/agile/1.0/epic/{epicIdOrKey}           - 获取 Epic
POST   /rest/agile/1.0/epic/{epicIdOrKey}           - 更新 Epic
GET    /rest/agile/1.0/epic/{epicIdOrKey}/issue     - 获取 Epic Issue
POST   /rest/agile/1.0/epic/{epicIdOrKey}/issue     - 移动 Issue 到 Epic
PUT    /rest/agile/1.0/epic/{epicIdOrKey}/rank      - 排序 Epic
GET    /rest/agile/1.0/epic/none/issue              - 获取无 Epic 的 Issue
POST   /rest/agile/1.0/epic/none/issue              - 移除 Issue 的 Epic
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.agile import (
    Epic,
    AgileIssueList,
)


class EpicResource(BaseResource):
    """
    Epic 资源

    API: /rest/agile/1.0/epic
    """

    BASE_PATH = "/rest/agile/1.0/epic"

    # ==================== Epic CRUD ====================

    async def get(self, epic_id_or_key: str) -> Epic:
        """
        获取 Epic 详情

        GET /rest/agile/1.0/epic/{epicIdOrKey}

        Args:
            epic_id_or_key: Epic ID 或 Key

        Returns:
            Epic: Epic 信息
        """
        path = f"{self.BASE_PATH}/{epic_id_or_key}"
        data = await self.client.get_json(path)
        return Epic.model_validate(data)

    async def get_raw(self, epic_id_or_key: str) -> dict:
        """获取 Epic 详情（原始 JSON）"""
        path = f"{self.BASE_PATH}/{epic_id_or_key}"
        return await self.client.get_json(path)

    async def update(
        self,
        epic_id_or_key: str,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        color: Optional[str] = None,
        done: Optional[bool] = None,
    ) -> Epic:
        """
        更新 Epic

        POST /rest/agile/1.0/epic/{epicIdOrKey}

        Args:
            epic_id_or_key: Epic ID 或 Key
            name: Epic 名称（可选）
            summary: 摘要（可选）
            color: 颜色（可选），color_1 到 color_9
            done: 是否已完成（可选）

        Returns:
            Epic: 更新后的 Epic
        """
        path = f"{self.BASE_PATH}/{epic_id_or_key}"
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if summary is not None:
            payload["summary"] = summary
        if color is not None:
            payload["color"] = {"key": color}
        if done is not None:
            payload["done"] = done

        data = await self.client.post_json(path, data=payload)
        return Epic.model_validate(data)

    async def update_raw(
        self,
        epic_id_or_key: str,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        color: Optional[str] = None,
        done: Optional[bool] = None,
    ) -> dict:
        """更新 Epic（原始 JSON）"""
        path = f"{self.BASE_PATH}/{epic_id_or_key}"
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if summary is not None:
            payload["summary"] = summary
        if color is not None:
            payload["color"] = {"key": color}
        if done is not None:
            payload["done"] = done

        return await self.client.post_json(path, data=payload)

    async def mark_done(self, epic_id_or_key: str) -> Epic:
        """
        标记 Epic 为已完成

        Args:
            epic_id_or_key: Epic ID 或 Key

        Returns:
            Epic: 更新后的 Epic
        """
        return await self.update(epic_id_or_key, done=True)

    async def mark_not_done(self, epic_id_or_key: str) -> Epic:
        """
        标记 Epic 为未完成

        Args:
            epic_id_or_key: Epic ID 或 Key

        Returns:
            Epic: 更新后的 Epic
        """
        return await self.update(epic_id_or_key, done=False)

    # ==================== Epic Issues ====================

    async def get_issues(
        self,
        epic_id_or_key: str,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        validate_query: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> AgileIssueList:
        """
        获取 Epic 中的 Issue

        GET /rest/agile/1.0/epic/{epicIdOrKey}/issue

        Args:
            epic_id_or_key: Epic ID 或 Key
            start_at: 起始位置
            max_results: 最大返回数量
            jql: JQL 过滤条件
            validate_query: 是否验证 JQL
            fields: 返回的字段
            expand: 展开字段

        Returns:
            AgileIssueList: Issue 列表
        """
        path = f"{self.BASE_PATH}/{epic_id_or_key}/issue"
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
        epic_id_or_key: str,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        validate_query: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """获取 Epic Issue（原始 JSON）"""
        path = f"{self.BASE_PATH}/{epic_id_or_key}/issue"
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

        return await self.client.get_json(path, params=params)

    async def move_issues(
        self,
        epic_id_or_key: str,
        issues: list[str],
    ) -> None:
        """
        移动 Issue 到 Epic

        POST /rest/agile/1.0/epic/{epicIdOrKey}/issue

        Args:
            epic_id_or_key: Epic ID 或 Key
            issues: Issue Key 或 ID 列表（最多50个）
        """
        path = f"{self.BASE_PATH}/{epic_id_or_key}/issue"
        payload = {"issues": issues}
        response = await self.client.post(path, json=payload)
        response.raise_for_status()

    # ==================== Epic Ranking ====================

    async def rank(
        self,
        epic_id_or_key: str,
        rank_before_epic: Optional[str] = None,
        rank_after_epic: Optional[str] = None,
        rank_custom_field_id: Optional[int] = None,
    ) -> None:
        """
        排序 Epic

        PUT /rest/agile/1.0/epic/{epicIdOrKey}/rank

        Args:
            epic_id_or_key: Epic ID 或 Key
            rank_before_epic: 排在此 Epic 之前（可选）
            rank_after_epic: 排在此 Epic 之后（可选）
            rank_custom_field_id: 排序字段 ID（可选）
        """
        path = f"{self.BASE_PATH}/{epic_id_or_key}/rank"
        payload: dict[str, Any] = {}
        if rank_before_epic:
            payload["rankBeforeEpic"] = rank_before_epic
        if rank_after_epic:
            payload["rankAfterEpic"] = rank_after_epic
        if rank_custom_field_id:
            payload["rankCustomFieldId"] = rank_custom_field_id

        response = await self.client.put(path, json=payload)
        response.raise_for_status()

    # ==================== Issues Without Epic ====================

    async def get_issues_without_epic(
        self,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        validate_query: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> AgileIssueList:
        """
        获取没有 Epic 的 Issue

        GET /rest/agile/1.0/epic/none/issue

        Args:
            start_at: 起始位置
            max_results: 最大返回数量
            jql: JQL 过滤条件
            validate_query: 是否验证 JQL
            fields: 返回的字段
            expand: 展开字段

        Returns:
            AgileIssueList: 无 Epic 的 Issue 列表
        """
        path = f"{self.BASE_PATH}/none/issue"
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

    async def get_issues_without_epic_raw(
        self,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """获取无 Epic 的 Issue（原始 JSON）"""
        path = f"{self.BASE_PATH}/none/issue"
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

    async def remove_issues_from_epic(self, issues: list[str]) -> None:
        """
        从 Epic 中移除 Issue（将 Issue 的 Epic 字段清空）

        POST /rest/agile/1.0/epic/none/issue

        Args:
            issues: Issue Key 或 ID 列表（最多50个）
        """
        path = f"{self.BASE_PATH}/none/issue"
        payload = {"issues": issues}
        response = await self.client.post(path, json=payload)
        response.raise_for_status()
