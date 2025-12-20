"""
Group Resource - 用户组资源

GET    /rest/api/2/group                      - 获取用户组
POST   /rest/api/2/group                      - 创建用户组
DELETE /rest/api/2/group                      - 删除用户组
GET    /rest/api/2/group/bulk                 - 批量获取用户组
GET    /rest/api/2/group/member               - 获取用户组成员
POST   /rest/api/2/group/user                 - 添加用户到组
DELETE /rest/api/2/group/user                 - 从组中移除用户
GET    /rest/api/2/groups/picker              - 搜索用户组
"""

from typing import Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.group import Group, GroupMembers
from atlassian.jira.models.user import User


class GroupResource(BaseResource):
    """
    用户组资源

    API: /rest/api/2/group
    """

    BASE_PATH = "/rest/api/2/group"

    # ==================== Group Management ====================

    async def get(
        self,
        group_name: str,
        expand: Optional[str] = None,
    ) -> Group:
        """
        获取用户组详情

        GET /rest/api/2/group

        Args:
            group_name: 用户组名称
            expand: 扩展字段（可选，如"users"）

        Returns:
            Group: 用户组详情
        """
        params = {"groupname": group_name}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(self.BASE_PATH, params=params)
        return Group.model_validate(data)

    async def get_raw(
        self,
        group_name: str,
        expand: Optional[str] = None,
    ) -> dict:
        """获取用户组详情（原始JSON）"""
        params = {"groupname": group_name}
        if expand:
            params["expand"] = expand

        return await self.client.get_json(self.BASE_PATH, params=params)

    async def create(
        self,
        name: str,
    ) -> Group:
        """
        创建用户组

        POST /rest/api/2/group

        Args:
            name: 用户组名称

        Returns:
            Group: 创建的用户组
        """
        payload = {"name": name}
        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return Group.model_validate(data)

    async def create_raw(
        self,
        name: str,
    ) -> dict:
        """创建用户组（原始JSON）"""
        payload = {"name": name}
        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def delete(
        self,
        group_name: str,
        swap_group: Optional[str] = None,
    ) -> None:
        """
        删除用户组

        DELETE /rest/api/2/group

        Args:
            group_name: 要删除的用户组名称
            swap_group: 替换组名称（可选）。如果提供，删除组中的所有限制将被转移到此组
        """
        params = {"groupname": group_name}
        if swap_group:
            params["swapGroup"] = swap_group

        await self.client.delete(self.BASE_PATH, params=params)

    async def bulk_get(
        self,
        group_names: list[str],
        expand: Optional[str] = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict:
        """
        批量获取用户组

        GET /rest/api/2/group/bulk

        Args:
            group_names: 用户组名称列表
            expand: 扩展字段（可选）
            start_at: 起始位置（默认0）
            max_results: 最大结果数（默认50）

        Returns:
            dict: 包含分页信息和用户组列表的字典
        """
        path = f"{self.BASE_PATH}/bulk"
        params = {
            "groupname": ",".join(group_names),
            "startAt": start_at,
            "maxResults": max_results,
        }
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    # ==================== Group Members ====================

    async def get_members(
        self,
        group_name: str,
        include_inactive_users: bool = False,
        start_at: int = 0,
        max_results: int = 50,
    ) -> GroupMembers:
        """
        获取用户组成员列表

        GET /rest/api/2/group/member

        Args:
            group_name: 用户组名称
            include_inactive_users: 是否包含非活动用户（默认False）
            start_at: 起始位置（默认0）
            max_results: 最大结果数（默认50）

        Returns:
            GroupMembers: 包含分页信息的成员列表
        """
        path = f"{self.BASE_PATH}/member"
        params = {
            "groupname": group_name,
            "includeInactiveUsers": str(include_inactive_users).lower(),
            "startAt": start_at,
            "maxResults": max_results,
        }

        data = await self.client.get_json(path, params=params)
        return GroupMembers.model_validate(data)

    async def get_members_raw(
        self,
        group_name: str,
        include_inactive_users: bool = False,
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict:
        """获取用户组成员列表（原始JSON）"""
        path = f"{self.BASE_PATH}/member"
        params = {
            "groupname": group_name,
            "includeInactiveUsers": str(include_inactive_users).lower(),
            "startAt": start_at,
            "maxResults": max_results,
        }

        return await self.client.get_json(path, params=params)

    async def add_member(
        self,
        group_name: str,
        username: str,
    ) -> Group:
        """
        添加用户到用户组

        POST /rest/api/2/group/user

        Args:
            group_name: 用户组名称
            username: 要添加的用户名

        Returns:
            Group: 更新后的用户组
        """
        path = f"{self.BASE_PATH}/user"
        params = {"groupname": group_name}
        payload = {"name": username}

        data = await self.client.post_json(path, params=params, data=payload)
        return Group.model_validate(data)

    async def add_member_raw(
        self,
        group_name: str,
        username: str,
    ) -> dict:
        """添加用户到用户组（原始JSON）"""
        path = f"{self.BASE_PATH}/user"
        params = {"groupname": group_name}
        payload = {"name": username}

        return await self.client.post_json(path, params=params, data=payload)

    async def remove_member(
        self,
        group_name: str,
        username: str,
    ) -> None:
        """
        从用户组中移除用户

        DELETE /rest/api/2/group/user

        Args:
            group_name: 用户组名称
            username: 要移除的用户名
        """
        path = f"{self.BASE_PATH}/user"
        params = {
            "groupname": group_name,
            "username": username,
        }

        await self.client.delete(path, params=params)

    async def find(
        self,
        query: Optional[str] = None,
        exclude: Optional[list[str]] = None,
        max_results: int = 20,
    ) -> dict:
        """
        搜索用户组（Picker）

        GET /rest/api/2/groups/picker

        Args:
            query: 搜索查询字符串（可选）
            exclude: 要排除的用户组名称列表（可选）
            max_results: 最大结果数（默认20）

        Returns:
            dict: 搜索结果，包含用户组列表和分页信息
        """
        path = "/rest/api/2/groups/picker"
        params = {"maxResults": max_results}

        if query:
            params["query"] = query
        if exclude:
            params["exclude"] = ",".join(exclude)

        return await self.client.get_json(path, params=params)
