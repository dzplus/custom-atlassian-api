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
    SearchResource,
    ComponentResource,
    VersionResource,
    UserResource,
    FilterResource,
    GroupResource,
    WorkflowResource,
    WorkflowSchemeResource,
    StatusResource,
    ResolutionResource,
    PermissionSchemeResource,
    RoleResource,
    SecurityLevelResource,
    IssueTypeResource,
    IssueTypeSchemeResource,
    FieldResource,
    ScreenResource,
    PriorityResource,
    PrioritySchemeResource,
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
        self._search: Optional[SearchResource] = None
        self._component: Optional[ComponentResource] = None
        self._version: Optional[VersionResource] = None
        self._user: Optional[UserResource] = None
        self._filter: Optional[FilterResource] = None
        self._group: Optional[GroupResource] = None
        self._workflow: Optional[WorkflowResource] = None
        self._workflow_scheme: Optional[WorkflowSchemeResource] = None
        self._status: Optional[StatusResource] = None
        self._resolution: Optional[ResolutionResource] = None
        self._permission_scheme: Optional[PermissionSchemeResource] = None
        self._role: Optional[RoleResource] = None
        self._security_level: Optional[SecurityLevelResource] = None
        self._issue_type: Optional[IssueTypeResource] = None
        self._issue_type_scheme: Optional[IssueTypeSchemeResource] = None
        self._field: Optional[FieldResource] = None
        self._screen: Optional[ScreenResource] = None
        self._priority: Optional[PriorityResource] = None
        self._priority_scheme: Optional[PrioritySchemeResource] = None

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

    @property
    def search(self) -> SearchResource:
        """搜索资源 (api/2/search)"""
        if self._search is None:
            self._search = SearchResource(self)
        return self._search

    @property
    def component(self) -> ComponentResource:
        """组件资源 (api/2/component)"""
        if self._component is None:
            self._component = ComponentResource(self)
        return self._component

    @property
    def version(self) -> VersionResource:
        """版本资源 (api/2/version)"""
        if self._version is None:
            self._version = VersionResource(self)
        return self._version

    @property
    def user(self) -> UserResource:
        """用户资源 (api/2/user)"""
        if self._user is None:
            self._user = UserResource(self)
        return self._user

    @property
    def filter(self) -> FilterResource:
        """过滤器资源 (api/2/filter)"""
        if self._filter is None:
            self._filter = FilterResource(self)
        return self._filter

    @property
    def group(self) -> GroupResource:
        """用户组资源 (api/2/group)"""
        if self._group is None:
            self._group = GroupResource(self)
        return self._group

    @property
    def workflow(self) -> WorkflowResource:
        """工作流资源 (api/2/workflow)"""
        if self._workflow is None:
            self._workflow = WorkflowResource(self)
        return self._workflow

    @property
    def workflow_scheme(self) -> WorkflowSchemeResource:
        """工作流方案资源 (api/2/workflowscheme)"""
        if self._workflow_scheme is None:
            self._workflow_scheme = WorkflowSchemeResource(self)
        return self._workflow_scheme

    @property
    def status(self) -> StatusResource:
        """状态资源 (api/2/status)"""
        if self._status is None:
            self._status = StatusResource(self)
        return self._status

    @property
    def resolution(self) -> ResolutionResource:
        """解决方案资源 (api/2/resolution)"""
        if self._resolution is None:
            self._resolution = ResolutionResource(self)
        return self._resolution

    @property
    def permission_scheme(self) -> PermissionSchemeResource:
        """权限方案资源 (api/2/permissionscheme)"""
        if self._permission_scheme is None:
            self._permission_scheme = PermissionSchemeResource(self)
        return self._permission_scheme

    @property
    def role(self) -> RoleResource:
        """角色资源 (api/2/role)"""
        if self._role is None:
            self._role = RoleResource(self)
        return self._role

    @property
    def security_level(self) -> SecurityLevelResource:
        """安全级别资源 (api/2/securitylevel)"""
        if self._security_level is None:
            self._security_level = SecurityLevelResource(self)
        return self._security_level

    @property
    def issue_type(self) -> IssueTypeResource:
        """Issue类型资源 (api/2/issuetype)"""
        if self._issue_type is None:
            self._issue_type = IssueTypeResource(self)
        return self._issue_type

    @property
    def issue_type_scheme(self) -> IssueTypeSchemeResource:
        """Issue类型方案资源 (api/2/issuetypescheme)"""
        if self._issue_type_scheme is None:
            self._issue_type_scheme = IssueTypeSchemeResource(self)
        return self._issue_type_scheme

    @property
    def field(self) -> FieldResource:
        """字段资源 (api/2/field)"""
        if self._field is None:
            self._field = FieldResource(self)
        return self._field

    @property
    def screen(self) -> ScreenResource:
        """屏幕资源 (api/2/screens)"""
        if self._screen is None:
            self._screen = ScreenResource(self)
        return self._screen

    @property
    def priority(self) -> PriorityResource:
        """优先级资源 (api/2/priority)"""
        if self._priority is None:
            self._priority = PriorityResource(self)
        return self._priority

    @property
    def priority_scheme(self) -> PrioritySchemeResource:
        """优先级方案资源 (api/2/priorityscheme)"""
        if self._priority_scheme is None:
            self._priority_scheme = PrioritySchemeResource(self)
        return self._priority_scheme

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
