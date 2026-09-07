"""
Like Resource - Likes API (点赞)

GET    /rest/likes/1.0/content/{contentId}/likes   - 获取点赞列表
POST   /rest/likes/1.0/content/{contentId}/likes   - 点赞
DELETE /rest/likes/1.0/content/{contentId}/likes   - 取消点赞

注意:
    该 API 位于 /rest/likes/1.0 命名空间, 不在 /rest/api 下。
    page 与 comment (含划线批注及其回复) 共用同一套端点,
    contentId 传哪种内容的 ID 即操作哪种内容。
"""

from typing import Any, Optional

import httpx

from atlassian.common.base import BaseResource


class LikeResource(BaseResource):
    """
    Like 资源

    API: /rest/likes/1.0/content
    """

    BASE_PATH = "/rest/likes/1.0/content"

    def _likes_path(self, content_id: str) -> str:
        return f"{self.BASE_PATH}/{content_id}/likes"

    async def get_likes(self, content_id: str) -> dict:
        """
        获取点赞列表

        GET /rest/likes/1.0/content/{contentId}/likes

        Args:
            content_id: 内容 ID (页面 / 评论 / 划线批注)

        Returns:
            dict: 形如
                {
                    "likes": [{"user": {"name": ..., "fullName": ..., ...}}],
                    "content_type": "page",
                    "content_id": "223740097",
                }
                content_type 可区分 page / comment
        """
        return await self.client.get_json(self._likes_path(content_id))

    async def add_like(
        self,
        content_id: str,
        username: Optional[str] = None,
    ) -> dict:
        """
        点赞

        POST /rest/likes/1.0/content/{contentId}/likes

        直接返回更新后的点赞列表，无需再读一次。

        重复点赞时服务端返回 400 "The content cannot be liked"，报错文本看不出原因。
        本方法对此做幂等处理: 若目标用户已在点赞列表中则返回当前列表，否则抛出原错误。

        Args:
            content_id: 内容 ID (页面 / 评论 / 划线批注)
            username: 点赞用户名，默认为当前认证用户

        Returns:
            dict: 点赞列表（结构同 get_likes）
        """
        user = username or await self._current_username()
        try:
            return await self.client.post_json(
                self._likes_path(content_id),
                data={"username": user},
            )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code != 400:
                raise
            likes = await self.get_likes(content_id)
            if self._contains_user(likes, user):
                return likes
            raise

    async def remove_like(self, content_id: str) -> None:
        """
        取消点赞

        DELETE /rest/likes/1.0/content/{contentId}/likes

        取消的始终是当前认证用户的赞（服务端忽略 username 参数）。
        代删他人的赞未经验证，不提供该能力。

        Args:
            content_id: 内容 ID (页面 / 评论 / 划线批注)
        """
        await self.client.delete_json(self._likes_path(content_id))

    # ========== 内部方法 ==========

    @staticmethod
    def _contains_user(likes: Any, username: str) -> bool:
        if not isinstance(likes, dict):
            return False
        for item in likes.get("likes") or []:
            if not isinstance(item, dict):
                continue
            user = item.get("user") or {}
            if isinstance(user, dict) and user.get("name") == username:
                return True
        return False

    async def _current_username(self) -> str:
        username = getattr(self.client, "_username", None)
        if username:
            return username

        data = await self.client.get_json("/rest/api/user/current")
        username = data.get("username") if isinstance(data, dict) else None
        if not username:
            raise ValueError(
                "无法确定当前用户名，请显式传入 username 参数"
            )
        return username
