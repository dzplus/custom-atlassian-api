"""
Backlog Resource - Backlog API

POST /rest/agile/1.0/backlog/issue - 移动 Issue 到 Backlog
"""

from atlassian.common.base import BaseResource


class BacklogResource(BaseResource):
    """
    Backlog 资源

    API: /rest/agile/1.0/backlog
    """

    BASE_PATH = "/rest/agile/1.0/backlog"

    async def move_issues(self, issues: list[str]) -> None:
        """
        移动 Issue 到 Backlog

        POST /rest/agile/1.0/backlog/issue

        将 Issue 从当前 Sprint 移除，放入 Backlog。
        相当于清除 Issue 的 future 和 active Sprint。

        Args:
            issues: Issue Key 或 ID 列表（最多50个）
        """
        path = f"{self.BASE_PATH}/issue"
        payload = {"issues": issues}
        response = await self.client.post(path, json=payload)
        response.raise_for_status()
