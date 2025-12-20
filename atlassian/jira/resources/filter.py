"""
Filter Resource - 过滤器资源

GET    /rest/api/2/filter/{id}                    - 获取过滤器
POST   /rest/api/2/filter                         - 创建过滤器
PUT    /rest/api/2/filter/{id}                    - 更新过滤器
DELETE /rest/api/2/filter/{id}                    - 删除过滤器
GET    /rest/api/2/filter/{id}/columns            - 获取过滤器列
PUT    /rest/api/2/filter/{id}/columns            - 设置过滤器列
DELETE /rest/api/2/filter/{id}/columns            - 重置过滤器列
GET    /rest/api/2/filter/{id}/permission         - 获取过滤器权限
POST   /rest/api/2/filter/{id}/permission         - 添加过滤器权限
GET    /rest/api/2/filter/{id}/permission/{id}    - 获取单个过滤器权限
DELETE /rest/api/2/filter/{id}/permission/{id}    - 删除过滤器权限
PUT    /rest/api/2/filter/{id}/favourite          - 收藏过滤器
DELETE /rest/api/2/filter/{id}/favourite          - 取消收藏过滤器
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.filter import Filter, FilterPermission, Column


class FilterResource(BaseResource):
    """
    过滤器资源

    API: /rest/api/2/filter
    """

    BASE_PATH = "/rest/api/2/filter"

    # ==================== Filter CRUD ====================

    async def get(
        self,
        filter_id: str,
        expand: Optional[str] = None,
    ) -> Filter:
        """
        获取过滤器详情

        GET /rest/api/2/filter/{id}

        Args:
            filter_id: 过滤器ID
            expand: 扩展字段（可选，如"sharePermissions,subscriptions"）

        Returns:
            Filter: 过滤器详情
        """
        path = f"{self.BASE_PATH}/{filter_id}"
        params = {}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return Filter.model_validate(data)

    async def get_raw(
        self,
        filter_id: str,
        expand: Optional[str] = None,
    ) -> dict:
        """获取过滤器详情（原始JSON）"""
        path = f"{self.BASE_PATH}/{filter_id}"
        params = {}
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    async def create(
        self,
        name: str,
        jql: str,
        description: Optional[str] = None,
        favourite: bool = False,
        share_permissions: Optional[list[dict]] = None,
    ) -> Filter:
        """
        创建过滤器

        POST /rest/api/2/filter

        Args:
            name: 过滤器名称
            jql: JQL查询语句
            description: 描述（可选）
            favourite: 是否收藏（默认False）
            share_permissions: 共享权限列表（可选）

        Returns:
            Filter: 创建的过滤器
        """
        payload: dict[str, Any] = {
            "name": name,
            "jql": jql,
            "favourite": favourite,
        }
        if description:
            payload["description"] = description
        if share_permissions:
            payload["sharePermissions"] = share_permissions

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return Filter.model_validate(data)

    async def create_raw(
        self,
        name: str,
        jql: str,
        description: Optional[str] = None,
        favourite: bool = False,
        share_permissions: Optional[list[dict]] = None,
    ) -> dict:
        """创建过滤器（原始JSON）"""
        payload: dict[str, Any] = {
            "name": name,
            "jql": jql,
            "favourite": favourite,
        }
        if description:
            payload["description"] = description
        if share_permissions:
            payload["sharePermissions"] = share_permissions

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def update(
        self,
        filter_id: str,
        name: Optional[str] = None,
        jql: Optional[str] = None,
        description: Optional[str] = None,
        favourite: Optional[bool] = None,
        share_permissions: Optional[list[dict]] = None,
    ) -> Filter:
        """
        更新过滤器

        PUT /rest/api/2/filter/{id}

        Args:
            filter_id: 过滤器ID
            name: 过滤器名称（可选）
            jql: JQL查询语句（可选）
            description: 描述（可选）
            favourite: 是否收藏（可选）
            share_permissions: 共享权限列表（可选）

        Returns:
            Filter: 更新后的过滤器
        """
        path = f"{self.BASE_PATH}/{filter_id}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if jql:
            payload["jql"] = jql
        if description:
            payload["description"] = description
        if favourite is not None:
            payload["favourite"] = favourite
        if share_permissions:
            payload["sharePermissions"] = share_permissions

        data = await self.client.put_json(path, data=payload)
        return Filter.model_validate(data)

    async def update_raw(
        self,
        filter_id: str,
        name: Optional[str] = None,
        jql: Optional[str] = None,
        description: Optional[str] = None,
        favourite: Optional[bool] = None,
        share_permissions: Optional[list[dict]] = None,
    ) -> dict:
        """更新过滤器（原始JSON）"""
        path = f"{self.BASE_PATH}/{filter_id}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if jql:
            payload["jql"] = jql
        if description:
            payload["description"] = description
        if favourite is not None:
            payload["favourite"] = favourite
        if share_permissions:
            payload["sharePermissions"] = share_permissions

        return await self.client.put_json(path, data=payload)

    async def delete(
        self,
        filter_id: str,
    ) -> None:
        """
        删除过滤器

        DELETE /rest/api/2/filter/{id}

        Args:
            filter_id: 过滤器ID
        """
        path = f"{self.BASE_PATH}/{filter_id}"
        await self.client.delete(path)

    # ==================== Columns ====================

    async def get_columns(
        self,
        filter_id: str,
    ) -> list[Column]:
        """
        获取过滤器的列定义

        GET /rest/api/2/filter/{id}/columns

        Args:
            filter_id: 过滤器ID

        Returns:
            list[Column]: 列定义列表
        """
        path = f"{self.BASE_PATH}/{filter_id}/columns"
        data = await self.client.get_json(path)
        return [Column.model_validate(c) for c in data]

    async def get_columns_raw(
        self,
        filter_id: str,
    ) -> list[dict]:
        """获取过滤器的列定义（原始JSON）"""
        path = f"{self.BASE_PATH}/{filter_id}/columns"
        return await self.client.get_json(path)

    async def set_columns(
        self,
        filter_id: str,
        columns: list[str],
    ) -> dict:
        """
        设置过滤器的列

        PUT /rest/api/2/filter/{id}/columns

        Args:
            filter_id: 过滤器ID
            columns: 列名列表

        Returns:
            dict: 操作结果
        """
        path = f"{self.BASE_PATH}/{filter_id}/columns"
        return await self.client.put_json(path, data=columns)

    async def reset_columns(
        self,
        filter_id: str,
    ) -> None:
        """
        重置过滤器的列为默认值

        DELETE /rest/api/2/filter/{id}/columns

        Args:
            filter_id: 过滤器ID
        """
        path = f"{self.BASE_PATH}/{filter_id}/columns"
        await self.client.delete(path)

    # ==================== Share Permissions ====================

    async def get_permissions(
        self,
        filter_id: str,
    ) -> list[FilterPermission]:
        """
        获取过滤器的共享权限列表

        GET /rest/api/2/filter/{id}/permission

        Args:
            filter_id: 过滤器ID

        Returns:
            list[FilterPermission]: 权限列表
        """
        path = f"{self.BASE_PATH}/{filter_id}/permission"
        data = await self.client.get_json(path)
        return [FilterPermission.model_validate(p) for p in data]

    async def get_permissions_raw(
        self,
        filter_id: str,
    ) -> list[dict]:
        """获取过滤器的共享权限列表（原始JSON）"""
        path = f"{self.BASE_PATH}/{filter_id}/permission"
        return await self.client.get_json(path)

    async def add_permission(
        self,
        filter_id: str,
        permission_type: str,
        project_id: Optional[str] = None,
        group_name: Optional[str] = None,
        role_id: Optional[str] = None,
    ) -> FilterPermission:
        """
        添加过滤器共享权限

        POST /rest/api/2/filter/{id}/permission

        Args:
            filter_id: 过滤器ID
            permission_type: 权限类型（"group"、"project"、"projectRole"、"global"、"authenticated"）
            project_id: 项目ID（当type为"project"或"projectRole"时需要）
            group_name: 用户组名（当type为"group"时需要）
            role_id: 角色ID（当type为"projectRole"时需要）

        Returns:
            FilterPermission: 创建的权限
        """
        path = f"{self.BASE_PATH}/{filter_id}/permission"
        payload: dict[str, Any] = {"type": permission_type}

        if project_id:
            payload["projectId"] = project_id
        if group_name:
            payload["groupname"] = group_name
        if role_id:
            payload["roleId"] = role_id

        data = await self.client.post_json(path, data=payload)
        return FilterPermission.model_validate(data)

    async def add_permission_raw(
        self,
        filter_id: str,
        permission_type: str,
        project_id: Optional[str] = None,
        group_name: Optional[str] = None,
        role_id: Optional[str] = None,
    ) -> dict:
        """添加过滤器共享权限（原始JSON）"""
        path = f"{self.BASE_PATH}/{filter_id}/permission"
        payload: dict[str, Any] = {"type": permission_type}

        if project_id:
            payload["projectId"] = project_id
        if group_name:
            payload["groupname"] = group_name
        if role_id:
            payload["roleId"] = role_id

        return await self.client.post_json(path, data=payload)

    async def get_permission(
        self,
        filter_id: str,
        permission_id: str,
    ) -> FilterPermission:
        """
        获取单个过滤器权限详情

        GET /rest/api/2/filter/{id}/permission/{permissionId}

        Args:
            filter_id: 过滤器ID
            permission_id: 权限ID

        Returns:
            FilterPermission: 权限详情
        """
        path = f"{self.BASE_PATH}/{filter_id}/permission/{permission_id}"
        data = await self.client.get_json(path)
        return FilterPermission.model_validate(data)

    async def get_permission_raw(
        self,
        filter_id: str,
        permission_id: str,
    ) -> dict:
        """获取单个过滤器权限详情（原始JSON）"""
        path = f"{self.BASE_PATH}/{filter_id}/permission/{permission_id}"
        return await self.client.get_json(path)

    async def delete_permission(
        self,
        filter_id: str,
        permission_id: str,
    ) -> None:
        """
        删除过滤器共享权限

        DELETE /rest/api/2/filter/{id}/permission/{permissionId}

        Args:
            filter_id: 过滤器ID
            permission_id: 权限ID
        """
        path = f"{self.BASE_PATH}/{filter_id}/permission/{permission_id}"
        await self.client.delete(path)

    # ==================== Favourites ====================

    async def add_favourite(
        self,
        filter_id: str,
    ) -> Filter:
        """
        收藏过滤器

        PUT /rest/api/2/filter/{id}/favourite

        Args:
            filter_id: 过滤器ID

        Returns:
            Filter: 更新后的过滤器
        """
        path = f"{self.BASE_PATH}/{filter_id}/favourite"
        data = await self.client.put_json(path, data=None)
        return Filter.model_validate(data)

    async def add_favourite_raw(
        self,
        filter_id: str,
    ) -> dict:
        """收藏过滤器（原始JSON）"""
        path = f"{self.BASE_PATH}/{filter_id}/favourite"
        return await self.client.put_json(path, data=None)

    async def remove_favourite(
        self,
        filter_id: str,
    ) -> Filter:
        """
        取消收藏过滤器

        DELETE /rest/api/2/filter/{id}/favourite

        Args:
            filter_id: 过滤器ID

        Returns:
            Filter: 更新后的过滤器
        """
        path = f"{self.BASE_PATH}/{filter_id}/favourite"
        data = await self.client.delete(path)
        return Filter.model_validate(data)

    async def remove_favourite_raw(
        self,
        filter_id: str,
    ) -> dict:
        """取消收藏过滤器（原始JSON）"""
        path = f"{self.BASE_PATH}/{filter_id}/favourite"
        return await self.client.delete(path)
