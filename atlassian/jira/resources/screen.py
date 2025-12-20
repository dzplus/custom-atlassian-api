"""
Screen Resource - 屏幕资源

Screen CRUD:
GET    /rest/api/2/screens                            - 获取所有屏幕
POST   /rest/api/2/screens                            - 创建屏幕
PUT    /rest/api/2/screens/{screenId}                 - 更新屏幕
DELETE /rest/api/2/screens/{screenId}                 - 删除屏幕

Available Fields:
GET    /rest/api/2/screens/{screenId}/availableFields - 获取可用字段

Tabs:
GET    /rest/api/2/screens/{screenId}/tabs            - 获取所有Tab
POST   /rest/api/2/screens/{screenId}/tabs            - 创建Tab
PUT    /rest/api/2/screens/{screenId}/tabs/{tabId}    - 更新Tab
DELETE /rest/api/2/screens/{screenId}/tabs/{tabId}    - 删除Tab
POST   /rest/api/2/screens/{screenId}/tabs/{tabId}/move/{pos} - 移动Tab

Tab Fields:
GET    /rest/api/2/screens/{screenId}/tabs/{tabId}/fields - 获取Tab字段
POST   /rest/api/2/screens/{screenId}/tabs/{tabId}/fields - 添加字段到Tab
DELETE /rest/api/2/screens/{screenId}/tabs/{tabId}/fields/{id} - 从Tab移除字段
POST   /rest/api/2/screens/{screenId}/tabs/{tabId}/fields/{id}/move - 移动字段位置
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.field import Screen, ScreenTab, ScreenableField


class ScreenResource(BaseResource):
    """
    屏幕资源

    API: /rest/api/2/screens
    """

    BASE_PATH = "/rest/api/2/screens"

    # ==================== Screen CRUD ====================

    async def get_all(
        self,
        start_at: int = 0,
        max_results: int = 100,
    ) -> dict:
        """
        获取所有屏幕

        GET /rest/api/2/screens

        Args:
            start_at: 起始位置（默认0）
            max_results: 最大结果数（默认100）

        Returns:
            dict: 包含分页信息和屏幕列表
        """
        params = {
            "startAt": start_at,
            "maxResults": max_results,
        }

        return await self.client.get_json(self.BASE_PATH, params=params)

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
    ) -> Screen:
        """
        创建屏幕

        POST /rest/api/2/screens

        Args:
            name: 屏幕名称
            description: 屏幕描述（可选）

        Returns:
            Screen: 创建的屏幕
        """
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return Screen.model_validate(data)

    async def create_raw(
        self,
        name: str,
        description: Optional[str] = None,
    ) -> dict:
        """创建屏幕（原始JSON）"""
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def update(
        self,
        screen_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Screen:
        """
        更新屏幕

        PUT /rest/api/2/screens/{screenId}

        Args:
            screen_id: 屏幕ID
            name: 屏幕名称（可选）
            description: 屏幕描述（可选）

        Returns:
            Screen: 更新后的屏幕
        """
        path = f"{self.BASE_PATH}/{screen_id}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description

        data = await self.client.put_json(path, data=payload)
        return Screen.model_validate(data)

    async def update_raw(
        self,
        screen_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> dict:
        """更新屏幕（原始JSON）"""
        path = f"{self.BASE_PATH}/{screen_id}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description

        return await self.client.put_json(path, data=payload)

    async def delete(
        self,
        screen_id: str,
    ) -> None:
        """
        删除屏幕

        DELETE /rest/api/2/screens/{screenId}

        Args:
            screen_id: 屏幕ID
        """
        path = f"{self.BASE_PATH}/{screen_id}"
        await self.client.delete(path)

    # ==================== Available Fields ====================

    async def get_available_fields(
        self,
        screen_id: str,
    ) -> list[ScreenableField]:
        """
        获取屏幕可用字段

        GET /rest/api/2/screens/{screenId}/availableFields

        Args:
            screen_id: 屏幕ID

        Returns:
            list[ScreenableField]: 可用字段列表
        """
        path = f"{self.BASE_PATH}/{screen_id}/availableFields"
        data = await self.client.get_json(path)
        return [ScreenableField.model_validate(f) for f in data]

    async def get_available_fields_raw(
        self,
        screen_id: str,
    ) -> list[dict]:
        """获取屏幕可用字段（原始JSON）"""
        path = f"{self.BASE_PATH}/{screen_id}/availableFields"
        return await self.client.get_json(path)

    # ==================== Tabs ====================

    async def get_tabs(
        self,
        screen_id: str,
    ) -> list[ScreenTab]:
        """
        获取屏幕的所有Tab

        GET /rest/api/2/screens/{screenId}/tabs

        Args:
            screen_id: 屏幕ID

        Returns:
            list[ScreenTab]: Tab列表
        """
        path = f"{self.BASE_PATH}/{screen_id}/tabs"
        data = await self.client.get_json(path)
        return [ScreenTab.model_validate(t) for t in data]

    async def get_tabs_raw(
        self,
        screen_id: str,
    ) -> list[dict]:
        """获取屏幕的所有Tab（原始JSON）"""
        path = f"{self.BASE_PATH}/{screen_id}/tabs"
        return await self.client.get_json(path)

    async def create_tab(
        self,
        screen_id: str,
        name: str,
    ) -> ScreenTab:
        """
        创建Tab

        POST /rest/api/2/screens/{screenId}/tabs

        Args:
            screen_id: 屏幕ID
            name: Tab名称

        Returns:
            ScreenTab: 创建的Tab
        """
        path = f"{self.BASE_PATH}/{screen_id}/tabs"
        payload = {"name": name}

        data = await self.client.post_json(path, data=payload)
        return ScreenTab.model_validate(data)

    async def create_tab_raw(
        self,
        screen_id: str,
        name: str,
    ) -> dict:
        """创建Tab（原始JSON）"""
        path = f"{self.BASE_PATH}/{screen_id}/tabs"
        payload = {"name": name}

        return await self.client.post_json(path, data=payload)

    async def update_tab(
        self,
        screen_id: str,
        tab_id: str,
        name: str,
    ) -> ScreenTab:
        """
        更新Tab

        PUT /rest/api/2/screens/{screenId}/tabs/{tabId}

        Args:
            screen_id: 屏幕ID
            tab_id: Tab ID
            name: Tab名称

        Returns:
            ScreenTab: 更新后的Tab
        """
        path = f"{self.BASE_PATH}/{screen_id}/tabs/{tab_id}"
        payload = {"name": name}

        data = await self.client.put_json(path, data=payload)
        return ScreenTab.model_validate(data)

    async def update_tab_raw(
        self,
        screen_id: str,
        tab_id: str,
        name: str,
    ) -> dict:
        """更新Tab（原始JSON）"""
        path = f"{self.BASE_PATH}/{screen_id}/tabs/{tab_id}"
        payload = {"name": name}

        return await self.client.put_json(path, data=payload)

    async def delete_tab(
        self,
        screen_id: str,
        tab_id: str,
    ) -> None:
        """
        删除Tab

        DELETE /rest/api/2/screens/{screenId}/tabs/{tabId}

        Args:
            screen_id: 屏幕ID
            tab_id: Tab ID
        """
        path = f"{self.BASE_PATH}/{screen_id}/tabs/{tab_id}"
        await self.client.delete(path)

    async def move_tab(
        self,
        screen_id: str,
        tab_id: str,
        position: int,
    ) -> dict:
        """
        移动Tab位置

        POST /rest/api/2/screens/{screenId}/tabs/{tabId}/move/{pos}

        Args:
            screen_id: 屏幕ID
            tab_id: Tab ID
            position: 新位置

        Returns:
            dict: 操作结果
        """
        path = f"{self.BASE_PATH}/{screen_id}/tabs/{tab_id}/move/{position}"
        return await self.client.post_json(path, data=None)

    # ==================== Tab Fields ====================

    async def get_tab_fields(
        self,
        screen_id: str,
        tab_id: str,
    ) -> list[ScreenableField]:
        """
        获取Tab的所有字段

        GET /rest/api/2/screens/{screenId}/tabs/{tabId}/fields

        Args:
            screen_id: 屏幕ID
            tab_id: Tab ID

        Returns:
            list[ScreenableField]: 字段列表
        """
        path = f"{self.BASE_PATH}/{screen_id}/tabs/{tab_id}/fields"
        data = await self.client.get_json(path)
        return [ScreenableField.model_validate(f) for f in data]

    async def get_tab_fields_raw(
        self,
        screen_id: str,
        tab_id: str,
    ) -> list[dict]:
        """获取Tab的所有字段（原始JSON）"""
        path = f"{self.BASE_PATH}/{screen_id}/tabs/{tab_id}/fields"
        return await self.client.get_json(path)

    async def add_field_to_tab(
        self,
        screen_id: str,
        tab_id: str,
        field_id: str,
    ) -> ScreenableField:
        """
        添加字段到Tab

        POST /rest/api/2/screens/{screenId}/tabs/{tabId}/fields

        Args:
            screen_id: 屏幕ID
            tab_id: Tab ID
            field_id: 字段ID

        Returns:
            ScreenableField: 添加的字段
        """
        path = f"{self.BASE_PATH}/{screen_id}/tabs/{tab_id}/fields"
        payload = {"fieldId": field_id}

        data = await self.client.post_json(path, data=payload)
        return ScreenableField.model_validate(data)

    async def add_field_to_tab_raw(
        self,
        screen_id: str,
        tab_id: str,
        field_id: str,
    ) -> dict:
        """添加字段到Tab（原始JSON）"""
        path = f"{self.BASE_PATH}/{screen_id}/tabs/{tab_id}/fields"
        payload = {"fieldId": field_id}

        return await self.client.post_json(path, data=payload)

    async def remove_field_from_tab(
        self,
        screen_id: str,
        tab_id: str,
        field_id: str,
    ) -> None:
        """
        从Tab移除字段

        DELETE /rest/api/2/screens/{screenId}/tabs/{tabId}/fields/{id}

        Args:
            screen_id: 屏幕ID
            tab_id: Tab ID
            field_id: 字段ID
        """
        path = f"{self.BASE_PATH}/{screen_id}/tabs/{tab_id}/fields/{field_id}"
        await self.client.delete(path)

    async def move_field_to_position(
        self,
        screen_id: str,
        tab_id: str,
        field_id: str,
        position: int,
    ) -> dict:
        """
        移动字段到指定位置

        POST /rest/api/2/screens/{screenId}/tabs/{tabId}/fields/{id}/move

        Args:
            screen_id: 屏幕ID
            tab_id: Tab ID
            field_id: 字段ID
            position: 目标位置

        Returns:
            dict: 操作结果
        """
        path = f"{self.BASE_PATH}/{screen_id}/tabs/{tab_id}/fields/{field_id}/move"
        payload = {"position": position}

        return await self.client.post_json(path, data=payload)
