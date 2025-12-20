"""
Resolution Resource - 解决方案资源

GET /rest/api/2/resolution         - 获取所有解决方案
GET /rest/api/2/resolution/{id}    - 获取解决方案详情
"""

from typing import Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.issue import Resolution


class ResolutionResource(BaseResource):
    """
    解决方案资源

    API: /rest/api/2/resolution
    """

    BASE_PATH = "/rest/api/2/resolution"

    async def get_all(self) -> list[Resolution]:
        """
        获取所有解决方案

        GET /rest/api/2/resolution

        Returns:
            list[Resolution]: 解决方案列表
        """
        data = await self.client.get_json(self.BASE_PATH)
        return [Resolution.model_validate(r) for r in data]

    async def get_all_raw(self) -> list[dict]:
        """获取所有解决方案（原始JSON）"""
        return await self.client.get_json(self.BASE_PATH)

    async def get(
        self,
        resolution_id: str,
    ) -> Resolution:
        """
        获取解决方案详情

        GET /rest/api/2/resolution/{id}

        Args:
            resolution_id: 解决方案ID

        Returns:
            Resolution: 解决方案详情
        """
        path = f"{self.BASE_PATH}/{resolution_id}"
        data = await self.client.get_json(path)
        return Resolution.model_validate(data)

    async def get_raw(
        self,
        resolution_id: str,
    ) -> dict:
        """获取解决方案详情（原始JSON）"""
        path = f"{self.BASE_PATH}/{resolution_id}"
        return await self.client.get_json(path)
