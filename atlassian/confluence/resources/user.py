"""
User Resource - User API

GET    /rest/api/user                                 - 获取用户（通过 username 或 key）
GET    /rest/api/user/current                         - 获取当前用户
GET    /rest/api/user/anonymous                       - 获取匿名用户

GET    /rest/api/user/watch/content/{contentId}       - 检查是否监视内容
POST   /rest/api/user/watch/content/{contentId}       - 监视内容
DELETE /rest/api/user/watch/content/{contentId}       - 取消监视内容

GET    /rest/api/user/watch/space/{spaceKey}          - 检查是否监视空间
POST   /rest/api/user/watch/space/{spaceKey}          - 监视空间
DELETE /rest/api/user/watch/space/{spaceKey}          - 取消监视空间
"""

from typing import Optional

from atlassian.common.base import BaseResource
from atlassian.confluence.models.user import User, UserWatch


class UserResource(BaseResource):
    """
    User 资源

    API: /rest/api/user
    """

    BASE_PATH = "/rest/api/user"

    # ========== User Info ==========

    async def get(
        self,
        username: Optional[str] = None,
        key: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> User:
        """
        获取用户信息

        GET /rest/api/user

        Args:
            username: 用户名
            key: 用户 key
            expand: 展开的字段

        Returns:
            User: 用户信息

        注意: username 和 key 必须提供其中一个
        """
        params = {}
        if username:
            params["username"] = username
        if key:
            params["key"] = key
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(self.BASE_PATH, params=params)
        return User.model_validate(data)

    async def get_raw(
        self,
        username: Optional[str] = None,
        key: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """
        获取用户信息（原始 JSON）

        Args:
            username: 用户名
            key: 用户 key
            expand: 展开的字段

        Returns:
            dict: 原始 JSON 响应
        """
        params = {}
        if username:
            params["username"] = username
        if key:
            params["key"] = key
        if expand:
            params["expand"] = expand

        return await self.client.get_json(self.BASE_PATH, params=params)

    async def get_current(self, expand: Optional[str] = None) -> User:
        """
        获取当前用户

        GET /rest/api/user/current

        Args:
            expand: 展开的字段

        Returns:
            User: 当前用户信息
        """
        params = {}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(f"{self.BASE_PATH}/current", params=params)
        return User.model_validate(data)

    async def get_current_raw(self, expand: Optional[str] = None) -> dict:
        """
        获取当前用户（原始 JSON）

        Args:
            expand: 展开的字段

        Returns:
            dict: 原始 JSON 响应
        """
        params = {}
        if expand:
            params["expand"] = expand

        return await self.client.get_json(f"{self.BASE_PATH}/current", params=params)

    async def get_anonymous(self, expand: Optional[str] = None) -> User:
        """
        获取匿名用户表示

        GET /rest/api/user/anonymous

        Args:
            expand: 展开的字段

        Returns:
            User: 匿名用户信息
        """
        params = {}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(f"{self.BASE_PATH}/anonymous", params=params)
        return User.model_validate(data)

    # ========== Content Watch ==========

    async def is_watching_content(
        self,
        content_id: str,
        username: Optional[str] = None,
        key: Optional[str] = None,
    ) -> UserWatch:
        """
        检查用户是否监视内容

        GET /rest/api/user/watch/content/{contentId}

        Args:
            content_id: 内容 ID
            username: 用户名（可选，默认当前用户）
            key: 用户 key（可选）

        Returns:
            UserWatch: 监视状态
        """
        path = f"{self.BASE_PATH}/watch/content/{content_id}"
        params = {}
        if username:
            params["username"] = username
        if key:
            params["key"] = key

        data = await self.client.get_json(path, params=params)
        return UserWatch.model_validate(data)

    async def watch_content(
        self,
        content_id: str,
        username: Optional[str] = None,
        key: Optional[str] = None,
    ) -> None:
        """
        监视内容

        POST /rest/api/user/watch/content/{contentId}

        Args:
            content_id: 内容 ID
            username: 用户名（可选，默认当前用户）
            key: 用户 key（可选）
        """
        path = f"{self.BASE_PATH}/watch/content/{content_id}"
        params = {}
        if username:
            params["username"] = username
        if key:
            params["key"] = key

        response = await self.client.post(path, params=params)
        response.raise_for_status()

    async def unwatch_content(
        self,
        content_id: str,
        username: Optional[str] = None,
        key: Optional[str] = None,
    ) -> None:
        """
        取消监视内容

        DELETE /rest/api/user/watch/content/{contentId}

        Args:
            content_id: 内容 ID
            username: 用户名（可选，默认当前用户）
            key: 用户 key（可选）
        """
        path = f"{self.BASE_PATH}/watch/content/{content_id}"
        params = {}
        if username:
            params["username"] = username
        if key:
            params["key"] = key

        response = await self.client.delete(path, params=params)
        response.raise_for_status()

    # ========== Space Watch ==========

    async def is_watching_space(
        self,
        space_key: str,
        username: Optional[str] = None,
        key: Optional[str] = None,
    ) -> UserWatch:
        """
        检查用户是否监视空间

        GET /rest/api/user/watch/space/{spaceKey}

        Args:
            space_key: 空间 key
            username: 用户名（可选，默认当前用户）
            key: 用户 key（可选）

        Returns:
            UserWatch: 监视状态
        """
        path = f"{self.BASE_PATH}/watch/space/{space_key}"
        params = {}
        if username:
            params["username"] = username
        if key:
            params["key"] = key

        data = await self.client.get_json(path, params=params)
        return UserWatch.model_validate(data)

    async def watch_space(
        self,
        space_key: str,
        username: Optional[str] = None,
        key: Optional[str] = None,
    ) -> None:
        """
        监视空间

        POST /rest/api/user/watch/space/{spaceKey}

        Args:
            space_key: 空间 key
            username: 用户名（可选，默认当前用户）
            key: 用户 key（可选）
        """
        path = f"{self.BASE_PATH}/watch/space/{space_key}"
        params = {}
        if username:
            params["username"] = username
        if key:
            params["key"] = key

        response = await self.client.post(path, params=params)
        response.raise_for_status()

    async def unwatch_space(
        self,
        space_key: str,
        username: Optional[str] = None,
        key: Optional[str] = None,
    ) -> None:
        """
        取消监视空间

        DELETE /rest/api/user/watch/space/{spaceKey}

        Args:
            space_key: 空间 key
            username: 用户名（可选，默认当前用户）
            key: 用户 key（可选）
        """
        path = f"{self.BASE_PATH}/watch/space/{space_key}"
        params = {}
        if username:
            params["username"] = username
        if key:
            params["key"] = key

        response = await self.client.delete(path, params=params)
        response.raise_for_status()
