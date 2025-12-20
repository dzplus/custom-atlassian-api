"""
Status Resource - 状态资源

GET /rest/api/2/status         - 获取所有状态
GET /rest/api/2/status/{id}    - 获取状态详情
"""

from typing import Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.issue import Status


class StatusResource(BaseResource):
    """
    状态资源

    API: /rest/api/2/status
    """

    BASE_PATH = "/rest/api/2/status"

    async def get_all(self) -> list[Status]:
        """
        获取所有状态

        GET /rest/api/2/status

        Returns:
            list[Status]: 状态列表
        """
        data = await self.client.get_json(self.BASE_PATH)
        return [Status.model_validate(s) for s in data]

    async def get_all_raw(self) -> list[dict]:
        """获取所有状态（原始JSON）"""
        return await self.client.get_json(self.BASE_PATH)

    async def get(
        self,
        status_id: str,
    ) -> Status:
        """
        获取状态详情

        GET /rest/api/2/status/{id}

        Args:
            status_id: 状态ID

        Returns:
            Status: 状态详情
        """
        path = f"{self.BASE_PATH}/{status_id}"
        data = await self.client.get_json(path)
        return Status.model_validate(data)

    async def get_raw(
        self,
        status_id: str,
    ) -> dict:
        """获取状态详情（原始JSON）"""
        path = f"{self.BASE_PATH}/{status_id}"
        return await self.client.get_json(path)
