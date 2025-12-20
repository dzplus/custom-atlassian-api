"""
Priority Scheme Resource - 优先级方案资源

GET    /rest/api/2/priorityscheme                  - 获取所有优先级方案
POST   /rest/api/2/priorityscheme                  - 创建优先级方案
GET    /rest/api/2/priorityscheme/{schemeId}       - 获取优先级方案
PUT    /rest/api/2/priorityscheme/{schemeId}       - 更新优先级方案
DELETE /rest/api/2/priorityscheme/{schemeId}       - 删除优先级方案
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.issue_type import PriorityScheme


class PrioritySchemeResource(BaseResource):
    """
    优先级方案资源

    API: /rest/api/2/priorityscheme
    """

    BASE_PATH = "/rest/api/2/priorityscheme"

    async def get_all(
        self,
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict:
        """
        获取所有优先级方案

        GET /rest/api/2/priorityscheme

        Args:
            start_at: 起始位置（默认0）
            max_results: 最大结果数（默认50）

        Returns:
            dict: 包含分页信息和方案列表
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
        default_option_id: Optional[str] = None,
        option_ids: Optional[list[str]] = None,
    ) -> PriorityScheme:
        """
        创建优先级方案

        POST /rest/api/2/priorityscheme

        Args:
            name: 方案名称
            description: 方案描述（可选）
            default_option_id: 默认优先级ID（可选）
            option_ids: 优先级ID列表（可选）

        Returns:
            PriorityScheme: 创建的方案
        """
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        if default_option_id:
            payload["defaultOptionId"] = default_option_id
        if option_ids:
            payload["optionIds"] = option_ids

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return PriorityScheme.model_validate(data)

    async def create_raw(
        self,
        name: str,
        description: Optional[str] = None,
        default_option_id: Optional[str] = None,
        option_ids: Optional[list[str]] = None,
    ) -> dict:
        """创建优先级方案（原始JSON）"""
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        if default_option_id:
            payload["defaultOptionId"] = default_option_id
        if option_ids:
            payload["optionIds"] = option_ids

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def get(
        self,
        scheme_id: str,
    ) -> PriorityScheme:
        """
        获取优先级方案详情

        GET /rest/api/2/priorityscheme/{schemeId}

        Args:
            scheme_id: 方案ID

        Returns:
            PriorityScheme: 方案详情
        """
        path = f"{self.BASE_PATH}/{scheme_id}"
        data = await self.client.get_json(path)
        return PriorityScheme.model_validate(data)

    async def get_raw(
        self,
        scheme_id: str,
    ) -> dict:
        """获取优先级方案详情（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}"
        return await self.client.get_json(path)

    async def update(
        self,
        scheme_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        default_option_id: Optional[str] = None,
        option_ids: Optional[list[str]] = None,
    ) -> dict:
        """
        更新优先级方案

        PUT /rest/api/2/priorityscheme/{schemeId}

        Args:
            scheme_id: 方案ID
            name: 方案名称（可选）
            description: 方案描述（可选）
            default_option_id: 默认优先级ID（可选）
            option_ids: 优先级ID列表（可选）

        Returns:
            dict: 操作结果
        """
        path = f"{self.BASE_PATH}/{scheme_id}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if default_option_id:
            payload["defaultOptionId"] = default_option_id
        if option_ids:
            payload["optionIds"] = option_ids

        return await self.client.put_json(path, data=payload)

    async def delete(
        self,
        scheme_id: str,
    ) -> dict:
        """
        删除优先级方案

        DELETE /rest/api/2/priorityscheme/{schemeId}

        Args:
            scheme_id: 方案ID

        Returns:
            dict: 操作结果
        """
        path = f"{self.BASE_PATH}/{scheme_id}"
        return await self.client.delete(path)
