"""
Space Resource - Space API

GET    /rest/api/space                                - 获取空间列表
POST   /rest/api/space                                - 创建公共空间
POST   /rest/api/space/_private                       - 创建私有空间
GET    /rest/api/space/{spaceKey}                     - 获取空间
PUT    /rest/api/space/{spaceKey}                     - 更新空间
DELETE /rest/api/space/{spaceKey}                     - 删除空间

GET    /rest/api/space/{spaceKey}/content             - 获取空间内容
GET    /rest/api/space/{spaceKey}/content/{type}      - 获取空间指定类型内容

GET    /rest/api/space/{spaceKey}/property            - 获取空间属性列表
POST   /rest/api/space/{spaceKey}/property            - 创建空间属性
GET    /rest/api/space/{spaceKey}/property/{key}      - 获取空间属性
PUT    /rest/api/space/{spaceKey}/property/{key}      - 更新空间属性
DELETE /rest/api/space/{spaceKey}/property/{key}      - 删除空间属性
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.confluence.models.space import (
    Space,
    SpaceList,
    SpaceProperty,
    SpacePropertyList,
)
from atlassian.confluence.models.content import ContentList


class SpaceResource(BaseResource):
    """
    Space 资源

    API: /rest/api/space
    """

    BASE_PATH = "/rest/api/space"

    # ========== Space CRUD ==========

    async def get_all(
        self,
        space_key: Optional[list[str]] = None,
        type: Optional[str] = None,
        status: Optional[str] = None,
        label: Optional[str] = None,
        favourite: Optional[bool] = None,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
    ) -> SpaceList:
        """
        获取空间列表

        GET /rest/api/space

        Args:
            space_key: 空间 key 列表筛选
            type: 空间类型 (global, personal)
            status: 状态 (current, archived)
            label: 标签筛选
            favourite: 是否仅返回收藏的空间
            expand: 展开的字段
            start: 起始位置
            limit: 返回数量

        Returns:
            SpaceList: 空间列表
        """
        params: dict[str, Any] = {"start": start, "limit": limit}
        if space_key:
            params["spaceKey"] = ",".join(space_key)
        if type:
            params["type"] = type
        if status:
            params["status"] = status
        if label:
            params["label"] = label
        if favourite is not None:
            params["favourite"] = str(favourite).lower()
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(self.BASE_PATH, params=params)
        return SpaceList.model_validate(data)

    async def get(
        self,
        space_key: str,
        expand: Optional[str] = None,
    ) -> Space:
        """
        获取空间详情

        GET /rest/api/space/{spaceKey}

        Args:
            space_key: 空间 key
            expand: 展开的字段

        Returns:
            Space: 空间详情
        """
        path = f"{self.BASE_PATH}/{space_key}"
        params: dict[str, Any] = {}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return Space.model_validate(data)

    async def get_raw(
        self,
        space_key: str,
        expand: Optional[str] = None,
    ) -> dict:
        """
        获取空间详情（原始 JSON）

        Args:
            space_key: 空间 key
            expand: 展开的字段

        Returns:
            dict: 原始 JSON 响应
        """
        path = f"{self.BASE_PATH}/{space_key}"
        params: dict[str, Any] = {}
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    async def create(
        self,
        key: str,
        name: str,
        description: Optional[str] = None,
        private: bool = False,
    ) -> Space:
        """
        创建空间

        POST /rest/api/space 或 /rest/api/space/_private

        Args:
            key: 空间 key
            name: 空间名称
            description: 空间描述
            private: 是否为私有空间

        Returns:
            Space: 创建的空间
        """
        path = f"{self.BASE_PATH}/_private" if private else self.BASE_PATH
        payload: dict[str, Any] = {
            "key": key,
            "name": name,
        }

        if description:
            payload["description"] = {
                "plain": {
                    "value": description,
                    "representation": "plain",
                }
            }

        data = await self.client.post_json(path, data=payload)
        return Space.model_validate(data)

    async def create_raw(self, payload: dict, private: bool = False) -> dict:
        """
        使用原始 payload 创建空间

        Args:
            payload: 原始请求体
            private: 是否为私有空间

        Returns:
            dict: 创建结果
        """
        path = f"{self.BASE_PATH}/_private" if private else self.BASE_PATH
        return await self.client.post_json(path, data=payload)

    async def update(
        self,
        space_key: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        homepage_id: Optional[str] = None,
    ) -> Space:
        """
        更新空间

        PUT /rest/api/space/{spaceKey}

        Args:
            space_key: 空间 key
            name: 新名称
            description: 新描述
            homepage_id: 新主页 ID

        Returns:
            Space: 更新后的空间
        """
        path = f"{self.BASE_PATH}/{space_key}"
        payload: dict[str, Any] = {}

        if name:
            payload["name"] = name
        if description:
            payload["description"] = {
                "plain": {
                    "value": description,
                    "representation": "plain",
                }
            }
        if homepage_id:
            payload["homepage"] = {"id": homepage_id}

        data = await self.client.put_json(path, data=payload)
        return Space.model_validate(data)

    async def update_raw(self, space_key: str, payload: dict) -> dict:
        """
        使用原始 payload 更新空间

        Args:
            space_key: 空间 key
            payload: 原始请求体

        Returns:
            dict: 更新结果
        """
        path = f"{self.BASE_PATH}/{space_key}"
        return await self.client.put_json(path, data=payload)

    async def delete(self, space_key: str) -> dict:
        """
        删除空间

        DELETE /rest/api/space/{spaceKey}

        注意: 删除是异步的，返回任务指针

        Args:
            space_key: 空间 key

        Returns:
            dict: 删除任务信息
        """
        path = f"{self.BASE_PATH}/{space_key}"
        response = await self.client.delete(path)
        response.raise_for_status()
        return response.json()

    # ========== Space Content ==========

    async def get_content(
        self,
        space_key: str,
        depth: str = "all",
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
    ) -> ContentList:
        """
        获取空间内容

        GET /rest/api/space/{spaceKey}/content

        Args:
            space_key: 空间 key
            depth: 深度 (all, root)
            expand: 展开的字段
            start: 起始位置
            limit: 返回数量

        Returns:
            ContentList: 内容列表
        """
        path = f"{self.BASE_PATH}/{space_key}/content"
        params: dict[str, Any] = {
            "depth": depth,
            "start": start,
            "limit": limit,
        }
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return ContentList.model_validate(data)

    async def get_content_by_type(
        self,
        space_key: str,
        content_type: str,
        depth: str = "all",
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
    ) -> ContentList:
        """
        获取空间指定类型内容

        GET /rest/api/space/{spaceKey}/content/{type}

        Args:
            space_key: 空间 key
            content_type: 内容类型 (page, blogpost)
            depth: 深度 (all, root)
            expand: 展开的字段
            start: 起始位置
            limit: 返回数量

        Returns:
            ContentList: 内容列表
        """
        path = f"{self.BASE_PATH}/{space_key}/content/{content_type}"
        params: dict[str, Any] = {
            "depth": depth,
            "start": start,
            "limit": limit,
        }
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return ContentList.model_validate(data)

    # ========== Space Properties ==========

    async def get_properties(
        self,
        space_key: str,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
    ) -> SpacePropertyList:
        """
        获取空间属性列表

        GET /rest/api/space/{spaceKey}/property

        Args:
            space_key: 空间 key
            expand: 展开的字段
            start: 起始位置
            limit: 返回数量

        Returns:
            SpacePropertyList: 属性列表
        """
        path = f"{self.BASE_PATH}/{space_key}/property"
        params: dict[str, Any] = {"start": start, "limit": limit}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return SpacePropertyList.model_validate(data)

    async def get_property(
        self,
        space_key: str,
        key: str,
        expand: Optional[str] = None,
    ) -> SpaceProperty:
        """
        获取空间属性

        GET /rest/api/space/{spaceKey}/property/{key}

        Args:
            space_key: 空间 key
            key: 属性 key
            expand: 展开的字段

        Returns:
            SpaceProperty: 属性
        """
        path = f"{self.BASE_PATH}/{space_key}/property/{key}"
        params: dict[str, Any] = {}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return SpaceProperty.model_validate(data)

    async def create_property(
        self,
        space_key: str,
        key: str,
        value: Any,
    ) -> SpaceProperty:
        """
        创建空间属性

        POST /rest/api/space/{spaceKey}/property

        Args:
            space_key: 空间 key
            key: 属性 key
            value: 属性值

        Returns:
            SpaceProperty: 创建的属性
        """
        path = f"{self.BASE_PATH}/{space_key}/property"
        payload = {"key": key, "value": value}

        data = await self.client.post_json(path, data=payload)
        return SpaceProperty.model_validate(data)

    async def update_property(
        self,
        space_key: str,
        key: str,
        value: Any,
        version_number: int,
    ) -> SpaceProperty:
        """
        更新空间属性

        PUT /rest/api/space/{spaceKey}/property/{key}

        Args:
            space_key: 空间 key
            key: 属性 key
            value: 属性值
            version_number: 新版本号

        Returns:
            SpaceProperty: 更新的属性
        """
        path = f"{self.BASE_PATH}/{space_key}/property/{key}"
        payload = {
            "key": key,
            "value": value,
            "version": {"number": version_number},
        }

        data = await self.client.put_json(path, data=payload)
        return SpaceProperty.model_validate(data)

    async def delete_property(self, space_key: str, key: str) -> None:
        """
        删除空间属性

        DELETE /rest/api/space/{spaceKey}/property/{key}

        Args:
            space_key: 空间 key
            key: 属性 key
        """
        path = f"{self.BASE_PATH}/{space_key}/property/{key}"
        response = await self.client.delete(path)
        response.raise_for_status()
