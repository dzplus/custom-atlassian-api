"""
Issue Link Type Resource - Issue 链接类型 API

GET    /rest/api/2/issueLinkType                    - 获取所有链接类型
POST   /rest/api/2/issueLinkType                    - 创建链接类型
GET    /rest/api/2/issueLinkType/{issueLinkTypeId}  - 获取指定链接类型
PUT    /rest/api/2/issueLinkType/{issueLinkTypeId}  - 更新链接类型
DELETE /rest/api/2/issueLinkType/{issueLinkTypeId}  - 删除链接类型
"""

from typing import Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.issue_link import IssueLinkType, IssueLinkTypeList


class IssueLinkTypeResource(BaseResource):
    """
    Issue 链接类型资源

    API: /rest/api/2/issueLinkType
    """

    BASE_PATH = "/rest/api/2/issueLinkType"

    async def get_all(self) -> list[IssueLinkType]:
        """
        获取所有 Issue 链接类型

        GET /rest/api/2/issueLinkType

        Returns:
            list[IssueLinkType]: 链接类型列表
        """
        data = await self.client.get_json(self.BASE_PATH)
        result = IssueLinkTypeList.model_validate(data)
        return result.issue_link_types

    async def get_all_raw(self) -> dict:
        """
        获取所有 Issue 链接类型（原始 JSON）

        Returns:
            dict: 原始 JSON 响应
        """
        return await self.client.get_json(self.BASE_PATH)

    async def create(
        self,
        name: str,
        inward: str,
        outward: str,
    ) -> IssueLinkType:
        """
        创建 Issue 链接类型

        POST /rest/api/2/issueLinkType

        Args:
            name: 链接类型名称
            inward: 内向描述（如 "is blocked by"）
            outward: 外向描述（如 "blocks"）

        Returns:
            IssueLinkType: 创建的链接类型
        """
        payload = {
            "name": name,
            "inward": inward,
            "outward": outward,
        }
        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return IssueLinkType.model_validate(data)

    async def get(self, link_type_id: str) -> IssueLinkType:
        """
        获取指定 Issue 链接类型

        GET /rest/api/2/issueLinkType/{issueLinkTypeId}

        Args:
            link_type_id: 链接类型 ID

        Returns:
            IssueLinkType: 链接类型信息
        """
        path = f"{self.BASE_PATH}/{link_type_id}"
        data = await self.client.get_json(path)
        return IssueLinkType.model_validate(data)

    async def get_raw(self, link_type_id: str) -> dict:
        """
        获取指定 Issue 链接类型（原始 JSON）

        Args:
            link_type_id: 链接类型 ID

        Returns:
            dict: 原始 JSON 响应
        """
        path = f"{self.BASE_PATH}/{link_type_id}"
        return await self.client.get_json(path)

    async def update(
        self,
        link_type_id: str,
        name: Optional[str] = None,
        inward: Optional[str] = None,
        outward: Optional[str] = None,
    ) -> IssueLinkType:
        """
        更新 Issue 链接类型

        PUT /rest/api/2/issueLinkType/{issueLinkTypeId}

        Args:
            link_type_id: 链接类型 ID
            name: 新名称（可选）
            inward: 新内向描述（可选）
            outward: 新外向描述（可选）

        Returns:
            IssueLinkType: 更新后的链接类型
        """
        path = f"{self.BASE_PATH}/{link_type_id}"
        payload = {}
        if name is not None:
            payload["name"] = name
        if inward is not None:
            payload["inward"] = inward
        if outward is not None:
            payload["outward"] = outward

        data = await self.client.put_json(path, data=payload)
        return IssueLinkType.model_validate(data)

    async def delete(self, link_type_id: str) -> None:
        """
        删除 Issue 链接类型

        DELETE /rest/api/2/issueLinkType/{issueLinkTypeId}

        Args:
            link_type_id: 链接类型 ID
        """
        path = f"{self.BASE_PATH}/{link_type_id}"
        response = await self.client.delete(path)
        response.raise_for_status()
