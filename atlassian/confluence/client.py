"""
Confluence Client - Confluence HTTP 客户端

提供统一的 Confluence API 访问入口，整合所有资源类
"""

from typing import Optional

from atlassian.common.client import BaseHttpClient, AuthMode
from atlassian.confluence.resources import (
    ContentResource,
    SpaceResource,
    UserResource,
    SearchResource,
    NotificationResource,
    GroupResource,
    AuditResource,
    LongTaskResource,
)


class ConfluenceClient(BaseHttpClient):
    """
    Confluence API 客户端

    整合所有 Confluence API 资源，提供统一访问入口

    注意: Confluence Server 某些版本可能不支持 Session 认证，
    建议使用 auth_mode="basic"

    用法:
        async with ConfluenceClient() as confluence:
            # 获取当前用户
            user = await confluence.user.get_current()

            # 获取空间列表
            spaces = await confluence.space.get_all()

            # 获取内容
            content = await confluence.content.get("12345")

            # 创建页面
            page = await confluence.content.create(
                type="page",
                title="Test Page",
                space_key="DEV",
                body="<p>Hello World</p>",
            )

            # 搜索
            results = await confluence.search.search("type=page and space=DEV")

    环境变量:
        CONFLUENCE_URL: Confluence 服务地址
        CONFLUENCE_USERNAME: 用户名
        CONFLUENCE_PASSWORD: 密码

        或使用通用变量:
        ATLASSIAN_URL, ATLASSIAN_USERNAME, ATLASSIAN_PASSWORD
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: float = 30.0,
        auto_login: bool = True,
        auto_relogin: bool = True,
        auth_mode: AuthMode = "basic",  # Confluence 默认使用 Basic Auth
    ):
        """
        初始化 Confluence 客户端

        Args:
            base_url: Confluence 服务地址，默认从 CONFLUENCE_URL 环境变量读取
            username: 用户名，默认从 CONFLUENCE_USERNAME 环境变量读取
            password: 密码，默认从 CONFLUENCE_PASSWORD 环境变量读取
            timeout: 请求超时时间（秒）
            auto_login: 是否在首次请求时自动登录 (仅 session 模式)
            auto_relogin: 会话过期时是否自动重新登录 (仅 session 模式)
            auth_mode: 认证模式，"basic" (默认) 或 "session"
        """
        super().__init__(
            base_url=base_url,
            username=username,
            password=password,
            timeout=timeout,
            auto_login=auto_login,
            auto_relogin=auto_relogin,
            env_prefix="CONFLUENCE",
            auth_mode=auth_mode,
        )

        # 初始化资源
        self._content: Optional[ContentResource] = None
        self._space: Optional[SpaceResource] = None
        self._user: Optional[UserResource] = None
        self._search: Optional[SearchResource] = None
        self._notification: Optional[NotificationResource] = None
        self._group: Optional[GroupResource] = None
        self._audit: Optional[AuditResource] = None
        self._longtask: Optional[LongTaskResource] = None

    @property
    def content(self) -> ContentResource:
        """内容资源 (rest/api/content)"""
        if self._content is None:
            self._content = ContentResource(self)
        return self._content

    @property
    def space(self) -> SpaceResource:
        """空间资源 (rest/api/space)"""
        if self._space is None:
            self._space = SpaceResource(self)
        return self._space

    @property
    def user(self) -> UserResource:
        """用户资源 (rest/api/user)"""
        if self._user is None:
            self._user = UserResource(self)
        return self._user

    @property
    def search(self) -> SearchResource:
        """搜索资源 (rest/api/search)"""
        if self._search is None:
            self._search = SearchResource(self)
        return self._search

    @property
    def notification(self) -> NotificationResource:
        """通知资源 (rest/notification) - 需要 MyWork Plugin"""
        if self._notification is None:
            self._notification = NotificationResource(self)
        return self._notification

    @property
    def group(self) -> GroupResource:
        """用户组资源 (rest/api/group)"""
        if self._group is None:
            self._group = GroupResource(self)
        return self._group

    @property
    def audit(self) -> AuditResource:
        """审计资源 (rest/audit) - 需要管理员权限"""
        if self._audit is None:
            self._audit = AuditResource(self)
        return self._audit

    @property
    def longtask(self) -> LongTaskResource:
        """长期任务资源 (rest/api/longtask)"""
        if self._longtask is None:
            self._longtask = LongTaskResource(self)
        return self._longtask

    # ========== 便捷方法 ==========

    async def get_current_user(self) -> dict:
        """获取当前登录用户信息（便捷方法）"""
        return await self.user.get_current_raw()

    async def get_spaces(self, start: int = 0, limit: int = 25) -> dict:
        """获取空间列表（便捷方法）"""
        return await self.get_json(
            "/rest/api/space",
            params={"start": start, "limit": limit},
        )

    async def get_space(self, space_key: str, expand: Optional[str] = None) -> dict:
        """获取空间详情（便捷方法）"""
        return await self.space.get_raw(space_key, expand=expand)

    async def get_content(
        self,
        content_id: str,
        expand: Optional[str] = None,
    ) -> dict:
        """获取内容（页面/博客）详情（便捷方法）"""
        return await self.content.get_raw(content_id, expand=expand)

    async def search_content(
        self,
        cql: str,
        start: int = 0,
        limit: int = 25,
        expand: Optional[str] = None,
    ) -> dict:
        """
        使用 CQL 搜索内容（便捷方法）

        Args:
            cql: Confluence Query Language 查询
            start: 起始位置
            limit: 返回数量
            expand: 展开的字段
        """
        return await self.search.search_raw(cql, expand=expand, start=start, limit=limit)
