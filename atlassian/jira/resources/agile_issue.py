"""
Agile Issue Resource - Agile Issue API

GET /rest/agile/1.0/issue/{issueIdOrKey}                    - 获取 Issue（含敏捷字段）
PUT /rest/agile/1.0/issue/rank                              - 排序 Issue
GET /rest/agile/1.0/issue/{issueIdOrKey}/estimation         - 获取 Issue 估算
PUT /rest/agile/1.0/issue/{issueIdOrKey}/estimation         - 更新 Issue 估算
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.agile import (
    AgileIssue,
    IssueEstimation,
)


class AgileIssueResource(BaseResource):
    """
    Agile Issue 资源

    API: /rest/agile/1.0/issue
    """

    BASE_PATH = "/rest/agile/1.0/issue"

    # ==================== Issue ====================

    async def get(
        self,
        issue_id_or_key: str,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
        update_history: Optional[bool] = None,
    ) -> AgileIssue:
        """
        获取 Issue（包含敏捷字段）

        GET /rest/agile/1.0/issue/{issueIdOrKey}

        返回的 Issue 包含敏捷特有字段：sprint, closedSprints, flagged, epic

        Args:
            issue_id_or_key: Issue ID 或 Key
            fields: 返回的字段
            expand: 展开字段
            update_history: 是否更新浏览历史

        Returns:
            AgileIssue: Issue 信息
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}"
        params: dict[str, Any] = {}
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand
        if update_history is not None:
            params["updateHistory"] = update_history

        data = await self.client.get_json(path, params=params)
        return AgileIssue.model_validate(data)

    async def get_raw(
        self,
        issue_id_or_key: str,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
        update_history: Optional[bool] = None,
    ) -> dict:
        """获取 Issue（原始 JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}"
        params: dict[str, Any] = {}
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand
        if update_history is not None:
            params["updateHistory"] = update_history

        return await self.client.get_json(path, params=params)

    # ==================== Ranking ====================

    async def rank(
        self,
        issues: list[str],
        rank_before_issue: Optional[str] = None,
        rank_after_issue: Optional[str] = None,
        rank_custom_field_id: Optional[int] = None,
    ) -> None:
        """
        排序 Issue

        PUT /rest/agile/1.0/issue/rank

        Args:
            issues: Issue Key 或 ID 列表（最多50个）
            rank_before_issue: 排在此 Issue 之前（可选）
            rank_after_issue: 排在此 Issue 之后（可选）
            rank_custom_field_id: 排序字段 ID（可选）
        """
        path = f"{self.BASE_PATH}/rank"
        payload: dict[str, Any] = {"issues": issues}
        if rank_before_issue:
            payload["rankBeforeIssue"] = rank_before_issue
        if rank_after_issue:
            payload["rankAfterIssue"] = rank_after_issue
        if rank_custom_field_id:
            payload["rankCustomFieldId"] = rank_custom_field_id

        response = await self.client.put(path, json=payload)
        response.raise_for_status()

    # ==================== Estimation ====================

    async def get_estimation(
        self,
        issue_id_or_key: str,
        board_id: int,
    ) -> IssueEstimation:
        """
        获取 Issue 估算

        GET /rest/agile/1.0/issue/{issueIdOrKey}/estimation

        Args:
            issue_id_or_key: Issue ID 或 Key
            board_id: 看板 ID（用于确定估算字段）

        Returns:
            IssueEstimation: 估算信息
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/estimation"
        params = {"boardId": board_id}
        data = await self.client.get_json(path, params=params)
        return IssueEstimation.model_validate(data)

    async def get_estimation_raw(
        self,
        issue_id_or_key: str,
        board_id: int,
    ) -> dict:
        """获取 Issue 估算（原始 JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/estimation"
        params = {"boardId": board_id}
        return await self.client.get_json(path, params=params)

    async def update_estimation(
        self,
        issue_id_or_key: str,
        board_id: int,
        value: str,
    ) -> IssueEstimation:
        """
        更新 Issue 估算

        PUT /rest/agile/1.0/issue/{issueIdOrKey}/estimation

        Args:
            issue_id_or_key: Issue ID 或 Key
            board_id: 看板 ID
            value: 估算值（如 "1w", "2d", "3h", "20m" 或分钟数）

        Returns:
            IssueEstimation: 更新后的估算信息
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/estimation"
        params = {"boardId": board_id}
        payload = {"value": value}
        data = await self.client.put_json(path, data=payload, params=params)
        return IssueEstimation.model_validate(data)

    async def update_estimation_raw(
        self,
        issue_id_or_key: str,
        board_id: int,
        value: str,
    ) -> dict:
        """更新 Issue 估算（原始 JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/estimation"
        params = {"boardId": board_id}
        payload = {"value": value}
        return await self.client.put_json(path, data=payload, params=params)
