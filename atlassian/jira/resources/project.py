"""
Project Resource - 项目 API

GET /rest/api/2/project                              - 获取所有项目
GET /rest/api/2/project/{projectIdOrKey}             - 获取项目详情
GET /rest/api/2/project/{projectIdOrKey}/components  - 获取项目组件
GET /rest/api/2/project/{projectIdOrKey}/versions    - 获取项目版本
GET /rest/api/2/project/{projectIdOrKey}/statuses    - 获取项目状态
"""

from typing import Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.project import (
    Project,
    ProjectComponent,
    ProjectVersion,
    ProjectStatus,
)


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
