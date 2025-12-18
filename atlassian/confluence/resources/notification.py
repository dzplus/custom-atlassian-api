"""
Notification Resource - Notification API (MyWork Plugin)

需要安装 MyWork Confluence Host Plugin 插件

GET    /rest/mywork/latest/notification                              - 获取通知列表
GET    /rest/mywork/latest/notification/nested                       - 获取嵌套（分组）通知
GET    /rest/mywork/latest/notification/{id}                         - 获取特定通知
POST   /rest/mywork/latest/notification                              - 创建或更新通知
DELETE /rest/mywork/latest/notification/{id}                         - 删除通知
PUT    /rest/mywork/latest/notification/{id}/status                  - 改变通知状态
PUT    /rest/mywork/latest/notification/read                         - 标记通知为已读
PUT    /rest/mywork/latest/notification/lastreadid                   - 设置最后查看的通知ID
POST   /rest/mywork/latest/notification/metadata                     - 更新通知元数据

GET    /rest/mywork/latest/status/notification/count                 - 获取未读通知数量
GET    /rest/mywork/latest/status/notification/new                   - 仅获取新通知计数
GET    /rest/mywork/latest/status                                    - 获取状态信息（包含未读数量和超时设置）
"""

from typing import Any, Optional
from atlassian.common.base import BaseResource


class NotificationResource(BaseResource):
    """
    Notification 资源 (MyWork Plugin)

    API: /rest/mywork/latest/notification
    """

    BASE_PATH = "/rest/mywork/latest/notification"
    STATUS_PATH = "/rest/mywork/latest/status"

    # ========== 获取通知 ==========

    async def get_all(
        self,
        limit: Optional[int] = None,
        after: Optional[int] = None,
        before: Optional[int] = None,
    ) -> list[dict]:
        """
        获取通知列表（平面列表）

        GET /rest/notification

        Args:
            limit: 返回结果数量
            after: 仅返回指定通知ID之后创建的通知（用于分页）
            before: 仅返回指定通知ID之前创建的通知

        Returns:
            list[dict]: 通知列表

        通知对象包含字段:
            - id: 通知ID
            - title: 通知标题
            - description: 通知描述
            - application: 来源应用
            - entity: 实体类型
            - action: 动作类型
            - created: 创建时间
            - updated: 更新时间
            - status: 通知状态
            - read: 是否已读
            - pinned: 是否标记
            - item: 关联项目信息（标题、URL、图标等）
            - metadata: 元数据
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before

        return await self.client.get_json(self.BASE_PATH, params=params)

    async def get_nested(
        self,
        limit: Optional[int] = None,
        after: Optional[int] = None,
        before: Optional[int] = None,
    ) -> list[dict]:
        """
        获取嵌套（分组）通知

        GET /rest/notification/nested

        按 groupingId 聚合通知，同一项目的多个通知会被分组

        Args:
            limit: 返回结果数量
            after: 仅返回指定通知ID之后创建的通知
            before: 仅返回指定通知ID之前创建的通知

        Returns:
            list[dict]: 分组的通知列表

        返回格式:
            [
                {
                    "item": {
                        "iconUrl": "...",
                        "title": "页面标题",
                        "applicationLinkId": "..."
                    },
                    "notifications": [
                        {
                            "id": 0,
                            "title": "John 评论了",
                            "globalId": "1234",
                            "read": false
                        }
                    ]
                }
            ]
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before

        return await self.client.get_json(f"{self.BASE_PATH}/nested", params=params)

    async def get(self, notification_id: int) -> dict:
        """
        获取特定通知

        GET /rest/notification/{id}

        Args:
            notification_id: 通知ID

        Returns:
            dict: 通知详情
        """
        path = f"{self.BASE_PATH}/{notification_id}"
        return await self.client.get_json(path)

    # ========== 未读通知统计 ==========

    async def get_unread_count(self) -> dict:
        """
        获取未读通知数量

        GET /rest/status/notification/count

        Returns:
            dict: 包含未读数量和轮询超时配置
            {
                "count": 7,          # 未读通知数量
                "timeout": 60,       # 轮询间隔（秒）
                "maxTimeout": 300    # 最大超时
            }
        """
        return await self.client.get_json(f"{self.STATUS_PATH}/notification/count")

    async def get_new_count(self) -> dict:
        """
        仅获取新通知计数

        GET /rest/status/notification/new

        Returns:
            dict: 新通知数量
        """
        return await self.client.get_json(f"{self.STATUS_PATH}/notification/new")

    async def get_status(self) -> dict:
        """
        获取通知状态信息（包含未读数量和轮询配置）

        GET /rest/status

        Returns:
            dict: 状态信息，包含未读通知计数和超时设置
        """
        return await self.client.get_json(self.STATUS_PATH)

    # ========== 标记已读 ==========

    async def mark_as_read(self, notification_id: int) -> dict:
        """
        标记通知为已读

        PUT /rest/notification/read

        设置哪个通知已被查看，更新未读计数

        Args:
            notification_id: 通知ID

        Returns:
            dict: 空响应（操作成功）
        """
        return await self.client.put_json(
            f"{self.BASE_PATH}/read",
            data=notification_id
        )

    async def set_last_read_id(self, notification_id: int) -> dict:
        """
        设置最后查看的通知ID

        PUT /rest/notification/lastreadid

        Args:
            notification_id: 最后查看的通知ID

        Returns:
            dict: 响应
        """
        return await self.client.put_json(
            f"{self.BASE_PATH}/lastreadid",
            data=notification_id
        )

    # ========== 通知管理 ==========

    async def update_status(
        self,
        notification_id: int,
        status: str
    ) -> dict:
        """
        改变通知状态

        PUT /rest/notification/{id}/status

        如果改为 TODO，则会创建新任务

        Args:
            notification_id: 通知ID
            status: 新状态（如 "TODO", "DONE" 等）

        Returns:
            dict: 更新结果
        """
        path = f"{self.BASE_PATH}/{notification_id}/status"
        return await self.client.put_json(path, data={"status": status})

    async def delete(self, notification_id: int) -> None:
        """
        永久删除通知

        DELETE /rest/notification/{id}

        Args:
            notification_id: 通知ID
        """
        path = f"{self.BASE_PATH}/{notification_id}"
        response = await self.client.delete(path)
        response.raise_for_status()

    async def create_or_update(self, notification_data: dict) -> dict:
        """
        创建或更新通知

        POST /rest/notification

        Args:
            notification_data: 通知数据

        Returns:
            dict: 创建或更新的通知
        """
        return await self.client.post_json(self.BASE_PATH, data=notification_data)

    async def update_metadata(self, metadata: dict) -> dict:
        """
        更新通知元数据

        POST /rest/notification/metadata

        Args:
            metadata: 元数据

        Returns:
            dict: 更新结果
        """
        return await self.client.post_json(
            f"{self.BASE_PATH}/metadata",
            data=metadata
        )
