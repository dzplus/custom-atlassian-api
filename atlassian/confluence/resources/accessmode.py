"""
AccessMode Resource - 访问模式 API

GET    /rest/api/accessmode  - 获取 Confluence 访问模式状态

注意: AccessMode API 在 Confluence 7.0+ 版本中可用
"""

from atlassian.common.base import BaseResource


class AccessModeResource(BaseResource):
    """
    访问模式资源

    API: /rest/api/accessmode

    用于检查 Confluence 当前的访问模式状态（只读、读写、维护等）

    注意: 需要 Confluence 7.0+ 版本
    """

    BASE_PATH = "/rest/api/accessmode"

    async def get(self) -> dict:
        """
        获取 Confluence 访问模式状态

        GET /rest/api/accessmode

        Returns:
            dict: 访问模式信息
            {
                "mode": "READ_WRITE",  # 可能的值: READ_WRITE, READ_ONLY, MAINTENANCE
                "message": "Confluence is running normally",
                "readOnly": false
            }

        访问模式说明:
            - READ_WRITE: 正常读写模式
            - READ_ONLY: 只读模式（通常在维护期间）
            - MAINTENANCE: 维护模式（不可访问）
        """
        return await self.client.get_json(self.BASE_PATH)
