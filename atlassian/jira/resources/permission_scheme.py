"""
Permission Scheme Resource - 权限方案资源

Scheme CRUD:
GET    /rest/api/2/permissionscheme                              - 获取所有权限方案
POST   /rest/api/2/permissionscheme                              - 创建权限方案
GET    /rest/api/2/permissionscheme/{id}                         - 获取权限方案
PUT    /rest/api/2/permissionscheme/{id}                         - 更新权限方案
DELETE /rest/api/2/permissionscheme/{id}                         - 删除权限方案

Permission Grants:
POST   /rest/api/2/permissionscheme/{id}/permission              - 创建权限授予
GET    /rest/api/2/permissionscheme/{id}/permission/{permissionId} - 获取权限授予
DELETE /rest/api/2/permissionscheme/{id}/permission/{permissionId} - 删除权限授予

Attributes:
GET    /rest/api/2/permissionscheme/{id}/permission/{permissionId}/attributes - 获取权限属性
PUT    /rest/api/2/permissionscheme/{id}/permission/{permissionId}/attributes - 更新权限属性
DELETE /rest/api/2/permissionscheme/{id}/permission/{permissionId}/attributes - 删除权限属性
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.permission import PermissionScheme, PermissionGrant


class PermissionSchemeResource(BaseResource):
    """
    权限方案资源

    API: /rest/api/2/permissionscheme
    """

    BASE_PATH = "/rest/api/2/permissionscheme"

    # ==================== Scheme CRUD ====================

    async def get_all(
        self,
        expand: Optional[str] = None,
    ) -> list[PermissionScheme]:
        """
        获取所有权限方案

        GET /rest/api/2/permissionscheme

        Args:
            expand: 扩展字段（可选，如"permissions,user,group,projectRole"）

        Returns:
            list[PermissionScheme]: 权限方案列表
        """
        params = {}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(self.BASE_PATH, params=params)
        # API 返回 {"permissionSchemes": [...]}
        schemes = data.get("permissionSchemes", [])
        return [PermissionScheme.model_validate(s) for s in schemes]

    async def get_all_raw(
        self,
        expand: Optional[str] = None,
    ) -> dict:
        """获取所有权限方案（原始JSON）"""
        params = {}
        if expand:
            params["expand"] = expand

        return await self.client.get_json(self.BASE_PATH, params=params)

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        permissions: Optional[list[dict]] = None,
    ) -> PermissionScheme:
        """
        创建权限方案

        POST /rest/api/2/permissionscheme

        Args:
            name: 方案名称
            description: 方案描述（可选）
            permissions: 权限列表（可选）

        Returns:
            PermissionScheme: 创建的权限方案
        """
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        if permissions:
            payload["permissions"] = permissions

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return PermissionScheme.model_validate(data)

    async def create_raw(
        self,
        name: str,
        description: Optional[str] = None,
        permissions: Optional[list[dict]] = None,
    ) -> dict:
        """创建权限方案（原始JSON）"""
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        if permissions:
            payload["permissions"] = permissions

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def get(
        self,
        scheme_id: int,
        expand: Optional[str] = None,
    ) -> PermissionScheme:
        """
        获取权限方案

        GET /rest/api/2/permissionscheme/{id}

        Args:
            scheme_id: 方案ID
            expand: 扩展字段（可选）

        Returns:
            PermissionScheme: 权限方案详情
        """
        path = f"{self.BASE_PATH}/{scheme_id}"
        params = {}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return PermissionScheme.model_validate(data)

    async def get_raw(
        self,
        scheme_id: int,
        expand: Optional[str] = None,
    ) -> dict:
        """获取权限方案（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}"
        params = {}
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    async def update(
        self,
        scheme_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        permissions: Optional[list[dict]] = None,
    ) -> PermissionScheme:
        """
        更新权限方案

        PUT /rest/api/2/permissionscheme/{id}

        Args:
            scheme_id: 方案ID
            name: 方案名称（可选）
            description: 方案描述（可选）
            permissions: 权限列表（可选）

        Returns:
            PermissionScheme: 更新后的权限方案
        """
        path = f"{self.BASE_PATH}/{scheme_id}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if permissions:
            payload["permissions"] = permissions

        data = await self.client.put_json(path, data=payload)
        return PermissionScheme.model_validate(data)

    async def update_raw(
        self,
        scheme_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        permissions: Optional[list[dict]] = None,
    ) -> dict:
        """更新权限方案（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if permissions:
            payload["permissions"] = permissions

        return await self.client.put_json(path, data=payload)

    async def delete(
        self,
        scheme_id: int,
    ) -> None:
        """
        删除权限方案

        DELETE /rest/api/2/permissionscheme/{id}

        Args:
            scheme_id: 方案ID
        """
        path = f"{self.BASE_PATH}/{scheme_id}"
        await self.client.delete(path)

    # ==================== Permission Grants ====================

    async def create_permission_grant(
        self,
        scheme_id: int,
        permission: str,
        holder: dict,
    ) -> PermissionGrant:
        """
        创建权限授予

        POST /rest/api/2/permissionscheme/{id}/permission

        Args:
            scheme_id: 方案ID
            permission: 权限key（如"ADMINISTER_PROJECTS"）
            holder: 权限持有者信息，如{"type": "group", "parameter": "jira-administrators"}

        Returns:
            PermissionGrant: 创建的权限授予
        """
        path = f"{self.BASE_PATH}/{scheme_id}/permission"
        payload = {
            "permission": permission,
            "holder": holder,
        }

        data = await self.client.post_json(path, data=payload)
        return PermissionGrant.model_validate(data)

    async def create_permission_grant_raw(
        self,
        scheme_id: int,
        permission: str,
        holder: dict,
    ) -> dict:
        """创建权限授予（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/permission"
        payload = {
            "permission": permission,
            "holder": holder,
        }

        return await self.client.post_json(path, data=payload)

    async def get_permission_grant(
        self,
        scheme_id: int,
        permission_id: int,
        expand: Optional[str] = None,
    ) -> PermissionGrant:
        """
        获取权限授予

        GET /rest/api/2/permissionscheme/{id}/permission/{permissionId}

        Args:
            scheme_id: 方案ID
            permission_id: 权限ID
            expand: 扩展字段（可选）

        Returns:
            PermissionGrant: 权限授予详情
        """
        path = f"{self.BASE_PATH}/{scheme_id}/permission/{permission_id}"
        params = {}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return PermissionGrant.model_validate(data)

    async def get_permission_grant_raw(
        self,
        scheme_id: int,
        permission_id: int,
        expand: Optional[str] = None,
    ) -> dict:
        """获取权限授予（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/permission/{permission_id}"
        params = {}
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    async def delete_permission_grant(
        self,
        scheme_id: int,
        permission_id: int,
    ) -> None:
        """
        删除权限授予

        DELETE /rest/api/2/permissionscheme/{id}/permission/{permissionId}

        Args:
            scheme_id: 方案ID
            permission_id: 权限ID
        """
        path = f"{self.BASE_PATH}/{scheme_id}/permission/{permission_id}"
        await self.client.delete(path)
