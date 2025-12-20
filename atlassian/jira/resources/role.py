"""
Role Resource - 角色资源

GET    /rest/api/2/role                               - 获取所有角色
POST   /rest/api/2/role                               - 创建角色
GET    /rest/api/2/role/{id}                          - 获取角色
PUT    /rest/api/2/role/{id}                          - 更新角色
DELETE /rest/api/2/role/{id}                          - 删除角色
POST   /rest/api/2/role/{id}/actors                   - 添加角色执行者
DELETE /rest/api/2/role/{id}/actors                   - 删除角色执行者
GET    /rest/api/2/project/{projectIdOrKey}/role      - 获取项目角色（已在ProjectResource中实现）
GET    /rest/api/2/project/{projectIdOrKey}/role/{id} - 获取项目角色详情（已在ProjectResource中实现）
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.permission import Role, RoleActor


class RoleResource(BaseResource):
    """
    角色资源

    API: /rest/api/2/role
    """

    BASE_PATH = "/rest/api/2/role"

    # ==================== Role Management ====================

    async def get_all(self) -> list[Role]:
        """
        获取所有角色

        GET /rest/api/2/role

        Returns:
            list[Role]: 角色列表
        """
        data = await self.client.get_json(self.BASE_PATH)
        return [Role.model_validate(r) for r in data]

    async def get_all_raw(self) -> list[dict]:
        """获取所有角色（原始JSON）"""
        return await self.client.get_json(self.BASE_PATH)

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
    ) -> Role:
        """
        创建角色

        POST /rest/api/2/role

        Args:
            name: 角色名称
            description: 角色描述（可选）

        Returns:
            Role: 创建的角色
        """
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return Role.model_validate(data)

    async def create_raw(
        self,
        name: str,
        description: Optional[str] = None,
    ) -> dict:
        """创建角色（原始JSON）"""
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def get(
        self,
        role_id: int,
    ) -> Role:
        """
        获取角色详情

        GET /rest/api/2/role/{id}

        Args:
            role_id: 角色ID

        Returns:
            Role: 角色详情
        """
        path = f"{self.BASE_PATH}/{role_id}"
        data = await self.client.get_json(path)
        return Role.model_validate(data)

    async def get_raw(
        self,
        role_id: int,
    ) -> dict:
        """获取角色详情（原始JSON）"""
        path = f"{self.BASE_PATH}/{role_id}"
        return await self.client.get_json(path)

    async def update(
        self,
        role_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Role:
        """
        更新角色

        PUT /rest/api/2/role/{id}

        Args:
            role_id: 角色ID
            name: 角色名称（可选）
            description: 角色描述（可选）

        Returns:
            Role: 更新后的角色
        """
        path = f"{self.BASE_PATH}/{role_id}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description

        data = await self.client.put_json(path, data=payload)
        return Role.model_validate(data)

    async def update_raw(
        self,
        role_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> dict:
        """更新角色（原始JSON）"""
        path = f"{self.BASE_PATH}/{role_id}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description

        return await self.client.put_json(path, data=payload)

    async def delete(
        self,
        role_id: int,
        swap_role_id: Optional[int] = None,
    ) -> None:
        """
        删除角色

        DELETE /rest/api/2/role/{id}

        Args:
            role_id: 要删除的角色ID
            swap_role_id: 替换角色ID（可选）。如果提供，删除角色中的所有关联将被转移到此角色
        """
        path = f"{self.BASE_PATH}/{role_id}"
        params = {}
        if swap_role_id:
            params["swapRoleId"] = swap_role_id

        await self.client.delete(path, params=params)

    # ==================== Role Actors ====================

    async def add_actors(
        self,
        role_id: int,
        user: Optional[list[str]] = None,
        group: Optional[list[str]] = None,
    ) -> Role:
        """
        添加角色执行者

        POST /rest/api/2/role/{id}/actors

        Args:
            role_id: 角色ID
            user: 用户名列表（可选）
            group: 用户组名列表（可选）

        Returns:
            Role: 更新后的角色
        """
        path = f"{self.BASE_PATH}/{role_id}/actors"
        payload: dict[str, Any] = {}
        if user:
            payload["user"] = user
        if group:
            payload["group"] = group

        data = await self.client.post_json(path, data=payload)
        return Role.model_validate(data)

    async def add_actors_raw(
        self,
        role_id: int,
        user: Optional[list[str]] = None,
        group: Optional[list[str]] = None,
    ) -> dict:
        """添加角色执行者（原始JSON）"""
        path = f"{self.BASE_PATH}/{role_id}/actors"
        payload: dict[str, Any] = {}
        if user:
            payload["user"] = user
        if group:
            payload["group"] = group

        return await self.client.post_json(path, data=payload)

    async def delete_actors(
        self,
        role_id: int,
        user: Optional[str] = None,
        group: Optional[str] = None,
    ) -> Role:
        """
        删除角色执行者

        DELETE /rest/api/2/role/{id}/actors

        Args:
            role_id: 角色ID
            user: 用户名（可选）
            group: 用户组名（可选）

        Returns:
            Role: 更新后的角色
        """
        path = f"{self.BASE_PATH}/{role_id}/actors"
        params: dict[str, Any] = {}
        if user:
            params["user"] = user
        if group:
            params["group"] = group

        data = await self.client.delete(path, params=params)
        return Role.model_validate(data)

    async def delete_actors_raw(
        self,
        role_id: int,
        user: Optional[str] = None,
        group: Optional[str] = None,
    ) -> dict:
        """删除角色执行者（原始JSON）"""
        path = f"{self.BASE_PATH}/{role_id}/actors"
        params: dict[str, Any] = {}
        if user:
            params["user"] = user
        if group:
            params["group"] = group

        return await self.client.delete(path, params=params)
