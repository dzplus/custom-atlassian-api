"""
Search Resource - Search API

GET    /rest/api/search                               - 全局搜索 (CQL)
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.confluence.models.content import SearchResultList


class SearchResource(BaseResource):
    """
    Search 资源

    API: /rest/api/search
    """

    BASE_PATH = "/rest/api/search"

    async def search(
        self,
        cql: str,
        cql_context: Optional[str] = None,
        excerpt: Optional[str] = None,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
        include_archived_spaces: bool = False,
    ) -> SearchResultList:
        """
        全局搜索

        GET /rest/api/search

        使用 CQL (Confluence Query Language) 搜索内容、空间、用户等

        Args:
            cql: CQL 查询语句
            cql_context: CQL 上下文（JSON 格式）
            excerpt: 摘要模式 (highlight, indexed, none)
            expand: 展开的字段
            start: 起始位置
            limit: 返回数量
            include_archived_spaces: 是否包含已归档空间

        Returns:
            SearchResultList: 搜索结果

        CQL 示例:
            - "type=page"
            - "space=DEV and type=page"
            - "title~test"
            - "creator=admin"
            - "lastModified>=2023-01-01"
        """
        params: dict[str, Any] = {
            "cql": cql,
            "start": start,
            "limit": limit,
        }
        if cql_context:
            params["cqlcontext"] = cql_context
        if excerpt:
            params["excerpt"] = excerpt
        if expand:
            params["expand"] = expand
        if include_archived_spaces:
            params["includeArchivedSpaces"] = "true"

        data = await self.client.get_json(self.BASE_PATH, params=params)
        return SearchResultList.model_validate(data)

    async def search_raw(
        self,
        cql: str,
        cql_context: Optional[str] = None,
        excerpt: Optional[str] = None,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
        include_archived_spaces: bool = False,
    ) -> dict:
        """
        全局搜索（原始 JSON）

        Args:
            cql: CQL 查询语句
            cql_context: CQL 上下文（JSON 格式）
            excerpt: 摘要模式
            expand: 展开的字段
            start: 起始位置
            limit: 返回数量
            include_archived_spaces: 是否包含已归档空间

        Returns:
            dict: 原始 JSON 响应
        """
        params: dict[str, Any] = {
            "cql": cql,
            "start": start,
            "limit": limit,
        }
        if cql_context:
            params["cqlcontext"] = cql_context
        if excerpt:
            params["excerpt"] = excerpt
        if expand:
            params["expand"] = expand
        if include_archived_spaces:
            params["includeArchivedSpaces"] = "true"

        return await self.client.get_json(self.BASE_PATH, params=params)
