"""
Project Resource - 项目 API

GET    /rest/api/2/project                              - 获取所有项目
POST   /rest/api/2/project                              - 创建项目
GET    /rest/api/2/project/{projectIdOrKey}             - 获取项目详情
PUT    /rest/api/2/project/{projectIdOrKey}             - 更新项目
DELETE /rest/api/2/project/{projectIdOrKey}             - 删除项目
GET    /rest/api/2/project/{projectIdOrKey}/components  - 获取项目组件
GET    /rest/api/2/project/{projectIdOrKey}/versions    - 获取项目版本
GET    /rest/api/2/project/{projectIdOrKey}/statuses    - 获取项目状态
GET    /rest/api/2/project/{projectIdOrKey}/role        - 获取项目角色
GET    /rest/api/2/project/{projectIdOrKey}/role/{id}   - 获取项目角色详情
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.project import (
    Project,
    ProjectComponent,
    ProjectVersion,
    ProjectStatus,
)
from atlassian.jira.models.common import EntityProperty, EntityPropertyKeys


class ProjectResource(BaseResource):
    """
    项目资源

    API: /rest/api/2/project
    """

    BASE_PATH = "/rest/api/2/project"

    async def get_all(
        self,
        expand: Optional[str] = None,
        recent: Optional[int] = None,
    ) -> list[Project]:
        """
        获取所有项目

        GET /rest/api/2/project

        Args:
            expand: 展开的字段（可选），如 "description,lead,url,projectKeys"
            recent: 最近访问的项目数量（可选）

        Returns:
            list[Project]: 项目列表
        """
        params = {}
        if expand:
            params["expand"] = expand
        if recent is not None:
            params["recent"] = recent

        data = await self.client.get_json(self.BASE_PATH, params=params)
        return [Project.model_validate(p) for p in data]

    async def get_all_raw(
        self,
        expand: Optional[str] = None,
        recent: Optional[int] = None,
    ) -> list[dict]:
        """
        获取所有项目（原始 JSON）

        Args:
            expand: 展开的字段（可选）
            recent: 最近访问的项目数量（可选）

        Returns:
            list[dict]: 原始 JSON 响应
        """
        params = {}
        if expand:
            params["expand"] = expand
        if recent is not None:
            params["recent"] = recent

        return await self.client.get_json(self.BASE_PATH, params=params)

    async def get(
        self,
        project_id_or_key: str,
        expand: Optional[str] = None,
    ) -> Project:
        """
        获取项目详情

        GET /rest/api/2/project/{projectIdOrKey}

        Args:
            project_id_or_key: 项目 ID 或 Key
            expand: 展开的字段（可选），如 "description,lead,url,projectKeys,issueTypes"

        Returns:
            Project: 项目信息
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}"
        params = {}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return Project.model_validate(data)

    async def get_raw(
        self,
        project_id_or_key: str,
        expand: Optional[str] = None,
    ) -> dict:
        """
        获取项目详情（原始 JSON）

        Args:
            project_id_or_key: 项目 ID 或 Key
            expand: 展开的字段（可选）

        Returns:
            dict: 原始 JSON 响应
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}"
        params = {}
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    async def get_components(self, project_id_or_key: str) -> list[ProjectComponent]:
        """
        获取项目组件

        GET /rest/api/2/project/{projectIdOrKey}/components

        Args:
            project_id_or_key: 项目 ID 或 Key

        Returns:
            list[ProjectComponent]: 组件列表
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/components"
        data = await self.client.get_json(path)
        return [ProjectComponent.model_validate(c) for c in data]

    async def get_components_raw(self, project_id_or_key: str) -> list[dict]:
        """
        获取项目组件（原始 JSON）

        Args:
            project_id_or_key: 项目 ID 或 Key

        Returns:
            list[dict]: 原始 JSON 响应
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/components"
        return await self.client.get_json(path)

    async def get_versions(self, project_id_or_key: str) -> list[ProjectVersion]:
        """
        获取项目版本

        GET /rest/api/2/project/{projectIdOrKey}/versions

        Args:
            project_id_or_key: 项目 ID 或 Key

        Returns:
            list[ProjectVersion]: 版本列表
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/versions"
        data = await self.client.get_json(path)
        return [ProjectVersion.model_validate(v) for v in data]

    async def get_versions_raw(self, project_id_or_key: str) -> list[dict]:
        """
        获取项目版本（原始 JSON）

        Args:
            project_id_or_key: 项目 ID 或 Key

        Returns:
            list[dict]: 原始 JSON 响应
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/versions"
        return await self.client.get_json(path)

    async def get_statuses(self, project_id_or_key: str) -> list[ProjectStatus]:
        """
        获取项目状态（按 issue type 分组）

        GET /rest/api/2/project/{projectIdOrKey}/statuses

        Args:
            project_id_or_key: 项目 ID 或 Key

        Returns:
            list[ProjectStatus]: 状态列表（每个 issue type 一组）
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/statuses"
        data = await self.client.get_json(path)
        return [ProjectStatus.model_validate(s) for s in data]

    async def get_statuses_raw(self, project_id_or_key: str) -> list[dict]:
        """
        获取项目状态（原始 JSON）

        Args:
            project_id_or_key: 项目 ID 或 Key

        Returns:
            list[dict]: 原始 JSON 响应
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/statuses"
        return await self.client.get_json(path)

    # ==================== Project CRUD ====================

    async def create(
        self,
        key: str,
        name: str,
        project_type_key: str,
        lead: str,
        description: Optional[str] = None,
        url: Optional[str] = None,
        assignee_type: Optional[str] = None,
        avatar_id: Optional[int] = None,
        issue_security_scheme: Optional[int] = None,
        permission_scheme: Optional[int] = None,
        notification_scheme: Optional[int] = None,
        category_id: Optional[int] = None,
    ) -> Project:
        """
        创建项目

        POST /rest/api/2/project

        Args:
            key: 项目Key（大写字母，3-10个字符）
            name: 项目名称
            project_type_key: 项目类型Key（如"software"、"business"）
            lead: 项目负责人用户名
            description: 项目描述（可选）
            url: 项目URL（可选）
            assignee_type: 默认经办人类型（可选）
            avatar_id: 头像ID（可选）
            issue_security_scheme: Issue安全方案ID（可选）
            permission_scheme: 权限方案ID（可选）
            notification_scheme: 通知方案ID（可选）
            category_id: 项目类别ID（可选）

        Returns:
            Project: 创建的项目
        """
        payload: dict[str, Any] = {
            "key": key,
            "name": name,
            "projectTypeKey": project_type_key,
            "lead": lead,
        }
        if description:
            payload["description"] = description
        if url:
            payload["url"] = url
        if assignee_type:
            payload["assigneeType"] = assignee_type
        if avatar_id:
            payload["avatarId"] = avatar_id
        if issue_security_scheme:
            payload["issueSecurityScheme"] = issue_security_scheme
        if permission_scheme:
            payload["permissionScheme"] = permission_scheme
        if notification_scheme:
            payload["notificationScheme"] = notification_scheme
        if category_id:
            payload["categoryId"] = category_id

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return Project.model_validate(data)

    async def create_raw(
        self,
        key: str,
        name: str,
        project_type_key: str,
        lead: str,
        description: Optional[str] = None,
        url: Optional[str] = None,
        assignee_type: Optional[str] = None,
        avatar_id: Optional[int] = None,
        issue_security_scheme: Optional[int] = None,
        permission_scheme: Optional[int] = None,
        notification_scheme: Optional[int] = None,
        category_id: Optional[int] = None,
    ) -> dict:
        """创建项目（原始JSON）"""
        payload: dict[str, Any] = {
            "key": key,
            "name": name,
            "projectTypeKey": project_type_key,
            "lead": lead,
        }
        if description:
            payload["description"] = description
        if url:
            payload["url"] = url
        if assignee_type:
            payload["assigneeType"] = assignee_type
        if avatar_id:
            payload["avatarId"] = avatar_id
        if issue_security_scheme:
            payload["issueSecurityScheme"] = issue_security_scheme
        if permission_scheme:
            payload["permissionScheme"] = permission_scheme
        if notification_scheme:
            payload["notificationScheme"] = notification_scheme
        if category_id:
            payload["categoryId"] = category_id

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def update(
        self,
        project_id_or_key: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        lead: Optional[str] = None,
        url: Optional[str] = None,
        assignee_type: Optional[str] = None,
        avatar_id: Optional[int] = None,
        category_id: Optional[int] = None,
    ) -> Project:
        """
        更新项目

        PUT /rest/api/2/project/{projectIdOrKey}

        Args:
            project_id_or_key: 项目ID或Key
            name: 项目名称（可选）
            description: 项目描述（可选）
            lead: 项目负责人用户名（可选）
            url: 项目URL（可选）
            assignee_type: 默认经办人类型（可选）
            avatar_id: 头像ID（可选）
            category_id: 项目类别ID（可选）

        Returns:
            Project: 更新后的项目
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if lead:
            payload["lead"] = lead
        if url:
            payload["url"] = url
        if assignee_type:
            payload["assigneeType"] = assignee_type
        if avatar_id:
            payload["avatarId"] = avatar_id
        if category_id:
            payload["categoryId"] = category_id

        data = await self.client.put_json(path, data=payload)
        return Project.model_validate(data)

    async def update_raw(
        self,
        project_id_or_key: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        lead: Optional[str] = None,
        url: Optional[str] = None,
        assignee_type: Optional[str] = None,
        avatar_id: Optional[int] = None,
        category_id: Optional[int] = None,
    ) -> dict:
        """更新项目（原始JSON）"""
        path = f"{self.BASE_PATH}/{project_id_or_key}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if lead:
            payload["lead"] = lead
        if url:
            payload["url"] = url
        if assignee_type:
            payload["assigneeType"] = assignee_type
        if avatar_id:
            payload["avatarId"] = avatar_id
        if category_id:
            payload["categoryId"] = category_id

        return await self.client.put_json(path, data=payload)

    async def delete(
        self,
        project_id_or_key: str,
    ) -> None:
        """
        删除项目

        DELETE /rest/api/2/project/{projectIdOrKey}

        Args:
            project_id_or_key: 项目ID或Key
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}"
        await self.client.delete(path)

    # ==================== Role Management ====================

    async def get_roles(
        self,
        project_id_or_key: str,
    ) -> dict:
        """
        获取项目角色列表

        GET /rest/api/2/project/{projectIdOrKey}/role

        Args:
            project_id_or_key: 项目ID或Key

        Returns:
            dict: 角色字典（角色名到角色URL的映射）
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/role"
        return await self.client.get_json(path)

    async def get_role(
        self,
        project_id_or_key: str,
        role_id: str,
    ) -> dict:
        """
        获取项目角色详情

        GET /rest/api/2/project/{projectIdOrKey}/role/{id}

        Args:
            project_id_or_key: 项目ID或Key
            role_id: 角色ID

        Returns:
            dict: 角色详情
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/role/{role_id}"
        return await self.client.get_json(path)

    async def set_role_actors(
        self,
        project_id_or_key: str,
        role_id: str,
        user: Optional[list[str]] = None,
        group: Optional[list[str]] = None,
    ) -> dict:
        """
        设置项目角色成员

        PUT /rest/api/2/project/{projectIdOrKey}/role/{id}

        Args:
            project_id_or_key: 项目ID或Key
            role_id: 角色ID
            user: 用户名列表（可选）
            group: 用户组名列表（可选）

        Returns:
            dict: 更新后的角色详情
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/role/{role_id}"
        payload: dict[str, Any] = {}
        if user:
            payload["user"] = user
        if group:
            payload["group"] = group

        return await self.client.put_json(path, data=payload)

    async def add_role_actors(
        self,
        project_id_or_key: str,
        role_id: str,
        user: Optional[list[str]] = None,
        group: Optional[list[str]] = None,
    ) -> dict:
        """
        添加项目角色成员

        POST /rest/api/2/project/{projectIdOrKey}/role/{id}

        Args:
            project_id_or_key: 项目ID或Key
            role_id: 角色ID
            user: 用户名列表（可选）
            group: 用户组名列表（可选）

        Returns:
            dict: 更新后的角色详情
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/role/{role_id}"
        payload: dict[str, Any] = {}
        if user:
            payload["user"] = user
        if group:
            payload["group"] = group

        return await self.client.post_json(path, data=payload)

    async def delete_role_actor(
        self,
        project_id_or_key: str,
        role_id: str,
        user: Optional[str] = None,
        group: Optional[str] = None,
    ) -> None:
        """
        删除项目角色成员

        DELETE /rest/api/2/project/{projectIdOrKey}/role/{id}

        Args:
            project_id_or_key: 项目ID或Key
            role_id: 角色ID
            user: 用户名（可选）
            group: 用户组名（可选）
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/role/{role_id}"
        params: dict[str, Any] = {}
        if user:
            params["user"] = user
        if group:
            params["group"] = group

        await self.client.delete(path, params=params)

    # ==================== Properties ====================

    async def get_property_keys(
        self,
        project_id_or_key: str,
    ) -> EntityPropertyKeys:
        """
        获取项目属性键列表

        GET /rest/api/2/project/{projectIdOrKey}/properties

        Args:
            project_id_or_key: 项目ID或Key

        Returns:
            EntityPropertyKeys: 属性键列表
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/properties"
        data = await self.client.get_json(path)
        return EntityPropertyKeys.model_validate(data)

    async def get_property_keys_raw(
        self,
        project_id_or_key: str,
    ) -> dict:
        """获取项目属性键列表（原始JSON）"""
        path = f"{self.BASE_PATH}/{project_id_or_key}/properties"
        return await self.client.get_json(path)

    async def get_property(
        self,
        project_id_or_key: str,
        property_key: str,
    ) -> EntityProperty:
        """
        获取项目属性

        GET /rest/api/2/project/{projectIdOrKey}/properties/{propertyKey}

        Args:
            project_id_or_key: 项目ID或Key
            property_key: 属性键

        Returns:
            EntityProperty: 属性详情
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/properties/{property_key}"
        data = await self.client.get_json(path)
        return EntityProperty.model_validate(data)

    async def get_property_raw(
        self,
        project_id_or_key: str,
        property_key: str,
    ) -> dict:
        """获取项目属性（原始JSON）"""
        path = f"{self.BASE_PATH}/{project_id_or_key}/properties/{property_key}"
        return await self.client.get_json(path)

    async def set_property(
        self,
        project_id_or_key: str,
        property_key: str,
        value: Any,
    ) -> None:
        """
        设置项目属性

        PUT /rest/api/2/project/{projectIdOrKey}/properties/{propertyKey}

        Args:
            project_id_or_key: 项目ID或Key
            property_key: 属性键
            value: 属性值
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/properties/{property_key}"
        await self.client.put_json(path, data=value)

    async def delete_property(
        self,
        project_id_or_key: str,
        property_key: str,
    ) -> None:
        """
        删除项目属性

        DELETE /rest/api/2/project/{projectIdOrKey}/properties/{propertyKey}

        Args:
            project_id_or_key: 项目ID或Key
            property_key: 属性键
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/properties/{property_key}"
        await self.client.delete(path)

    # ==================== Avatar Management ====================

    async def get_avatars(
        self,
        project_id_or_key: str,
    ) -> dict:
        """
        获取项目所有可用头像

        GET /rest/api/2/project/{projectIdOrKey}/avatars

        Args:
            project_id_or_key: 项目ID或Key

        Returns:
            dict: 头像列表（包含system和custom）
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/avatars"
        return await self.client.get_json(path)

    async def create_avatar(
        self,
        project_id_or_key: str,
        file_path: str,
        filename: Optional[str] = None,
    ) -> dict:
        """
        上传项目头像

        POST /rest/api/2/project/{projectIdOrKey}/avatar

        Args:
            project_id_or_key: 项目ID或Key
            file_path: 图片文件路径
            filename: 文件名（可选）

        Returns:
            dict: 上传结果
        """
        from pathlib import Path

        path = f"{self.BASE_PATH}/{project_id_or_key}/avatar"
        file_path_obj = Path(file_path)

        if filename is None:
            filename = file_path_obj.name

        with open(file_path_obj, "rb") as f:
            files = {"file": (filename, f)}
            headers = {"X-Atlassian-Token": "no-check"}
            auth_headers = self.client._get_auth_headers()
            auth_headers.pop("Content-Type", None)
            headers.update(auth_headers)

            response = await self.client._get_client().post(
                path,
                files=files,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

    async def update_avatar(
        self,
        project_id_or_key: str,
        avatar_id: str,
    ) -> dict:
        """
        设置项目头像

        PUT /rest/api/2/project/{projectIdOrKey}/avatar

        Args:
            project_id_or_key: 项目ID或Key
            avatar_id: 头像ID

        Returns:
            dict: 操作结果
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/avatar"
        payload = {"id": avatar_id}
        return await self.client.put_json(path, data=payload)

    async def delete_avatar(
        self,
        project_id_or_key: str,
        avatar_id: str,
    ) -> None:
        """
        删除项目头像

        DELETE /rest/api/2/project/{projectIdOrKey}/avatar/{id}

        Args:
            project_id_or_key: 项目ID或Key
            avatar_id: 头像ID
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/avatar/{avatar_id}"
        await self.client.delete(path)

    # ==================== Schemes ====================

    async def get_notification_scheme(
        self,
        project_id_or_key: str,
        expand: Optional[str] = None,
    ) -> dict:
        """
        获取项目通知方案

        GET /rest/api/2/project/{projectIdOrKey}/notificationscheme

        Args:
            project_id_or_key: 项目ID或Key
            expand: 扩展字段（可选）

        Returns:
            dict: 通知方案详情
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/notificationscheme"
        params = {}
        if expand:
            params["expand"] = expand
        return await self.client.get_json(path, params=params)

    async def get_permission_scheme(
        self,
        project_id_or_key: str,
        expand: Optional[str] = None,
    ) -> dict:
        """
        获取项目权限方案

        GET /rest/api/2/project/{projectIdOrKey}/permissionscheme

        Args:
            project_id_or_key: 项目ID或Key
            expand: 扩展字段（可选）

        Returns:
            dict: 权限方案详情
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/permissionscheme"
        params = {}
        if expand:
            params["expand"] = expand
        return await self.client.get_json(path, params=params)

    async def get_issue_security_scheme(
        self,
        project_id_or_key: str,
    ) -> dict:
        """
        获取项目Issue安全方案

        GET /rest/api/2/project/{projectIdOrKey}/issuesecuritylevelscheme

        Args:
            project_id_or_key: 项目ID或Key

        Returns:
            dict: Issue安全方案详情
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/issuesecuritylevelscheme"
        return await self.client.get_json(path)

    async def get_security_levels(
        self,
        project_id_or_key: str,
    ) -> dict:
        """
        获取项目安全级别

        GET /rest/api/2/project/{projectIdOrKey}/securitylevel

        Args:
            project_id_or_key: 项目ID或Key

        Returns:
            dict: 安全级别列表
        """
        path = f"{self.BASE_PATH}/{project_id_or_key}/securitylevel"
        return await self.client.get_json(path)
