"""
User Resource - 用户资源

GET    /rest/api/2/user                          - 获取用户
POST   /rest/api/2/user                          - 创建用户
PUT    /rest/api/2/user                          - 更新用户
DELETE /rest/api/2/user                          - 删除用户
GET    /rest/api/2/user/search                   - 搜索用户
GET    /rest/api/2/user/assignable/search        - 搜索可分配用户
GET    /rest/api/2/user/assignable/multiProjectSearch - 搜索多项目可分配用户
GET    /rest/api/2/user/picker                   - 用户选择器
GET    /rest/api/2/user/viewissue/search         - 搜索可查看Issue的用户
GET    /rest/api/2/user/permission/search        - 搜索有权限的用户
GET    /rest/api/2/user/bulk                     - 批量获取用户
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.user import User, UserDetails
from atlassian.jira.models.common import EntityProperty, EntityPropertyKeys


class UserResource(BaseResource):
    """
    用户资源

    API: /rest/api/2/user
    """

    BASE_PATH = "/rest/api/2/user"

    # ==================== User CRUD ====================

    async def get(
        self,
        username: Optional[str] = None,
        key: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> User:
        """
        获取用户信息

        GET /rest/api/2/user

        Args:
            username: 用户名（可选，username和key至少提供一个）
            key: 用户key（可选）
            expand: 扩展字段（可选，如"groups,applicationRoles"）

        Returns:
            User: 用户信息
        """
        params: dict[str, Any] = {}
        if username:
            params["username"] = username
        if key:
            params["key"] = key
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(self.BASE_PATH, params=params)
        return User.model_validate(data)

    async def get_raw(
        self,
        username: Optional[str] = None,
        key: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """获取用户信息（原始JSON）"""
        params: dict[str, Any] = {}
        if username:
            params["username"] = username
        if key:
            params["key"] = key
        if expand:
            params["expand"] = expand

        return await self.client.get_json(self.BASE_PATH, params=params)

    async def create(
        self,
        name: str,
        email: str,
        display_name: str,
        password: Optional[str] = None,
        notification: bool = False,
        application_keys: Optional[list[str]] = None,
    ) -> User:
        """
        创建用户

        POST /rest/api/2/user

        Args:
            name: 用户名
            email: 邮箱地址
            display_name: 显示名称
            password: 密码（可选）
            notification: 是否发送通知邮件（默认False）
            application_keys: 应用权限列表（可选）

        Returns:
            User: 创建的用户
        """
        payload: dict[str, Any] = {
            "name": name,
            "emailAddress": email,
            "displayName": display_name,
            "notification": notification,
        }
        if password:
            payload["password"] = password
        if application_keys:
            payload["applicationKeys"] = application_keys

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return User.model_validate(data)

    async def create_raw(
        self,
        name: str,
        email: str,
        display_name: str,
        password: Optional[str] = None,
        notification: bool = False,
        application_keys: Optional[list[str]] = None,
    ) -> dict:
        """创建用户（原始JSON）"""
        payload: dict[str, Any] = {
            "name": name,
            "emailAddress": email,
            "displayName": display_name,
            "notification": notification,
        }
        if password:
            payload["password"] = password
        if application_keys:
            payload["applicationKeys"] = application_keys

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def update(
        self,
        username: str,
        email: Optional[str] = None,
        display_name: Optional[str] = None,
        active: Optional[bool] = None,
        application_keys: Optional[list[str]] = None,
    ) -> User:
        """
        更新用户

        PUT /rest/api/2/user

        Args:
            username: 用户名
            email: 邮箱地址（可选）
            display_name: 显示名称（可选）
            active: 是否激活（可选）
            application_keys: 应用权限列表（可选）

        Returns:
            User: 更新后的用户
        """
        params = {"username": username}
        payload: dict[str, Any] = {}
        if email:
            payload["emailAddress"] = email
        if display_name:
            payload["displayName"] = display_name
        if active is not None:
            payload["active"] = active
        if application_keys:
            payload["applicationKeys"] = application_keys

        data = await self.client.put_json(self.BASE_PATH, params=params, data=payload)
        return User.model_validate(data)

    async def update_raw(
        self,
        username: str,
        email: Optional[str] = None,
        display_name: Optional[str] = None,
        active: Optional[bool] = None,
        application_keys: Optional[list[str]] = None,
    ) -> dict:
        """更新用户（原始JSON）"""
        params = {"username": username}
        payload: dict[str, Any] = {}
        if email:
            payload["emailAddress"] = email
        if display_name:
            payload["displayName"] = display_name
        if active is not None:
            payload["active"] = active
        if application_keys:
            payload["applicationKeys"] = application_keys

        return await self.client.put_json(self.BASE_PATH, params=params, data=payload)

    async def delete(
        self,
        username: str,
    ) -> None:
        """
        删除用户

        DELETE /rest/api/2/user

        Args:
            username: 用户名
        """
        params = {"username": username}
        await self.client.delete(self.BASE_PATH, params=params)

    # ==================== User Search ====================

    async def search(
        self,
        username: Optional[str] = None,
        start_at: int = 0,
        max_results: int = 50,
        include_active: bool = True,
        include_inactive: bool = False,
    ) -> list[User]:
        """
        搜索用户

        GET /rest/api/2/user/search

        Args:
            username: 用户名关键字（可选）
            start_at: 起始位置
            max_results: 最大结果数
            include_active: 包含激活用户（默认True）
            include_inactive: 包含禁用用户（默认False）

        Returns:
            list[User]: 用户列表
        """
        path = f"{self.BASE_PATH}/search"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
            "includeActive": str(include_active).lower(),
            "includeInactive": str(include_inactive).lower(),
        }
        if username:
            params["username"] = username

        data = await self.client.get_json(path, params=params)
        return [User.model_validate(u) for u in data]

    async def search_raw(
        self,
        username: Optional[str] = None,
        start_at: int = 0,
        max_results: int = 50,
        include_active: bool = True,
        include_inactive: bool = False,
    ) -> list[dict]:
        """搜索用户（原始JSON）"""
        path = f"{self.BASE_PATH}/search"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
            "includeActive": str(include_active).lower(),
            "includeInactive": str(include_inactive).lower(),
        }
        if username:
            params["username"] = username

        return await self.client.get_json(path, params=params)

    async def search_assignable(
        self,
        username: Optional[str] = None,
        project: Optional[str] = None,
        issue_key: Optional[str] = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> list[User]:
        """
        搜索可分配给Issue的用户

        GET /rest/api/2/user/assignable/search

        Args:
            username: 用户名关键字（可选）
            project: 项目Key（可选，project和issue_key至少提供一个）
            issue_key: Issue Key（可选）
            start_at: 起始位置
            max_results: 最大结果数

        Returns:
            list[User]: 用户列表
        """
        path = f"{self.BASE_PATH}/assignable/search"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if username:
            params["username"] = username
        if project:
            params["project"] = project
        if issue_key:
            params["issueKey"] = issue_key

        data = await self.client.get_json(path, params=params)
        return [User.model_validate(u) for u in data]

    async def search_assignable_raw(
        self,
        username: Optional[str] = None,
        project: Optional[str] = None,
        issue_key: Optional[str] = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> list[dict]:
        """搜索可分配给Issue的用户（原始JSON）"""
        path = f"{self.BASE_PATH}/assignable/search"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if username:
            params["username"] = username
        if project:
            params["project"] = project
        if issue_key:
            params["issueKey"] = issue_key

        return await self.client.get_json(path, params=params)

    async def search_assignable_multiproject(
        self,
        project_keys: list[str],
        username: Optional[str] = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> list[User]:
        """
        搜索多项目可分配用户

        GET /rest/api/2/user/assignable/multiProjectSearch

        Args:
            project_keys: 项目Key列表
            username: 用户名关键字（可选）
            start_at: 起始位置
            max_results: 最大结果数

        Returns:
            list[User]: 用户列表
        """
        path = f"{self.BASE_PATH}/assignable/multiProjectSearch"
        params: dict[str, Any] = {
            "projectKeys": ",".join(project_keys),
            "startAt": start_at,
            "maxResults": max_results,
        }
        if username:
            params["username"] = username

        data = await self.client.get_json(path, params=params)
        return [User.model_validate(u) for u in data]

    async def search_assignable_multiproject_raw(
        self,
        project_keys: list[str],
        username: Optional[str] = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> list[dict]:
        """搜索多项目可分配用户（原始JSON）"""
        path = f"{self.BASE_PATH}/assignable/multiProjectSearch"
        params: dict[str, Any] = {
            "projectKeys": ",".join(project_keys),
            "startAt": start_at,
            "maxResults": max_results,
        }
        if username:
            params["username"] = username

        return await self.client.get_json(path, params=params)

    async def picker(
        self,
        query: str,
        max_results: int = 50,
        show_avatar: bool = False,
        exclude: Optional[list[str]] = None,
    ) -> dict:
        """
        用户选择器

        GET /rest/api/2/user/picker

        Args:
            query: 查询字符串
            max_results: 最大结果数
            show_avatar: 是否显示头像（默认False）
            exclude: 排除的用户名列表（可选）

        Returns:
            dict: 选择器结果
        """
        path = f"{self.BASE_PATH}/picker"
        params: dict[str, Any] = {
            "query": query,
            "maxResults": max_results,
            "showAvatar": str(show_avatar).lower(),
        }
        if exclude:
            params["exclude"] = ",".join(exclude)

        return await self.client.get_json(path, params=params)

    async def search_view_issue(
        self,
        username: Optional[str] = None,
        issue_key: Optional[str] = None,
        project_key: Optional[str] = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> list[User]:
        """
        搜索可查看Issue的用户

        GET /rest/api/2/user/viewissue/search

        Args:
            username: 用户名关键字（可选）
            issue_key: Issue Key（可选）
            project_key: 项目Key（可选）
            start_at: 起始位置
            max_results: 最大结果数

        Returns:
            list[User]: 用户列表
        """
        path = f"{self.BASE_PATH}/viewissue/search"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if username:
            params["username"] = username
        if issue_key:
            params["issueKey"] = issue_key
        if project_key:
            params["projectKey"] = project_key

        data = await self.client.get_json(path, params=params)
        return [User.model_validate(u) for u in data]

    async def search_view_issue_raw(
        self,
        username: Optional[str] = None,
        issue_key: Optional[str] = None,
        project_key: Optional[str] = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> list[dict]:
        """搜索可查看Issue的用户（原始JSON）"""
        path = f"{self.BASE_PATH}/viewissue/search"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if username:
            params["username"] = username
        if issue_key:
            params["issueKey"] = issue_key
        if project_key:
            params["projectKey"] = project_key

        return await self.client.get_json(path, params=params)

    async def search_permission(
        self,
        permissions: str,
        username: Optional[str] = None,
        issue_key: Optional[str] = None,
        project_key: Optional[str] = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> list[User]:
        """
        搜索有特定权限的用户

        GET /rest/api/2/user/permission/search

        Args:
            permissions: 权限名称（必填）
            username: 用户名关键字（可选）
            issue_key: Issue Key（可选）
            project_key: 项目Key（可选）
            start_at: 起始位置
            max_results: 最大结果数

        Returns:
            list[User]: 用户列表
        """
        path = f"{self.BASE_PATH}/permission/search"
        params: dict[str, Any] = {
            "permissions": permissions,
            "startAt": start_at,
            "maxResults": max_results,
        }
        if username:
            params["username"] = username
        if issue_key:
            params["issueKey"] = issue_key
        if project_key:
            params["projectKey"] = project_key

        data = await self.client.get_json(path, params=params)
        return [User.model_validate(u) for u in data]

    async def search_permission_raw(
        self,
        permissions: str,
        username: Optional[str] = None,
        issue_key: Optional[str] = None,
        project_key: Optional[str] = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> list[dict]:
        """搜索有特定权限的用户（原始JSON）"""
        path = f"{self.BASE_PATH}/permission/search"
        params: dict[str, Any] = {
            "permissions": permissions,
            "startAt": start_at,
            "maxResults": max_results,
        }
        if username:
            params["username"] = username
        if issue_key:
            params["issueKey"] = issue_key
        if project_key:
            params["projectKey"] = project_key

        return await self.client.get_json(path, params=params)

    async def bulk_get(
        self,
        usernames: Optional[list[str]] = None,
        keys: Optional[list[str]] = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> list[User]:
        """
        批量获取用户

        GET /rest/api/2/user/bulk

        Args:
            usernames: 用户名列表（可选，与keys至少提供一个）
            keys: 用户key列表（可选）
            start_at: 起始位置
            max_results: 最大结果数

        Returns:
            list[User]: 用户列表
        """
        path = f"{self.BASE_PATH}/bulk"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if usernames:
            params["username"] = ",".join(usernames)
        if keys:
            params["key"] = ",".join(keys)

        data = await self.client.get_json(path, params=params)
        return [User.model_validate(u) for u in data]

    async def bulk_get_raw(
        self,
        usernames: Optional[list[str]] = None,
        keys: Optional[list[str]] = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> list[dict]:
        """批量获取用户（原始JSON）"""
        path = f"{self.BASE_PATH}/bulk"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if usernames:
            params["username"] = ",".join(usernames)
        if keys:
            params["key"] = ",".join(keys)

        return await self.client.get_json(path, params=params)

    # ==================== Avatar Management ====================

    async def get_avatars(
        self,
        username: str,
    ) -> dict:
        """
        获取用户所有可用头像

        GET /rest/api/2/user/avatars

        Args:
            username: 用户名

        Returns:
            dict: 头像列表（包含system和custom）
        """
        path = f"{self.BASE_PATH}/avatars"
        params = {"username": username}
        return await self.client.get_json(path, params=params)

    async def create_avatar_from_temporary(
        self,
        username: str,
        crop_info: dict,
    ) -> dict:
        """
        从临时头像创建用户头像

        POST /rest/api/2/user/avatar

        Args:
            username: 用户名
            crop_info: 裁剪信息

        Returns:
            dict: 创建结果
        """
        path = f"{self.BASE_PATH}/avatar"
        params = {"username": username}
        return await self.client.post_json(path, params=params, data=crop_info)

    async def upload_avatar(
        self,
        username: str,
        file_path: str,
        filename: Optional[str] = None,
    ) -> dict:
        """
        上传用户头像

        POST /rest/api/2/user/avatar/temporary

        Args:
            username: 用户名
            file_path: 图片文件路径
            filename: 文件名（可选）

        Returns:
            dict: 上传结果（包含裁剪信息）
        """
        from pathlib import Path

        path = f"{self.BASE_PATH}/avatar/temporary"
        params = {"username": username}
        file_path_obj = Path(file_path)

        if filename is None:
            filename = file_path_obj.name

        with open(file_path_obj, "rb") as f:
            files = {"file": (filename, f)}
            headers = {"X-Atlassian-Token": "no-check"}
            auth_headers = self.client._get_auth_headers()
            auth_headers.pop("Content-Type", None)
            headers.update(auth_headers)

            # 构建完整URL
            full_url = f"{self.client.base_url}{path}"
            response = await self.client._get_client().post(
                full_url,
                params=params,
                files=files,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

    async def crop_avatar(
        self,
        username: str,
        crop_info: dict,
    ) -> dict:
        """
        裁剪临时头像

        POST /rest/api/2/user/avatar/temporary/crop

        Args:
            username: 用户名
            crop_info: 裁剪信息（cropX, cropY, cropWidth, cropHeight）

        Returns:
            dict: 裁剪结果
        """
        path = f"{self.BASE_PATH}/avatar/temporary/crop"
        params = {"username": username}
        return await self.client.post_json(path, params=params, data=crop_info)

    async def update_avatar(
        self,
        username: str,
        avatar_id: str,
    ) -> dict:
        """
        设置用户头像

        PUT /rest/api/2/user/avatar

        Args:
            username: 用户名
            avatar_id: 头像ID

        Returns:
            dict: 操作结果
        """
        path = f"{self.BASE_PATH}/avatar"
        params = {"username": username}
        payload = {"id": avatar_id}
        return await self.client.put_json(path, params=params, data=payload)

    async def delete_avatar(
        self,
        username: str,
        avatar_id: str,
    ) -> None:
        """
        删除用户头像

        DELETE /rest/api/2/user/avatar/{id}

        Args:
            username: 用户名
            avatar_id: 头像ID
        """
        path = f"{self.BASE_PATH}/avatar/{avatar_id}"
        params = {"username": username}
        await self.client.delete(path, params=params)

    async def get_default_columns(
        self,
        username: Optional[str] = None,
    ) -> list[dict]:
        """
        获取用户默认列

        GET /rest/api/2/user/columns

        Args:
            username: 用户名（可选）

        Returns:
            list[dict]: 列定义列表
        """
        path = f"{self.BASE_PATH}/columns"
        params = {}
        if username:
            params["username"] = username

        return await self.client.get_json(path, params=params)

    async def set_default_columns(
        self,
        columns: list[str],
        username: Optional[str] = None,
    ) -> dict:
        """
        设置用户默认列

        PUT /rest/api/2/user/columns

        Args:
            columns: 列名列表
            username: 用户名（可选）

        Returns:
            dict: 操作结果
        """
        path = f"{self.BASE_PATH}/columns"
        params = {}
        if username:
            params["username"] = username

        return await self.client.put_json(path, params=params, data=columns)

    async def reset_default_columns(
        self,
        username: Optional[str] = None,
    ) -> None:
        """
        重置用户默认列

        DELETE /rest/api/2/user/columns

        Args:
            username: 用户名（可选）
        """
        path = f"{self.BASE_PATH}/columns"
        params = {}
        if username:
            params["username"] = username

        await self.client.delete(path, params=params)

    # ==================== Properties ====================

    async def get_property_keys(
        self,
        username: Optional[str] = None,
        user_key: Optional[str] = None,
    ) -> EntityPropertyKeys:
        """
        获取用户属性键列表

        GET /rest/api/2/user/properties

        Args:
            username: 用户名（可选，username和user_key至少提供一个）
            user_key: 用户key（可选）

        Returns:
            EntityPropertyKeys: 属性键列表
        """
        path = f"{self.BASE_PATH}/properties"
        params: dict[str, Any] = {}
        if username:
            params["username"] = username
        if user_key:
            params["userKey"] = user_key

        data = await self.client.get_json(path, params=params)
        return EntityPropertyKeys.model_validate(data)

    async def get_property_keys_raw(
        self,
        username: Optional[str] = None,
        user_key: Optional[str] = None,
    ) -> dict:
        """获取用户属性键列表（原始JSON）"""
        path = f"{self.BASE_PATH}/properties"
        params: dict[str, Any] = {}
        if username:
            params["username"] = username
        if user_key:
            params["userKey"] = user_key

        return await self.client.get_json(path, params=params)

    async def get_property(
        self,
        property_key: str,
        username: Optional[str] = None,
        user_key: Optional[str] = None,
    ) -> EntityProperty:
        """
        获取用户属性

        GET /rest/api/2/user/properties/{propertyKey}

        Args:
            property_key: 属性键
            username: 用户名（可选，username和user_key至少提供一个）
            user_key: 用户key（可选）

        Returns:
            EntityProperty: 属性详情
        """
        path = f"{self.BASE_PATH}/properties/{property_key}"
        params: dict[str, Any] = {}
        if username:
            params["username"] = username
        if user_key:
            params["userKey"] = user_key

        data = await self.client.get_json(path, params=params)
        return EntityProperty.model_validate(data)

    async def get_property_raw(
        self,
        property_key: str,
        username: Optional[str] = None,
        user_key: Optional[str] = None,
    ) -> dict:
        """获取用户属性（原始JSON）"""
        path = f"{self.BASE_PATH}/properties/{property_key}"
        params: dict[str, Any] = {}
        if username:
            params["username"] = username
        if user_key:
            params["userKey"] = user_key

        return await self.client.get_json(path, params=params)

    async def set_property(
        self,
        property_key: str,
        value: Any,
        username: Optional[str] = None,
        user_key: Optional[str] = None,
    ) -> None:
        """
        设置用户属性

        PUT /rest/api/2/user/properties/{propertyKey}

        Args:
            property_key: 属性键
            value: 属性值
            username: 用户名（可选，username和user_key至少提供一个）
            user_key: 用户key（可选）
        """
        path = f"{self.BASE_PATH}/properties/{property_key}"
        params: dict[str, Any] = {}
        if username:
            params["username"] = username
        if user_key:
            params["userKey"] = user_key

        await self.client.put_json(path, params=params, data=value)

    async def delete_property(
        self,
        property_key: str,
        username: Optional[str] = None,
        user_key: Optional[str] = None,
    ) -> None:
        """
        删除用户属性

        DELETE /rest/api/2/user/properties/{propertyKey}

        Args:
            property_key: 属性键
            username: 用户名（可选，username和user_key至少提供一个）
            user_key: 用户key（可选）
        """
        path = f"{self.BASE_PATH}/properties/{property_key}"
        params: dict[str, Any] = {}
        if username:
            params["username"] = username
        if user_key:
            params["userKey"] = user_key

        await self.client.delete(path, params=params)

    # ==================== Application Management ====================

    async def remove_from_application(
        self,
        username: str,
        application_key: str,
    ) -> User:
        """
        将用户从应用中移除

        DELETE /rest/api/2/user/application

        Args:
            username: 用户名
            application_key: 应用key

        Returns:
            User: 更新后的用户
        """
        path = f"{self.BASE_PATH}/application"
        params = {
            "username": username,
            "applicationKey": application_key,
        }
        data = await self.client.delete(path, params=params)
        return User.model_validate(data)

    async def remove_from_application_raw(
        self,
        username: str,
        application_key: str,
    ) -> dict:
        """将用户从应用中移除（原始JSON）"""
        path = f"{self.BASE_PATH}/application"
        params = {
            "username": username,
            "applicationKey": application_key,
        }
        return await self.client.delete(path, params=params)

    # ==================== Anonymization ====================

    async def anonymize(
        self,
        username: Optional[str] = None,
        user_key: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """
        匿名化用户（GDPR）

        GET /rest/api/2/user/anonymization

        Args:
            username: 用户名（可选，username和user_key至少提供一个）
            user_key: 用户key（可选）
            expand: 扩展字段（可选）

        Returns:
            dict: 匿名化信息
        """
        path = f"{self.BASE_PATH}/anonymization"
        params: dict[str, Any] = {}
        if username:
            params["username"] = username
        if user_key:
            params["userKey"] = user_key
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    async def progress_anonymization(
        self,
        task_id: str,
    ) -> dict:
        """
        获取匿名化进度

        GET /rest/api/2/user/anonymization/progress

        Args:
            task_id: 任务ID

        Returns:
            dict: 进度信息
        """
        path = f"{self.BASE_PATH}/anonymization/progress"
        params = {"taskId": task_id}
        return await self.client.get_json(path, params=params)

    async def validate_anonymize(
        self,
        username: Optional[str] = None,
        user_key: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """
        验证用户匿名化

        POST /rest/api/2/user/anonymization/validate

        Args:
            username: 用户名（可选，username和user_key至少提供一个）
            user_key: 用户key（可选）
            expand: 扩展字段（可选）

        Returns:
            dict: 验证结果
        """
        path = f"{self.BASE_PATH}/anonymization/validate"
        params: dict[str, Any] = {}
        if username:
            params["username"] = username
        if user_key:
            params["userKey"] = user_key
        if expand:
            params["expand"] = expand

        return await self.client.post_json(path, params=params, data=None)

    async def reanonymize(
        self,
        username: Optional[str] = None,
        user_key: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """
        重新匿名化用户

        POST /rest/api/2/user/anonymization/re-anonymize

        Args:
            username: 用户名（可选，username和user_key至少提供一个）
            user_key: 用户key（可选）
            expand: 扩展字段（可选）

        Returns:
            dict: 匿名化任务信息
        """
        path = f"{self.BASE_PATH}/anonymization/re-anonymize"
        params: dict[str, Any] = {}
        if username:
            params["username"] = username
        if user_key:
            params["userKey"] = user_key
        if expand:
            params["expand"] = expand

        return await self.client.post_json(path, params=params, data=None)

    async def execute_anonymize(
        self,
        username: Optional[str] = None,
        user_key: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """
        执行用户匿名化

        POST /rest/api/2/user/anonymization

        Args:
            username: 用户名（可选，username和user_key至少提供一个）
            user_key: 用户key（可选）
            expand: 扩展字段（可选）

        Returns:
            dict: 匿名化任务信息
        """
        path = f"{self.BASE_PATH}/anonymization"
        params: dict[str, Any] = {}
        if username:
            params["username"] = username
        if user_key:
            params["userKey"] = user_key
        if expand:
            params["expand"] = expand

        return await self.client.post_json(path, params=params, data=None)

    async def cancel_anonymize(
        self,
        task_id: str,
    ) -> None:
        """
        取消匿名化任务

        DELETE /rest/api/2/user/anonymization

        Args:
            task_id: 任务ID
        """
        path = f"{self.BASE_PATH}/anonymization"
        params = {"taskId": task_id}
        await self.client.delete(path, params=params)
