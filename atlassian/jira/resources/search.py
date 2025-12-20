"""
Search Resource - 搜索资源

GET  /rest/api/2/search - JQL搜索（GET）
POST /rest/api/2/search - JQL搜索（POST）
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.search import SearchResults


class SearchResource(BaseResource):
    """
    搜索资源

    API: /rest/api/2/search
    """

    BASE_PATH = "/rest/api/2/search"

    async def search(
        self,
        jql: str,
        start_at: int = 0,
        max_results: int = 50,
        fields: Optional[list[str]] = None,
        expand: Optional[list[str]] = None,
        validate_query: bool = True,
    ) -> SearchResults:
        """
        使用JQL搜索Issues（GET方法）

        GET /rest/api/2/search

        Args:
            jql: JQL查询语句
            start_at: 起始位置（默认0）
            max_results: 最大结果数（默认50）
            fields: 要返回的字段列表（可选）
            expand: 要扩展的字段列表（可选）
            validate_query: 是否验证查询（默认True）

        Returns:
            SearchResults: 搜索结果
        """
        params: dict[str, Any] = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results,
            "validateQuery": str(validate_query).lower(),
        }
        if fields:
            params["fields"] = ",".join(fields)
        if expand:
            params["expand"] = ",".join(expand)

        data = await self.client.get_json(self.BASE_PATH, params=params)
        return SearchResults.model_validate(data)

    async def search_raw(
        self,
        jql: str,
        start_at: int = 0,
        max_results: int = 50,
        fields: Optional[list[str]] = None,
        expand: Optional[list[str]] = None,
        validate_query: bool = True,
    ) -> dict:
        """使用JQL搜索Issues（GET方法，原始JSON）"""
        params: dict[str, Any] = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results,
            "validateQuery": str(validate_query).lower(),
        }
        if fields:
            params["fields"] = ",".join(fields)
        if expand:
            params["expand"] = ",".join(expand)

        return await self.client.get_json(self.BASE_PATH, params=params)

    async def search_post(
        self,
        jql: str,
        start_at: int = 0,
        max_results: int = 50,
        fields: Optional[list[str]] = None,
        expand: Optional[list[str]] = None,
        validate_query: bool = True,
    ) -> SearchResults:
        """
        使用JQL搜索Issues（POST方法）

        POST /rest/api/2/search

        Args:
            jql: JQL查询语句
            start_at: 起始位置（默认0）
            max_results: 最大结果数（默认50）
            fields: 要返回的字段列表（可选）
            expand: 要扩展的字段列表（可选）
            validate_query: 是否验证查询（默认True）

        Returns:
            SearchResults: 搜索结果
        """
        payload: dict[str, Any] = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results,
            "validateQuery": validate_query,
        }
        if fields:
            payload["fields"] = fields
        if expand:
            payload["expand"] = expand

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return SearchResults.model_validate(data)

    async def search_post_raw(
        self,
        jql: str,
        start_at: int = 0,
        max_results: int = 50,
        fields: Optional[list[str]] = None,
        expand: Optional[list[str]] = None,
        validate_query: bool = True,
    ) -> dict:
        """使用JQL搜索Issues（POST方法，原始JSON）"""
        payload: dict[str, Any] = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results,
            "validateQuery": validate_query,
        }
        if fields:
            payload["fields"] = fields
        if expand:
            payload["expand"] = expand

        return await self.client.post_json(self.BASE_PATH, data=payload)
