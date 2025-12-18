"""
Tempo Client - Tempo Server/Data Center HTTP 客户端

Tempo 是 Jira 的插件，使用与 Jira 相同的认证和 Base URL

提供统一的 Tempo API 访问入口:
- Timesheets (工时记录)
- Accounts (账户)
- Teams (团队)
"""

from typing import Optional

from atlassian.common.client import BaseHttpClient, AuthMode
from atlassian.tempo.resources import (
    WorklogResource,
    AccountResource,
    TeamResource,
    PlanResource,
)


class TempoClient(BaseHttpClient):
    """
    Tempo API 客户端

    整合 Tempo Timesheets, Accounts, Teams API

    注意: Tempo 是 Jira 的插件，使用与 Jira 相同的 URL 和认证信息

    用法:
        async with TempoClient() as tempo:
            # 搜索工时记录
            worklogs = await tempo.worklog.search(
                from_date="2024-01-01",
                to_date="2024-01-31",
            )

            # 获取所有团队
            teams = await tempo.team.get_all()

            # 获取所有账户
            accounts = await tempo.account.get_all()

    环境变量 (可使用 Jira 的环境变量):
        TEMPO_URL 或 JIRA_URL: Jira 服务地址
        TEMPO_USERNAME 或 JIRA_USERNAME: 用户名
        TEMPO_PASSWORD 或 JIRA_PASSWORD: 密码

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
        初始化 Tempo 客户端

        Args:
            base_url: Jira 服务地址，默认从 TEMPO_URL 或 JIRA_URL 环境变量读取
            username: 用户名，默认从 TEMPO_USERNAME 或 JIRA_USERNAME 环境变量读取
            password: 密码，默认从 TEMPO_PASSWORD 或 JIRA_PASSWORD 环境变量读取
            timeout: 请求超时时间（秒）
            auto_login: 是否在首次请求时自动登录 (仅 session 模式)
            auto_relogin: 会话过期时是否自动重新登录 (仅 session 模式)
            auth_mode: 认证模式，"basic" (默认) 或 "session"
        """
        # Tempo 可以使用 JIRA 的环境变量作为后备
        import os
        resolved_url = (
            base_url
            or os.getenv("TEMPO_URL")
            or os.getenv("JIRA_URL")
            or os.getenv("ATLASSIAN_URL")
        )
        resolved_username = (
            username
            or os.getenv("TEMPO_USERNAME")
            or os.getenv("JIRA_USERNAME")
            or os.getenv("ATLASSIAN_USERNAME")
        )
        resolved_password = (
            password
            or os.getenv("TEMPO_PASSWORD")
            or os.getenv("JIRA_PASSWORD")
            or os.getenv("ATLASSIAN_PASSWORD")
        )

        super().__init__(
            base_url=resolved_url,
            username=resolved_username,
            password=resolved_password,
            timeout=timeout,
            auto_login=auto_login,
            auto_relogin=auto_relogin,
            env_prefix="TEMPO",
            auth_mode=auth_mode,
        )

        # 初始化资源
        self._worklog: Optional[WorklogResource] = None
        self._account: Optional[AccountResource] = None
        self._team: Optional[TeamResource] = None
        self._plan: Optional[PlanResource] = None

    @property
    def worklog(self) -> WorklogResource:
        """工时记录资源 (tempo-timesheets/4/worklogs)"""
        if self._worklog is None:
            self._worklog = WorklogResource(self)
        return self._worklog

    @property
    def account(self) -> AccountResource:
        """账户资源 (tempo-accounts/1/account)"""
        if self._account is None:
            self._account = AccountResource(self)
        return self._account

    @property
    def team(self) -> TeamResource:
        """团队资源 (tempo-teams/2/team)"""
        if self._team is None:
            self._team = TeamResource(self)
        return self._team

    @property
    def plan(self) -> PlanResource:
        """计划资源 (tempo-planning/1/allocation, tempo-planning/1/plan)"""
        if self._plan is None:
            self._plan = PlanResource(self)
        return self._plan

    # ========== 便捷方法 ==========

    async def get_worklogs(
        self,
        from_date: str,
        to_date: str,
        worker: Optional[list[str]] = None,
    ) -> list:
        """
        获取工时记录（便捷方法）

        Args:
            from_date: 开始日期 "2024-01-01"
            to_date: 结束日期 "2024-01-31"
            worker: 工作者用户 key 列表

        Returns:
            list[Worklog]: 工时记录列表
        """
        return await self.worklog.search(
            from_date=from_date,
            to_date=to_date,
            worker=worker,
        )

    async def get_teams(self) -> list:
        """获取所有团队（便捷方法）"""
        return await self.team.get_all()

    async def get_accounts(self) -> list:
        """获取所有账户（便捷方法）"""
        return await self.account.get_all()
