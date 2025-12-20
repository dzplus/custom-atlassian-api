"""
Issue Type Resource - Issue类型资源

IssueType CRUD:
GET    /rest/api/2/issuetype                  - 获取所有Issue类型
POST   /rest/api/2/issuetype                  - 创建Issue类型
GET    /rest/api/2/issuetype/{id}             - 获取Issue类型
PUT    /rest/api/2/issuetype/{id}             - 更新Issue类型
DELETE /rest/api/2/issuetype/{id}             - 删除Issue类型

Alternatives:
GET    /rest/api/2/issuetype/{id}/alternatives - 获取替代Issue类型

Avatar:
POST   /rest/api/2/issuetype/{id}/avatar2     - 创建Avatar
GET    /rest/api/2/issuetype/{id}/avatar2     - 获取Avatars
DELETE /rest/api/2/issuetype/{id}/avatar2/{avatarId} - 删除Avatar

Properties:
GET    /rest/api/2/issuetype/{issueTypeId}/properties - 获取所有属性
GET    /rest/api/2/issuetype/{issueTypeId}/properties/{propertyKey} - 获取属性
PUT    /rest/api/2/issuetype/{issueTypeId}/properties/{propertyKey} - 设置属性
DELETE /rest/api/2/issuetype/{issueTypeId}/properties/{propertyKey} - 删除属性
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.issue import IssueType
from atlassian.jira.models.avatar import Avatar
from atlassian.jira.models.common import EntityPropertyKeys


class IssueTypeResource(BaseResource):
    """
    Issue类型资源

    API: /rest/api/2/issuetype
    """

    BASE_PATH = "/rest/api/2/issuetype"

    # ==================== IssueType CRUD ====================

    async def get_all(self) -> list[IssueType]:
        """
        获取所有Issue类型

        GET /rest/api/2/issuetype

        Returns:
            list[IssueType]: Issue类型列表
        """
        data = await self.client.get_json(self.BASE_PATH)
        return [IssueType.model_validate(it) for it in data]

    async def get_all_raw(self) -> list[dict]:
        """获取所有Issue类型（原始JSON）"""
        return await self.client.get_json(self.BASE_PATH)

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        type: str = "standard",
    ) -> IssueType:
        """
        创建Issue类型

        POST /rest/api/2/issuetype

        Args:
            name: Issue类型名称
            description: 描述（可选）
            type: 类型，"standard"或"subtask"（默认"standard"）

        Returns:
            IssueType: 创建的Issue类型
        """
        payload: dict[str, Any] = {
            "name": name,
            "type": type,
        }
        if description:
            payload["description"] = description

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return IssueType.model_validate(data)

    async def create_raw(
        self,
        name: str,
        description: Optional[str] = None,
        type: str = "standard",
    ) -> dict:
        """创建Issue类型（原始JSON）"""
        payload: dict[str, Any] = {
            "name": name,
            "type": type,
        }
        if description:
            payload["description"] = description

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def get(
        self,
        issue_type_id: str,
    ) -> IssueType:
        """
        获取Issue类型详情

        GET /rest/api/2/issuetype/{id}

        Args:
            issue_type_id: Issue类型ID

        Returns:
            IssueType: Issue类型详情
        """
        path = f"{self.BASE_PATH}/{issue_type_id}"
        data = await self.client.get_json(path)
        return IssueType.model_validate(data)

    async def get_raw(
        self,
        issue_type_id: str,
    ) -> dict:
        """获取Issue类型详情（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_type_id}"
        return await self.client.get_json(path)

    async def update(
        self,
        issue_type_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        avatar_id: Optional[str] = None,
    ) -> IssueType:
        """
        更新Issue类型

        PUT /rest/api/2/issuetype/{id}

        Args:
            issue_type_id: Issue类型ID
            name: Issue类型名称（可选）
            description: 描述（可选）
            avatar_id: Avatar ID（可选）

        Returns:
            IssueType: 更新后的Issue类型
        """
        path = f"{self.BASE_PATH}/{issue_type_id}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if avatar_id:
            payload["avatarId"] = avatar_id

        data = await self.client.put_json(path, data=payload)
        return IssueType.model_validate(data)

    async def update_raw(
        self,
        issue_type_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        avatar_id: Optional[str] = None,
    ) -> dict:
        """更新Issue类型（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_type_id}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if avatar_id:
            payload["avatarId"] = avatar_id

        return await self.client.put_json(path, data=payload)

    async def delete(
        self,
        issue_type_id: str,
        alternative_issue_type_id: Optional[str] = None,
    ) -> None:
        """
        删除Issue类型

        DELETE /rest/api/2/issuetype/{id}

        Args:
            issue_type_id: 要删除的Issue类型ID
            alternative_issue_type_id: 替代Issue类型ID（可选）
        """
        path = f"{self.BASE_PATH}/{issue_type_id}"
        params = {}
        if alternative_issue_type_id:
            params["alternativeIssueTypeId"] = alternative_issue_type_id

        await self.client.delete(path, params=params)

    # ==================== Alternatives ====================

    async def get_alternative_issue_types(
        self,
        issue_type_id: str,
    ) -> list[IssueType]:
        """
        获取替代Issue类型

        GET /rest/api/2/issuetype/{id}/alternatives

        Args:
            issue_type_id: Issue类型ID

        Returns:
            list[IssueType]: 可用的替代Issue类型列表
        """
        path = f"{self.BASE_PATH}/{issue_type_id}/alternatives"
        data = await self.client.get_json(path)
        return [IssueType.model_validate(it) for it in data]

    async def get_alternative_issue_types_raw(
        self,
        issue_type_id: str,
    ) -> list[dict]:
        """获取替代Issue类型（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_type_id}/alternatives"
        return await self.client.get_json(path)

    # ==================== Avatar ====================

    async def create_avatar(
        self,
        issue_type_id: str,
        file_path: str,
        filename: Optional[str] = None,
        size: int = 0,
        x: int = 0,
        y: int = 0,
    ) -> Avatar:
        """
        创建Issue类型Avatar

        POST /rest/api/2/issuetype/{id}/avatar2

        Args:
            issue_type_id: Issue类型ID
            file_path: 文件路径
            filename: 文件名（可选）
            size: 裁剪尺寸（默认0）
            x: 裁剪X坐标（默认0）
            y: 裁剪Y坐标（默认0）

        Returns:
            Avatar: 创建的Avatar
        """
        path = f"{self.BASE_PATH}/{issue_type_id}/avatar2"
        params = {
            "x": x,
            "y": y,
            "size": size,
        }

        if filename is None:
            filename = file_path.split("/")[-1]

        with open(file_path, "rb") as f:
            files = {"file": (filename, f, "application/octet-stream")}
            data = await self.client.post_multipart(path, files=files, params=params)

        return Avatar.model_validate(data)

    async def create_avatar_raw(
        self,
        issue_type_id: str,
        file_path: str,
        filename: Optional[str] = None,
        size: int = 0,
        x: int = 0,
        y: int = 0,
    ) -> dict:
        """创建Issue类型Avatar（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_type_id}/avatar2"
        params = {
            "x": x,
            "y": y,
            "size": size,
        }

        if filename is None:
            filename = file_path.split("/")[-1]

        with open(file_path, "rb") as f:
            files = {"file": (filename, f, "application/octet-stream")}
            return await self.client.post_multipart(path, files=files, params=params)

    async def get_avatars(
        self,
        issue_type_id: str,
    ) -> list[Avatar]:
        """
        获取Issue类型的所有Avatars

        GET /rest/api/2/issuetype/{id}/avatar2

        Args:
            issue_type_id: Issue类型ID

        Returns:
            list[Avatar]: Avatar列表
        """
        path = f"{self.BASE_PATH}/{issue_type_id}/avatar2"
        data = await self.client.get_json(path)
        # API返回 {"system": [...], "custom": [...]}
        avatars = []
        if "system" in data:
            avatars.extend([Avatar.model_validate(a) for a in data["system"]])
        if "custom" in data:
            avatars.extend([Avatar.model_validate(a) for a in data["custom"]])
        return avatars

    async def get_avatars_raw(
        self,
        issue_type_id: str,
    ) -> dict:
        """获取Issue类型的所有Avatars（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_type_id}/avatar2"
        return await self.client.get_json(path)

    async def delete_avatar(
        self,
        issue_type_id: str,
        avatar_id: str,
    ) -> None:
        """
        删除Issue类型Avatar

        DELETE /rest/api/2/issuetype/{id}/avatar2/{avatarId}

        Args:
            issue_type_id: Issue类型ID
            avatar_id: Avatar ID
        """
        path = f"{self.BASE_PATH}/{issue_type_id}/avatar2/{avatar_id}"
        await self.client.delete(path)

    # ==================== Properties ====================

    async def get_properties(
        self,
        issue_type_id: str,
    ) -> EntityPropertyKeys:
        """
        获取Issue类型的所有属性键

        GET /rest/api/2/issuetype/{issueTypeId}/properties

        Args:
            issue_type_id: Issue类型ID

        Returns:
            EntityPropertyKeys: 属性键列表
        """
        path = f"{self.BASE_PATH}/{issue_type_id}/properties"
        data = await self.client.get_json(path)
        return EntityPropertyKeys.model_validate(data)

    async def get_properties_raw(
        self,
        issue_type_id: str,
    ) -> dict:
        """获取Issue类型的所有属性键（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_type_id}/properties"
        return await self.client.get_json(path)

    async def get_property(
        self,
        issue_type_id: str,
        property_key: str,
    ) -> dict:
        """
        获取Issue类型属性值

        GET /rest/api/2/issuetype/{issueTypeId}/properties/{propertyKey}

        Args:
            issue_type_id: Issue类型ID
            property_key: 属性键

        Returns:
            dict: 属性值
        """
        path = f"{self.BASE_PATH}/{issue_type_id}/properties/{property_key}"
        return await self.client.get_json(path)

    async def set_property(
        self,
        issue_type_id: str,
        property_key: str,
        value: Any,
    ) -> dict:
        """
        设置Issue类型属性

        PUT /rest/api/2/issuetype/{issueTypeId}/properties/{propertyKey}

        Args:
            issue_type_id: Issue类型ID
            property_key: 属性键
            value: 属性值

        Returns:
            dict: 操作结果
        """
        path = f"{self.BASE_PATH}/{issue_type_id}/properties/{property_key}"
        return await self.client.put_json(path, data=value)

    async def delete_property(
        self,
        issue_type_id: str,
        property_key: str,
    ) -> None:
        """
        删除Issue类型属性

        DELETE /rest/api/2/issuetype/{issueTypeId}/properties/{propertyKey}

        Args:
            issue_type_id: Issue类型ID
            property_key: 属性键
        """
        path = f"{self.BASE_PATH}/{issue_type_id}/properties/{property_key}"
        await self.client.delete(path)
