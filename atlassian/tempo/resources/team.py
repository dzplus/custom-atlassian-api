"""
Tempo Team 资源

API: /rest/tempo-teams/2/team
"""

from typing import Optional
from atlassian.common.base import BaseResource
from atlassian.tempo.models.team import Team, TeamMember


class TeamResource(BaseResource):
    """
    Tempo 团队资源

    API 端点:
    - GET /team - 获取所有团队
    - POST /team - 创建团队
    - GET /team/{id} - 获取团队
    - GET /team/{id}/member - 获取团队成员
    - POST /team/{id}/member - 添加团队成员
    """

    BASE_PATH = "/rest/tempo-teams/2/team"

    async def get_all(
        self,
        expand_program: bool = False,
        expand_lead: bool = False,
    ) -> list[Team]:
        """
        获取所有团队

        Args:
            expand_program: 是否展开 Program 信息
            expand_lead: 是否展开 Lead 用户信息

        Returns:
            list[Team]: 团队列表
        """
        params = {}
        expand = []
        if expand_program:
            expand.append("program")
        if expand_lead:
            expand.append("lead.user")
        if expand:
            params["expand"] = ",".join(expand)

        data = await self._client.get_json(self.BASE_PATH, params=params)
        return [Team.model_validate(item) for item in data]

    async def get_all_raw(self) -> list[dict]:
        """获取所有团队原始数据"""
        return await self._client.get_json(self.BASE_PATH)

    async def get(self, team_id: int) -> Team:
        """
        获取团队

        Args:
            team_id: 团队 ID

        Returns:
            Team: 团队
        """
        data = await self._client.get_json(f"{self.BASE_PATH}/{team_id}")
        return Team.model_validate(data)

    async def get_raw(self, team_id: int) -> dict:
        """获取团队原始数据"""
        return await self._client.get_json(f"{self.BASE_PATH}/{team_id}")

    async def create(
        self,
        name: str,
        summary: Optional[str] = None,
        lead_username: Optional[str] = None,
    ) -> Team:
        """
        创建团队

        Args:
            name: 团队名称
            summary: 团队描述
            lead_username: 负责人用户名

        Returns:
            Team: 创建的团队
        """
        team_data = {"name": name}
        if summary:
            team_data["summary"] = summary
        if lead_username:
            team_data["leadUsername"] = lead_username

        data = await self._client.post_json(self.BASE_PATH, data=team_data)
        return Team.model_validate(data)

    async def get_members(
        self,
        team_id: int,
        active_only: bool = True,
        member_type: Optional[str] = None,
    ) -> list[TeamMember]:
        """
        获取团队成员

        Args:
            team_id: 团队 ID
            active_only: 仅返回活跃成员
            member_type: 成员类型 (USER, TEAM)

        Returns:
            list[TeamMember]: 成员列表
        """
        params = {}
        if not active_only:
            params["activeOnly"] = "false"
        if member_type:
            params["type"] = member_type

        data = await self._client.get_json(
            f"{self.BASE_PATH}/{team_id}/member",
            params=params,
        )
        return [TeamMember.model_validate(item) for item in data]

    async def get_members_raw(self, team_id: int) -> list[dict]:
        """获取团队成员原始数据"""
        return await self._client.get_json(f"{self.BASE_PATH}/{team_id}/member")

    async def add_member(
        self,
        team_id: int,
        member_key: str,
        role_id: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        commitment_percent: Optional[int] = None,
    ) -> TeamMember:
        """
        添加团队成员

        Args:
            team_id: 团队 ID
            member_key: 成员用户 key
            role_id: 角色 ID
            date_from: 开始日期
            date_to: 结束日期
            commitment_percent: 承诺百分比

        Returns:
            TeamMember: 添加的成员
        """
        member_data = {"memberKey": member_key}
        if role_id is not None:
            member_data["roleId"] = role_id
        if date_from:
            member_data["dateFrom"] = date_from
        if date_to:
            member_data["dateTo"] = date_to
        if commitment_percent is not None:
            member_data["commitmentPercent"] = commitment_percent

        data = await self._client.post_json(
            f"{self.BASE_PATH}/{team_id}/member",
            data=member_data,
        )
        return TeamMember.model_validate(data)

    async def update_member(
        self,
        team_id: int,
        member_id: int,
        role_id: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        commitment_percent: Optional[int] = None,
    ) -> TeamMember:
        """
        更新团队成员

        Args:
            team_id: 团队 ID
            member_id: 成员 ID
            role_id: 角色 ID
            date_from: 开始日期
            date_to: 结束日期
            commitment_percent: 承诺百分比

        Returns:
            TeamMember: 更新后的成员
        """
        update_data = {}
        if role_id is not None:
            update_data["roleId"] = role_id
        if date_from:
            update_data["dateFrom"] = date_from
        if date_to:
            update_data["dateTo"] = date_to
        if commitment_percent is not None:
            update_data["commitmentPercent"] = commitment_percent

        data = await self._client.put_json(
            f"{self.BASE_PATH}/{team_id}/member/{member_id}",
            data=update_data,
        )
        return TeamMember.model_validate(data)
