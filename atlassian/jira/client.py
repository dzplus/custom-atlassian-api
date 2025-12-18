"""
Jira Client - Jira HTTP 客户端

提供统一的 Jira API 访问入口，整合所有资源类
"""

from typing import Optional

from atlassian.common.client import BaseHttpClient, AuthMode
from atlassian.jira.resources import (
    MyselfResource,
    IssueResource,
    IssueLinkResource,
    IssueLinkTypeResource,
    AttachmentResource,
    CustomFieldsResource,
    ProjectResource,
)


class JiraClient(BaseHttpClient):
    """
    Jira API 客户端

    整合所有 Jira API 资源，提供统一访问入口

    用法:
        async with JiraClient() as jira:
            # 获取当前用户
            user = await jira.myself.get()

            # 获取 Issue
            issue = await jira.issue.get("DEMO-123")

            # 创建 Issue
            result = await jira.issue.create(
                project="DEMO",
                summary="Test issue",
                issue_type="Bug",
            )

    环境变量:
        JIRA_URL: Jira 服务地址
        JIRA_USERNAME: 用户名
        JIRA_PASSWORD: 密码

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
        auth_mode: AuthMode = "basic",
    ):
        """
        初始化 Jira 客户端

        Args:
            base_url: Jira 服务地址，默认从 JIRA_URL 环境变量读取
            username: 用户名，默认从 JIRA_USERNAME 环境变量读取
            password: 密码，默认从 JIRA_PASSWORD 环境变量读取
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
            env_prefix="JIRA",
            auth_mode=auth_mode,
        )

        # 初始化资源
        self._myself: Optional[MyselfResource] = None
        self._issue: Optional[IssueResource] = None
        self._issue_link: Optional[IssueLinkResource] = None
        self._issue_link_type: Optional[IssueLinkTypeResource] = None
        self._attachment: Optional[AttachmentResource] = None
        self._custom_fields: Optional[CustomFieldsResource] = None
        self._project: Optional[ProjectResource] = None

    @property
    def myself(self) -> MyselfResource:
        """当前用户资源 (api/2/myself)"""
        if self._myself is None:
            self._myself = MyselfResource(self)
        return self._myself

    @property
    def issue(self) -> IssueResource:
        """Issue 资源 (api/2/issue)"""
        if self._issue is None:
            self._issue = IssueResource(self)
        return self._issue

    @property
    def issue_link(self) -> IssueLinkResource:
        """Issue 链接资源 (api/2/issueLink)"""
        if self._issue_link is None:
            self._issue_link = IssueLinkResource(self)
        return self._issue_link

    @property
    def issue_link_type(self) -> IssueLinkTypeResource:
        """Issue 链接类型资源 (api/2/issueLinkType)"""
        if self._issue_link_type is None:
            self._issue_link_type = IssueLinkTypeResource(self)
        return self._issue_link_type

    @property
    def attachment(self) -> AttachmentResource:
        """附件资源 (api/2/attachment)"""
        if self._attachment is None:
            self._attachment = AttachmentResource(self)
        return self._attachment

    @property
    def custom_fields(self) -> CustomFieldsResource:
        """自定义字段资源 (api/2/customFields)"""
        if self._custom_fields is None:
            self._custom_fields = CustomFieldsResource(self)
        return self._custom_fields

    @property
    def project(self) -> ProjectResource:
        """项目资源 (api/2/project)"""
        if self._project is None:
            self._project = ProjectResource(self)
        return self._project

    # ========== 便捷方法 ==========

    async def get_myself(self) -> dict:
        """获取当前登录用户信息（便捷方法）"""
        return await self.myself.get_raw()

    async def get_issue(self, issue_key: str, expand: Optional[str] = None) -> dict:
        """获取 Issue 详情（便捷方法）"""
        return await self.issue.get_raw(issue_key, expand=expand)

    async def search_issues(self, jql: str, start_at: int = 0, max_results: int = 50) -> dict:
        """JQL 搜索（便捷方法）"""
        return await self.post_json(
            "/rest/api/2/search",
            data={
                "jql": jql,
                "startAt": start_at,
                "maxResults": max_results,
            },
        )
