"""
Security Level Resource - 安全级别资源

GET /rest/api/2/securitylevel/{id} - 获取安全级别详情
"""

from typing import Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.permission import SecurityLevel


class SecurityLevelResource(BaseResource):
    """
    安全级别资源

    API: /rest/api/2/securitylevel
    """

    BASE_PATH = "/rest/api/2/securitylevel"

    async def get(
        self,
        level_id: str,
    ) -> SecurityLevel:
        """
        获取安全级别详情

        GET /rest/api/2/securitylevel/{id}

        Args:
            level_id: 安全级别ID

        Returns:
            SecurityLevel: 安全级别详情
        """
        path = f"{self.BASE_PATH}/{level_id}"
        data = await self.client.get_json(path)
        return SecurityLevel.model_validate(data)

    async def get_raw(
        self,
        level_id: str,
    ) -> dict:
        """获取安全级别详情（原始JSON）"""
        path = f"{self.BASE_PATH}/{level_id}"
        return await self.client.get_json(path)
