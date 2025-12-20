"""
Field Resource - 字段资源

GET /rest/api/2/field         - 获取所有字段
GET /rest/api/2/field/{id}    - 获取字段详情
"""

from typing import Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.field import FieldMetadata


class FieldResource(BaseResource):
    """
    字段资源

    API: /rest/api/2/field
    """

    BASE_PATH = "/rest/api/2/field"

    async def get_all(self) -> list[FieldMetadata]:
        """
        获取所有字段

        GET /rest/api/2/field

        Returns:
            list[FieldMetadata]: 字段列表
        """
        data = await self.client.get_json(self.BASE_PATH)
        return [FieldMetadata.model_validate(f) for f in data]

    async def get_all_raw(self) -> list[dict]:
        """获取所有字段（原始JSON）"""
        return await self.client.get_json(self.BASE_PATH)

    async def get(
        self,
        field_id: str,
    ) -> FieldMetadata:
        """
        获取字段详情

        GET /rest/api/2/field/{id}

        Args:
            field_id: 字段ID

        Returns:
            FieldMetadata: 字段详情
        """
        path = f"{self.BASE_PATH}/{field_id}"
        data = await self.client.get_json(path)
        return FieldMetadata.model_validate(data)

    async def get_raw(
        self,
        field_id: str,
    ) -> dict:
        """获取字段详情（原始JSON）"""
        path = f"{self.BASE_PATH}/{field_id}"
        return await self.client.get_json(path)
