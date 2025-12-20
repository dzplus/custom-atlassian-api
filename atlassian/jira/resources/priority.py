"""
Priority Resource - 优先级资源

GET /rest/api/2/priority         - 获取所有优先级
GET /rest/api/2/priority/{id}    - 获取优先级详情
"""

from typing import Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.issue import Priority


class PriorityResource(BaseResource):
    """
    优先级资源

    API: /rest/api/2/priority
    """

    BASE_PATH = "/rest/api/2/priority"

    async def get_all(self) -> list[Priority]:
        """
        获取所有优先级

        GET /rest/api/2/priority

        Returns:
            list[Priority]: 优先级列表
        """
        data = await self.client.get_json(self.BASE_PATH)
        return [Priority.model_validate(p) for p in data]

    async def get_all_raw(self) -> list[dict]:
        """获取所有优先级（原始JSON）"""
        return await self.client.get_json(self.BASE_PATH)

    async def get(
        self,
        priority_id: str,
    ) -> Priority:
        """
        获取优先级详情

        GET /rest/api/2/priority/{id}

        Args:
            priority_id: 优先级ID

        Returns:
            Priority: 优先级详情
        """
        path = f"{self.BASE_PATH}/{priority_id}"
        data = await self.client.get_json(path)
        return Priority.model_validate(data)

    async def get_raw(
        self,
        priority_id: str,
    ) -> dict:
        """获取优先级详情（原始JSON）"""
        path = f"{self.BASE_PATH}/{priority_id}"
        return await self.client.get_json(path)
