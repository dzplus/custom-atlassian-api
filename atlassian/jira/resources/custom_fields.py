"""
Custom Fields Resource - 自定义字段 API

GET /rest/api/2/customFields - 获取自定义字段列表
"""

from typing import Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.custom_field import CustomField, CustomFieldsResponse


class CustomFieldsResource(BaseResource):
    """
    自定义字段资源

    API: /rest/api/2/customFields
    """

    BASE_PATH = "/rest/api/2/customFields"

    async def get_all(
        self,
        start_at: int = 0,
        max_results: int = 50,
        search: Optional[str] = None,
        project_ids: Optional[list[int]] = None,
        screen_ids: Optional[list[int]] = None,
        types: Optional[list[str]] = None,
    ) -> CustomFieldsResponse:
        """
        获取自定义字段列表（分页）

        GET /rest/api/2/customFields

        Args:
            start_at: 起始位置（默认 0，API 默认 1）
            max_results: 最大结果数（默认 50）
            search: 搜索关键字（可选）
            project_ids: 项目 ID 列表（可选）
            screen_ids: 屏幕 ID 列表（可选）
            types: 字段类型列表（可选）

        Returns:
            CustomFieldsResponse: 自定义字段列表（分页）
        """
        params: dict = {
            "startAt": start_at,
            "maxResults": max_results,
        }

        if search:
            params["search"] = search
        if project_ids:
            params["projectIds"] = ",".join(str(p) for p in project_ids)
        if screen_ids:
            params["screenIds"] = ",".join(str(s) for s in screen_ids)
        if types:
            params["types"] = ",".join(types)

        data = await self.client.get_json(self.BASE_PATH, params=params)
        return CustomFieldsResponse.model_validate(data)

    async def get_all_raw(
        self,
        start_at: int = 0,
        max_results: int = 50,
        search: Optional[str] = None,
        project_ids: Optional[list[int]] = None,
        screen_ids: Optional[list[int]] = None,
        types: Optional[list[str]] = None,
    ) -> dict:
        """
        获取自定义字段列表（原始 JSON）

        Args:
            start_at: 起始位置
            max_results: 最大结果数
            search: 搜索关键字（可选）
            project_ids: 项目 ID 列表（可选）
            screen_ids: 屏幕 ID 列表（可选）
            types: 字段类型列表（可选）

        Returns:
            dict: 原始 JSON 响应
        """
        params: dict = {
            "startAt": start_at,
            "maxResults": max_results,
        }

        if search:
            params["search"] = search
        if project_ids:
            params["projectIds"] = ",".join(str(p) for p in project_ids)
        if screen_ids:
            params["screenIds"] = ",".join(str(s) for s in screen_ids)
        if types:
            params["types"] = ",".join(types)

        return await self.client.get_json(self.BASE_PATH, params=params)

    async def iter_all(
        self,
        search: Optional[str] = None,
        project_ids: Optional[list[int]] = None,
        screen_ids: Optional[list[int]] = None,
        types: Optional[list[str]] = None,
        page_size: int = 50,
    ):
        """
        迭代获取所有自定义字段

        Args:
            search: 搜索关键字（可选）
            project_ids: 项目 ID 列表（可选）
            screen_ids: 屏幕 ID 列表（可选）
            types: 字段类型列表（可选）
            page_size: 每页大小（默认 50）

        Yields:
            CustomField: 自定义字段
        """
        start_at = 0
        while True:
            response = await self.get_all(
                start_at=start_at,
                max_results=page_size,
                search=search,
                project_ids=project_ids,
                screen_ids=screen_ids,
                types=types,
            )

            for field in response.values:
                yield field

            # 检查是否还有更多
            if start_at + len(response.values) >= response.total:
                break

            start_at += page_size
