"""
Group Resource - 用户组 API

GET    /rest/api/group                  - 获取用户组列表
GET    /rest/api/group/{groupName}      - 获取指定用户组
GET    /rest/api/group/{groupName}/member - 获取组成员
"""

from typing import Optional
from atlassian.common.base import BaseResource


class GroupResource(BaseResource):
    """
    用户组资源

    API: /rest/api/group
    """

    BASE_PATH = "/rest/api/group"

    async def get_all(
        self,
        start: int = 0,
        limit: int = 200,
    ) -> dict:
        """
        获取用户组列表

        GET /rest/api/group

        Args:
            start: 起始位置
            limit: 返回数量（最大200）

        Returns:
            dict: 用户组列表
            {
                "results": [
                    {
                        "type": "group",
                        "name": "confluence-users",
                        "_links": {...}
                    }
                ],
                "start": 0,
                "limit": 200,
                "size": 1
            }
        """
        params = {
            "start": start,
            "limit": limit,
        }
        return await self.client.get_json(self.BASE_PATH, params=params)

    async def get(
        self,
        group_name: str,
        expand: Optional[str] = None,
    ) -> dict:
        """
        获取指定用户组信息

        GET /rest/api/group/{groupName}

        Args:
            group_name: 用户组名称
            expand: 展开的字段

        Returns:
            dict: 用户组信息
            {
                "type": "group",
                "name": "confluence-users",
                "_links": {...}
            }
        """
        path = f"{self.BASE_PATH}/{group_name}"
        params = {}
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    async def get_members(
        self,
        group_name: str,
        start: int = 0,
        limit: int = 200,
        expand: Optional[str] = None,
    ) -> dict:
        """
        获取用户组成员列表

        GET /rest/api/group/{groupName}/member

        Args:
            group_name: 用户组名称
            start: 起始位置
            limit: 返回数量（最大200）
            expand: 展开的字段

        Returns:
            dict: 成员列表
            {
                "results": [
                    {
                        "type": "known",
                        "username": "admin",
                        "userKey": "...",
                        "profilePicture": {...},
                        "displayName": "Admin",
                        "_links": {...}
                    }
                ],
                "start": 0,
                "limit": 200,
                "size": 1
            }
        """
        path = f"{self.BASE_PATH}/{group_name}/member"
        params = {
            "start": start,
            "limit": limit,
        }
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)
