"""
Myself Resource - 当前用户 API

GET /rest/api/2/myself
"""

from typing import Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.user import UserDetails


class MyselfResource(BaseResource):
    """
    当前用户资源

    API: /rest/api/2/myself
    """

    BASE_PATH = "/rest/api/2/myself"

    async def get(self, expand: Optional[str] = None) -> UserDetails:
        """
        获取当前登录用户信息

        GET /rest/api/2/myself

        Args:
            expand: 可选，展开的字段 (如 "groups,applicationRoles")

        Returns:
            UserDetails: 当前用户详细信息
        """
        params = {}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(self.BASE_PATH, params=params)
        return UserDetails.model_validate(data)

    async def get_raw(self, expand: Optional[str] = None) -> dict:
        """
        获取当前登录用户信息（原始 JSON）

        Args:
            expand: 可选，展开的字段

        Returns:
            dict: 原始 JSON 响应
        """
        params = {}
        if expand:
            params["expand"] = expand

        return await self.client.get_json(self.BASE_PATH, params=params)
