"""
LongTask Resource - 长期任务 API

GET    /rest/api/longtask           - 获取所有长期任务信息
GET    /rest/api/longtask/{id}      - 获取指定长期任务信息
"""

from atlassian.common.base import BaseResource


class LongTaskResource(BaseResource):
    """
    长期任务资源

    API: /rest/api/longtask

    用于跟踪长时间运行的操作（如空间导出、内容删除等）
    """

    BASE_PATH = "/rest/api/longtask"

    async def get_all(
        self,
        start: int = 0,
        limit: int = 100,
    ) -> dict:
        """
        获取所有长期任务信息

        GET /rest/api/longtask

        Args:
            start: 起始位置
            limit: 返回数量

        Returns:
            dict: 长期任务列表
            {
                "results": [
                    {
                        "id": "123",
                        "name": {...},
                        "elapsedTime": 1000,
                        "percentageComplete": 50,
                        "successful": false,
                        "finished": false,
                        "messages": [],
                        "_links": {...}
                    }
                ],
                "start": 0,
                "limit": 100,
                "size": 1,
                "_links": {...}
            }
        """
        params = {
            "start": start,
            "limit": limit,
        }
        return await self.client.get_json(self.BASE_PATH, params=params)

    async def get(self, task_id: str) -> dict:
        """
        获取指定长期任务信息

        GET /rest/api/longtask/{id}

        Args:
            task_id: 任务ID

        Returns:
            dict: 任务详情
            {
                "id": "123",
                "name": {
                    "key": "...",
                    "args": [...]
                },
                "elapsedTime": 1000,
                "percentageComplete": 50,
                "successful": false,
                "finished": false,
                "messages": [
                    {
                        "translation": "...",
                        "args": []
                    }
                ],
                "_links": {...}
            }
        """
        path = f"{self.BASE_PATH}/{task_id}"
        return await self.client.get_json(path)
