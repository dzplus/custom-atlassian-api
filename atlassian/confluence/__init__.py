"""
Confluence API Client - Confluence Server/Data Center REST API

用法:
    from atlassian.confluence import ConfluenceClient

    async with ConfluenceClient() as confluence:
        # 获取空间列表
        spaces = await confluence.space.get_all()

        # 获取页面
        page = await confluence.content.get(page_id)
"""

from atlassian.confluence.client import ConfluenceClient

__all__ = ["ConfluenceClient"]
