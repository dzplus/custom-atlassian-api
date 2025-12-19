"""
Audit Resource - 审计 API

GET    /rest/audit                  - 获取审计记录列表
POST   /rest/audit                  - 存储审计记录
GET    /rest/audit/export           - 导出审计数据
GET    /rest/audit/retention        - 获取保留期设置
PUT    /rest/audit/retention        - 设置保留期
GET    /rest/audit/since            - 获取指定时间范围内的审计记录
"""

from typing import Any, Optional
from atlassian.common.base import BaseResource


class AuditResource(BaseResource):
    """
    审计资源

    API: /rest/audit

    注意: 需要管理员权限
    """

    BASE_PATH = "/rest/audit"

    async def get_all(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        search_string: Optional[str] = None,
        start: int = 0,
        limit: int = 1000,
    ) -> dict:
        """
        获取审计记录列表

        GET /rest/audit

        Args:
            start_date: 开始日期（ISO 8601 格式）
            end_date: 结束日期（ISO 8601 格式）
            search_string: 搜索字符串
            start: 起始位置
            limit: 返回数量

        Returns:
            dict: 审计记录列表
        """
        params: dict[str, Any] = {
            "start": start,
            "limit": limit,
        }
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if search_string:
            params["searchString"] = search_string

        return await self.client.get_json(self.BASE_PATH, params=params)

    async def create(self, audit_record: dict) -> dict:
        """
        存储审计记录

        POST /rest/audit

        Args:
            audit_record: 审计记录数据
                {
                    "author": {"type": "user", "displayName": "..."},
                    "remoteAddress": "192.168.1.1",
                    "creationDate": 1234567890000,
                    "summary": "...",
                    "description": "...",
                    "category": "...",
                    "sysAdmin": false,
                    "affectedObject": {...},
                    "changedValues": [...],
                    "associatedObjects": [...]
                }

        Returns:
            dict: 创建的审计记录
        """
        return await self.client.post_json(self.BASE_PATH, data=audit_record)

    async def export(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        search_string: Optional[str] = None,
        format: str = "csv",
    ) -> bytes:
        """
        导出审计数据

        GET /rest/audit/export

        Args:
            start_date: 开始日期（ISO 8601 格式）
            end_date: 结束日期（ISO 8601 格式）
            search_string: 搜索字符串
            format: 导出格式（csv 或 json）

        Returns:
            bytes: 导出的数据
        """
        path = f"{self.BASE_PATH}/export"
        params: dict[str, Any] = {"format": format}

        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if search_string:
            params["searchString"] = search_string

        response = await self.client.get(path, params=params)
        response.raise_for_status()
        return response.content

    async def get_retention(self) -> dict:
        """
        获取审计记录保留期设置

        GET /rest/audit/retention

        Returns:
            dict: 保留期设置
            {
                "number": 90,
                "units": "DAYS"
            }
        """
        path = f"{self.BASE_PATH}/retention"
        return await self.client.get_json(path)

    async def set_retention(
        self,
        number: int,
        units: str = "DAYS",
    ) -> dict:
        """
        设置审计记录保留期

        PUT /rest/audit/retention

        Args:
            number: 保留期数量
            units: 时间单位（DAYS, MONTHS, YEARS）

        Returns:
            dict: 更新后的保留期设置
        """
        path = f"{self.BASE_PATH}/retention"
        data = {
            "number": number,
            "units": units,
        }
        return await self.client.put_json(path, data=data)

    async def get_since(
        self,
        number: int,
        units: str = "DAYS",
        search_string: Optional[str] = None,
        start: int = 0,
        limit: int = 1000,
    ) -> dict:
        """
        获取指定时间范围内的审计记录

        GET /rest/audit/since

        Args:
            number: 时间数量
            units: 时间单位（NANOS, MICROS, MILLIS, SECONDS, MINUTES, HOURS, DAYS, WEEKS, MONTHS, YEARS）
            search_string: 搜索字符串
            start: 起始位置
            limit: 返回数量

        Returns:
            dict: 审计记录列表
        """
        path = f"{self.BASE_PATH}/since"
        params: dict[str, Any] = {
            "number": number,
            "units": units,
            "start": start,
            "limit": limit,
        }
        if search_string:
            params["searchString"] = search_string

        return await self.client.get_json(path, params=params)
