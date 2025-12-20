"""
Webhook Resource - Webhook API

POST   /rest/api/webhooks                              - 创建 webhook
GET    /rest/api/webhooks                              - 获取所有 webhooks
GET    /rest/api/webhooks/{webhookId}                  - 获取指定 webhook
PUT    /rest/api/webhooks/{webhookId}                  - 更新 webhook
DELETE /rest/api/webhooks/{webhookId}                  - 删除 webhook
GET    /rest/api/webhooks/{webhookId}/latest           - 获取最近调用记录
GET    /rest/api/webhooks/{webhookId}/statistics       - 获取统计信息
GET    /rest/api/webhooks/{webhookId}/statistics/summary - 获取统计摘要
POST   /rest/api/webhooks/test                         - 测试端点连接性

注意: Webhooks API 在 Confluence 7.0+ 版本中可用
"""

from typing import Optional, Any
from atlassian.common.base import BaseResource


class WebhookResource(BaseResource):
    """
    Webhook 资源

    API: /rest/api/webhooks

    用于创建和管理 webhooks，在 Confluence 事件发生时向外部系统发送通知

    注意: 需要 Confluence 7.0+ 版本
    """

    BASE_PATH = "/rest/api/webhooks"

    async def create(self, webhook_data: dict) -> dict:
        """
        创建 webhook

        POST /rest/api/webhooks

        Args:
            webhook_data: webhook 配置
                {
                    "name": "My Webhook",
                    "url": "https://example.com/webhook",
                    "events": ["page_created", "page_updated"],
                    "excludeBody": false,
                    "filters": {...}
                }

        Returns:
            dict: 创建的 webhook 信息
            {
                "id": "123",
                "name": "My Webhook",
                "url": "https://example.com/webhook",
                "events": [...],
                "enabled": true,
                "_links": {...}
            }
        """
        return await self.client.post_json(self.BASE_PATH, data=webhook_data)

    async def get_all(
        self,
        event: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
    ) -> dict:
        """
        获取所有 webhooks

        GET /rest/api/webhooks

        Args:
            event: 按事件类型过滤（如 "page_created"）
            start: 起始位置
            limit: 返回数量

        Returns:
            dict: webhook 列表
            {
                "results": [
                    {
                        "id": "123",
                        "name": "My Webhook",
                        "url": "...",
                        "events": [...],
                        "enabled": true
                    }
                ],
                "start": 0,
                "limit": 25,
                "size": 1,
                "_links": {...}
            }
        """
        params: dict[str, Any] = {
            "start": start,
            "limit": limit,
        }
        if event:
            params["event"] = event

        return await self.client.get_json(self.BASE_PATH, params=params)

    async def get(self, webhook_id: str) -> dict:
        """
        获取指定 webhook

        GET /rest/api/webhooks/{webhookId}

        Args:
            webhook_id: webhook ID

        Returns:
            dict: webhook 详情
            {
                "id": "123",
                "name": "My Webhook",
                "url": "https://example.com/webhook",
                "events": ["page_created", "page_updated"],
                "enabled": true,
                "excludeBody": false,
                "filters": {...},
                "_links": {...}
            }
        """
        path = f"{self.BASE_PATH}/{webhook_id}"
        return await self.client.get_json(path)

    async def update(self, webhook_id: str, webhook_data: dict) -> dict:
        """
        更新 webhook

        PUT /rest/api/webhooks/{webhookId}

        Args:
            webhook_id: webhook ID
            webhook_data: 更新的 webhook 配置
                {
                    "name": "Updated Webhook",
                    "url": "https://example.com/new-webhook",
                    "events": ["page_created"],
                    "enabled": true
                }

        Returns:
            dict: 更新后的 webhook 信息
        """
        path = f"{self.BASE_PATH}/{webhook_id}"
        return await self.client.put_json(path, data=webhook_data)

    async def delete(self, webhook_id: str) -> None:
        """
        删除 webhook

        DELETE /rest/api/webhooks/{webhookId}

        Args:
            webhook_id: webhook ID
        """
        path = f"{self.BASE_PATH}/{webhook_id}"
        response = await self.client.delete(path)
        response.raise_for_status()

    async def get_latest_invocations(
        self,
        webhook_id: str,
        start: int = 0,
        limit: int = 25,
    ) -> dict:
        """
        获取最近的 webhook 调用记录

        GET /rest/api/webhooks/{webhookId}/latest

        Args:
            webhook_id: webhook ID
            start: 起始位置
            limit: 返回数量

        Returns:
            dict: 调用记录列表
            {
                "results": [
                    {
                        "event": "page_created",
                        "timestamp": "2023-01-01T00:00:00.000Z",
                        "statusCode": 200,
                        "duration": 123,
                        "outcome": "SUCCESS"
                    }
                ],
                "start": 0,
                "limit": 25,
                "size": 1
            }
        """
        path = f"{self.BASE_PATH}/{webhook_id}/latest"
        params = {
            "start": start,
            "limit": limit,
        }
        return await self.client.get_json(path, params=params)

    async def get_statistics(
        self,
        webhook_id: str,
        start: int = 0,
        limit: int = 25,
    ) -> dict:
        """
        获取 webhook 统计信息

        GET /rest/api/webhooks/{webhookId}/statistics

        Args:
            webhook_id: webhook ID
            start: 起始位置
            limit: 返回数量

        Returns:
            dict: 统计信息
            {
                "results": [
                    {
                        "event": "page_created",
                        "totalInvocations": 100,
                        "successfulInvocations": 95,
                        "failedInvocations": 5,
                        "averageDuration": 150
                    }
                ],
                "start": 0,
                "limit": 25,
                "size": 1
            }
        """
        path = f"{self.BASE_PATH}/{webhook_id}/statistics"
        params = {
            "start": start,
            "limit": limit,
        }
        return await self.client.get_json(path, params=params)

    async def get_statistics_summary(self, webhook_id: str) -> dict:
        """
        获取 webhook 统计摘要

        GET /rest/api/webhooks/{webhookId}/statistics/summary

        Args:
            webhook_id: webhook ID

        Returns:
            dict: 统计摘要
            {
                "totalInvocations": 100,
                "successfulInvocations": 95,
                "failedInvocations": 5,
                "averageDuration": 150,
                "lastInvocation": "2023-01-01T00:00:00.000Z"
            }
        """
        path = f"{self.BASE_PATH}/{webhook_id}/statistics/summary"
        return await self.client.get_json(path)

    async def test(self, url: str) -> dict:
        """
        测试端点连接性

        POST /rest/api/webhooks/test

        Args:
            url: 要测试的 webhook URL

        Returns:
            dict: 测试结果
            {
                "statusCode": 200,
                "duration": 123,
                "message": "Connection successful"
            }
        """
        path = f"{self.BASE_PATH}/test"
        data = {"url": url}
        return await self.client.post_json(path, data=data)
