"""
Issue Type Scheme Resource - Issue类型方案资源

Scheme CRUD:
GET    /rest/api/2/issuetypescheme                        - 获取所有Issue类型方案
POST   /rest/api/2/issuetypescheme                        - 创建Issue类型方案
GET    /rest/api/2/issuetypescheme/{issueTypeSchemeId}    - 获取Issue类型方案
PUT    /rest/api/2/issuetypescheme/{issueTypeSchemeId}    - 更新Issue类型方案
DELETE /rest/api/2/issuetypescheme/{issueTypeSchemeId}    - 删除Issue类型方案

Project Associations:
PUT    /rest/api/2/issuetypescheme/project                - 分配方案到项目
GET    /rest/api/2/issuetypescheme/project                - 获取方案关联的项目
DELETE /rest/api/2/issuetypescheme/project                - 从项目移除方案
GET    /rest/api/2/issuetypescheme/project/paginated      - 分页获取项目方案关联
GET    /rest/api/2/issuetypescheme/mapping                - 获取Issue类型方案映射
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.issue_type import (
    IssueTypeScheme,
    IssueTypeSchemeProjects,
    IssueTypeSchemeMapping,
)


class IssueTypeSchemeResource(BaseResource):
    """
    Issue类型方案资源

    API: /rest/api/2/issuetypescheme
    """

    BASE_PATH = "/rest/api/2/issuetypescheme"

    # ==================== Scheme CRUD ====================

    async def get_all(
        self,
        start_at: int = 0,
        max_results: int = 50,
        issue_type_scheme_id: Optional[list[int]] = None,
    ) -> dict:
        """
        获取所有Issue类型方案

        GET /rest/api/2/issuetypescheme

        Args:
            start_at: 起始位置（默认0）
            max_results: 最大结果数（默认50）
            issue_type_scheme_id: Issue类型方案ID列表（可选）

        Returns:
            dict: 包含分页信息和方案列表
        """
        params = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if issue_type_scheme_id:
            params["id"] = issue_type_scheme_id

        return await self.client.get_json(self.BASE_PATH, params=params)

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        default_issue_type_id: Optional[str] = None,
        issue_type_ids: Optional[list[str]] = None,
    ) -> IssueTypeScheme:
        """
        创建Issue类型方案

        POST /rest/api/2/issuetypescheme

        Args:
            name: 方案名称
            description: 方案描述（可选）
            default_issue_type_id: 默认Issue类型ID（可选）
            issue_type_ids: Issue类型ID列表（可选）

        Returns:
            IssueTypeScheme: 创建的方案
        """
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        if default_issue_type_id:
            payload["defaultIssueTypeId"] = default_issue_type_id
        if issue_type_ids:
            payload["issueTypeIds"] = issue_type_ids

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return IssueTypeScheme.model_validate(data)

    async def create_raw(
        self,
        name: str,
        description: Optional[str] = None,
        default_issue_type_id: Optional[str] = None,
        issue_type_ids: Optional[list[str]] = None,
    ) -> dict:
        """创建Issue类型方案（原始JSON）"""
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        if default_issue_type_id:
            payload["defaultIssueTypeId"] = default_issue_type_id
        if issue_type_ids:
            payload["issueTypeIds"] = issue_type_ids

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def get(
        self,
        issue_type_scheme_id: str,
    ) -> IssueTypeScheme:
        """
        获取Issue类型方案详情

        GET /rest/api/2/issuetypescheme/{issueTypeSchemeId}

        Args:
            issue_type_scheme_id: Issue类型方案ID

        Returns:
            IssueTypeScheme: 方案详情
        """
        path = f"{self.BASE_PATH}/{issue_type_scheme_id}"
        data = await self.client.get_json(path)
        return IssueTypeScheme.model_validate(data)

    async def get_raw(
        self,
        issue_type_scheme_id: str,
    ) -> dict:
        """获取Issue类型方案详情（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_type_scheme_id}"
        return await self.client.get_json(path)

    async def update(
        self,
        issue_type_scheme_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        default_issue_type_id: Optional[str] = None,
    ) -> dict:
        """
        更新Issue类型方案

        PUT /rest/api/2/issuetypescheme/{issueTypeSchemeId}

        Args:
            issue_type_scheme_id: Issue类型方案ID
            name: 方案名称（可选）
            description: 方案描述（可选）
            default_issue_type_id: 默认Issue类型ID（可选）

        Returns:
            dict: 操作结果
        """
        path = f"{self.BASE_PATH}/{issue_type_scheme_id}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if default_issue_type_id:
            payload["defaultIssueTypeId"] = default_issue_type_id

        return await self.client.put_json(path, data=payload)

    async def delete(
        self,
        issue_type_scheme_id: str,
    ) -> dict:
        """
        删除Issue类型方案

        DELETE /rest/api/2/issuetypescheme/{issueTypeSchemeId}

        Args:
            issue_type_scheme_id: Issue类型方案ID

        Returns:
            dict: 操作结果
        """
        path = f"{self.BASE_PATH}/{issue_type_scheme_id}"
        return await self.client.delete(path)

    # ==================== Project Associations ====================

    async def assign_to_project(
        self,
        issue_type_scheme_id: str,
        project_id: str,
    ) -> dict:
        """
        分配Issue类型方案到项目

        PUT /rest/api/2/issuetypescheme/project

        Args:
            issue_type_scheme_id: Issue类型方案ID
            project_id: 项目ID

        Returns:
            dict: 操作结果
        """
        path = f"{self.BASE_PATH}/project"
        payload = {
            "issueTypeSchemeId": issue_type_scheme_id,
            "projectId": project_id,
        }

        return await self.client.put_json(path, data=payload)

    async def get_projects(
        self,
        project_id: list[int],
        start_at: int = 0,
        max_results: int = 50,
    ) -> list[IssueTypeSchemeProjects]:
        """
        获取Issue类型方案关联的项目

        GET /rest/api/2/issuetypescheme/project

        Args:
            project_id: 项目ID列表
            start_at: 起始位置（默认0）
            max_results: 最大结果数（默认50）

        Returns:
            list[IssueTypeSchemeProjects]: 方案-项目关联列表
        """
        path = f"{self.BASE_PATH}/project"
        params = {
            "projectId": project_id,
            "startAt": start_at,
            "maxResults": max_results,
        }

        data = await self.client.get_json(path, params=params)
        values = data.get("values", [])
        return [IssueTypeSchemeProjects.model_validate(v) for v in values]

    async def get_projects_raw(
        self,
        project_id: list[int],
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict:
        """获取Issue类型方案关联的项目（原始JSON）"""
        path = f"{self.BASE_PATH}/project"
        params = {
            "projectId": project_id,
            "startAt": start_at,
            "maxResults": max_results,
        }

        return await self.client.get_json(path, params=params)

    async def remove_from_project(
        self,
        project_id: str,
    ) -> dict:
        """
        从项目移除Issue类型方案

        DELETE /rest/api/2/issuetypescheme/project

        Args:
            project_id: 项目ID

        Returns:
            dict: 操作结果
        """
        path = f"{self.BASE_PATH}/project"
        params = {"projectId": project_id}

        return await self.client.delete(path, params=params)

    async def get_projects_paginated(
        self,
        start_at: int = 0,
        max_results: int = 50,
        issue_type_scheme_id: Optional[list[int]] = None,
    ) -> dict:
        """
        分页获取项目Issue类型方案关联

        GET /rest/api/2/issuetypescheme/project/paginated

        Args:
            start_at: 起始位置（默认0）
            max_results: 最大结果数（默认50）
            issue_type_scheme_id: Issue类型方案ID列表（可选）

        Returns:
            dict: 包含分页信息和关联列表
        """
        path = f"{self.BASE_PATH}/project/paginated"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if issue_type_scheme_id:
            params["issueTypeSchemeId"] = issue_type_scheme_id

        return await self.client.get_json(path, params=params)

    async def get_mappings(
        self,
        start_at: int = 0,
        max_results: int = 50,
        issue_type_scheme_id: Optional[list[int]] = None,
    ) -> list[IssueTypeSchemeMapping]:
        """
        获取Issue类型方案映射

        GET /rest/api/2/issuetypescheme/mapping

        Args:
            start_at: 起始位置（默认0）
            max_results: 最大结果数（默认50）
            issue_type_scheme_id: Issue类型方案ID列表（可选）

        Returns:
            list[IssueTypeSchemeMapping]: 映射列表
        """
        path = f"{self.BASE_PATH}/mapping"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if issue_type_scheme_id:
            params["issueTypeSchemeId"] = issue_type_scheme_id

        data = await self.client.get_json(path, params=params)
        values = data.get("values", [])
        return [IssueTypeSchemeMapping.model_validate(v) for v in values]

    async def get_mappings_raw(
        self,
        start_at: int = 0,
        max_results: int = 50,
        issue_type_scheme_id: Optional[list[int]] = None,
    ) -> dict:
        """获取Issue类型方案映射（原始JSON）"""
        path = f"{self.BASE_PATH}/mapping"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if issue_type_scheme_id:
            params["issueTypeSchemeId"] = issue_type_scheme_id

        return await self.client.get_json(path, params=params)
