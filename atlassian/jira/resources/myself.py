"""
Myself Resource - 当前用户 API

GET /rest/api/2/myself                  - 获取当前用户
PUT /rest/api/2/myself                  - 更新当前用户
PUT /rest/api/2/myself/password         - 修改密码
"""

from typing import Any, Optional

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

    async def update(
        self,
        email: Optional[str] = None,
        display_name: Optional[str] = None,
    ) -> UserDetails:
        """
        更新当前用户信息

        PUT /rest/api/2/myself

        Args:
            email: 新的邮箱地址（可选）
            display_name: 新的显示名称（可选）

        Returns:
            UserDetails: 更新后的用户详细信息
        """
        payload: dict[str, Any] = {}
        if email:
            payload["emailAddress"] = email
        if display_name:
            payload["displayName"] = display_name

        data = await self.client.put_json(self.BASE_PATH, data=payload)
        return UserDetails.model_validate(data)

    async def update_raw(
        self,
        email: Optional[str] = None,
        display_name: Optional[str] = None,
    ) -> dict:
        """更新当前用户信息（原始JSON）"""
        payload: dict[str, Any] = {}
        if email:
            payload["emailAddress"] = email
        if display_name:
            payload["displayName"] = display_name

        return await self.client.put_json(self.BASE_PATH, data=payload)

    async def change_password(
        self,
        current_password: str,
        new_password: str,
    ) -> None:
        """
        修改当前用户密码

        PUT /rest/api/2/myself/password

        Args:
            current_password: 当前密码
            new_password: 新密码
        """
        path = f"{self.BASE_PATH}/password"
        payload = {
            "password": current_password,
            "currentPassword": current_password,
            "newPassword": new_password,
        }

        await self.client.put_json(path, data=payload)
