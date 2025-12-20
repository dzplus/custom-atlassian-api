"""
Version Resource - 版本资源

POST   /rest/api/2/version                                    - 创建版本
GET    /rest/api/2/version/{id}                               - 获取版本
PUT    /rest/api/2/version/{id}                               - 更新版本
DELETE /rest/api/2/version/{id}                               - 删除版本
POST   /rest/api/2/version/{id}/move                          - 移动版本
POST   /rest/api/2/version/{id}/mergeto/{moveIssuesTo}       - 合并版本
POST   /rest/api/2/version/{id}/removeAndSwap                 - 删除并替换版本
GET    /rest/api/2/version/{id}/relatedIssueCounts           - 获取关联Issue数量
GET    /rest/api/2/version/{id}/unresolvedIssueCount         - 获取未解决Issue数量
GET    /rest/api/2/version/{versionId}/remotelink            - 获取远程链接列表
POST   /rest/api/2/version/{versionId}/remotelink            - 创建远程链接
DELETE /rest/api/2/version/{versionId}/remotelink            - 按全局ID删除远程链接
GET    /rest/api/2/version/{versionId}/remotelink/{globalId} - 获取远程链接
PUT    /rest/api/2/version/{versionId}/remotelink/{globalId} - 更新远程链接
DELETE /rest/api/2/version/{versionId}/remotelink/{globalId} - 删除远程链接
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.version import (
    Version,
    VersionRemoteLink,
    VersionIssueCounts,
    VersionUnresolvedIssueCount,
)


class VersionResource(BaseResource):
    """
    版本资源

    API: /rest/api/2/version
    """

    BASE_PATH = "/rest/api/2/version"

    async def create(
        self,
        name: str,
        project: str,
        description: Optional[str] = None,
        start_date: Optional[str] = None,
        release_date: Optional[str] = None,
        archived: bool = False,
        released: bool = False,
    ) -> Version:
        """
        创建版本

        POST /rest/api/2/version

        Args:
            name: 版本名称
            project: 项目Key或ID
            description: 版本描述（可选）
            start_date: 开始日期（格式：YYYY-MM-DD，可选）
            release_date: 发布日期（格式：YYYY-MM-DD，可选）
            archived: 是否归档（默认False）
            released: 是否已发布（默认False）

        Returns:
            Version: 创建的版本
        """
        payload: dict[str, Any] = {
            "name": name,
            "project": project,
            "archived": archived,
            "released": released,
        }
        if description:
            payload["description"] = description
        if start_date:
            payload["startDate"] = start_date
        if release_date:
            payload["releaseDate"] = release_date

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return Version.model_validate(data)

    async def create_raw(
        self,
        name: str,
        project: str,
        description: Optional[str] = None,
        start_date: Optional[str] = None,
        release_date: Optional[str] = None,
        archived: bool = False,
        released: bool = False,
    ) -> dict:
        """创建版本（原始JSON）"""
        payload: dict[str, Any] = {
            "name": name,
            "project": project,
            "archived": archived,
            "released": released,
        }
        if description:
            payload["description"] = description
        if start_date:
            payload["startDate"] = start_date
        if release_date:
            payload["releaseDate"] = release_date

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def get(
        self,
        version_id: str,
        expand: Optional[str] = None,
    ) -> Version:
        """
        获取版本详情

        GET /rest/api/2/version/{id}

        Args:
            version_id: 版本ID
            expand: 扩展字段（可选，如"operations"、"issuesStatusForFixVersion"）

        Returns:
            Version: 版本详情
        """
        path = f"{self.BASE_PATH}/{version_id}"
        params = {}
        if expand:
            params["expand"] = expand
        data = await self.client.get_json(path, params=params)
        return Version.model_validate(data)

    async def get_raw(
        self,
        version_id: str,
        expand: Optional[str] = None,
    ) -> dict:
        """获取版本详情（原始JSON）"""
        path = f"{self.BASE_PATH}/{version_id}"
        params = {}
        if expand:
            params["expand"] = expand
        return await self.client.get_json(path, params=params)

    async def update(
        self,
        version_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        start_date: Optional[str] = None,
        release_date: Optional[str] = None,
        archived: Optional[bool] = None,
        released: Optional[bool] = None,
    ) -> Version:
        """
        更新版本

        PUT /rest/api/2/version/{id}

        Args:
            version_id: 版本ID
            name: 版本名称（可选）
            description: 版本描述（可选）
            start_date: 开始日期（可选）
            release_date: 发布日期（可选）
            archived: 是否归档（可选）
            released: 是否已发布（可选）

        Returns:
            Version: 更新后的版本
        """
        path = f"{self.BASE_PATH}/{version_id}"
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if start_date is not None:
            payload["startDate"] = start_date
        if release_date is not None:
            payload["releaseDate"] = release_date
        if archived is not None:
            payload["archived"] = archived
        if released is not None:
            payload["released"] = released

        data = await self.client.put_json(path, data=payload)
        return Version.model_validate(data)

    async def update_raw(
        self,
        version_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        start_date: Optional[str] = None,
        release_date: Optional[str] = None,
        archived: Optional[bool] = None,
        released: Optional[bool] = None,
    ) -> dict:
        """更新版本（原始JSON）"""
        path = f"{self.BASE_PATH}/{version_id}"
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if start_date is not None:
            payload["startDate"] = start_date
        if release_date is not None:
            payload["releaseDate"] = release_date
        if archived is not None:
            payload["archived"] = archived
        if released is not None:
            payload["released"] = released

        return await self.client.put_json(path, data=payload)

    async def delete(
        self,
        version_id: str,
        move_fixed_issues_to: Optional[str] = None,
        move_affected_issues_to: Optional[str] = None,
    ) -> None:
        """
        删除版本

        DELETE /rest/api/2/version/{id}

        Args:
            version_id: 版本ID
            move_fixed_issues_to: 将"修复版本"为此版本的Issues移动到的版本ID（可选）
            move_affected_issues_to: 将"影响版本"为此版本的Issues移动到的版本ID（可选）
        """
        path = f"{self.BASE_PATH}/{version_id}"
        params: dict[str, Any] = {}
        if move_fixed_issues_to:
            params["moveFixIssuesTo"] = move_fixed_issues_to
        if move_affected_issues_to:
            params["moveAffectedIssuesTo"] = move_affected_issues_to
        await self.client.delete(path, params=params)

    async def move(
        self,
        version_id: str,
        after: Optional[str] = None,
        position: Optional[str] = None,
    ) -> Version:
        """
        移动版本位置

        POST /rest/api/2/version/{id}/move

        Args:
            version_id: 版本ID
            after: 移动到某个版本之后的版本URL（可选）
            position: 移动位置（可选，"Earlier"、"Later"、"First"、"Last"）

        Returns:
            Version: 移动后的版本
        """
        path = f"{self.BASE_PATH}/{version_id}/move"
        payload: dict[str, Any] = {}
        if after:
            payload["after"] = after
        if position:
            payload["position"] = position

        data = await self.client.post_json(path, data=payload)
        return Version.model_validate(data)

    async def move_raw(
        self,
        version_id: str,
        after: Optional[str] = None,
        position: Optional[str] = None,
    ) -> dict:
        """移动版本位置（原始JSON）"""
        path = f"{self.BASE_PATH}/{version_id}/move"
        payload: dict[str, Any] = {}
        if after:
            payload["after"] = after
        if position:
            payload["position"] = position

        return await self.client.post_json(path, data=payload)

    async def merge_to(
        self,
        version_id: str,
        move_issues_to: str,
    ) -> dict:
        """
        合并版本

        POST /rest/api/2/version/{id}/mergeto/{moveIssuesTo}

        Args:
            version_id: 要合并的版本ID
            move_issues_to: 目标版本ID

        Returns:
            dict: 合并结果
        """
        path = f"{self.BASE_PATH}/{version_id}/mergeto/{move_issues_to}"
        return await self.client.post_json(path, data=None)

    async def remove_and_swap(
        self,
        version_id: str,
        move_fixed_issues_to: Optional[str] = None,
        move_affected_issues_to: Optional[str] = None,
    ) -> dict:
        """
        删除版本并替换关联的Issues

        POST /rest/api/2/version/{id}/removeAndSwap

        Args:
            version_id: 版本ID
            move_fixed_issues_to: "修复版本"移动到的版本ID（可选）
            move_affected_issues_to: "影响版本"移动到的版本ID（可选）

        Returns:
            dict: 操作结果
        """
        path = f"{self.BASE_PATH}/{version_id}/removeAndSwap"
        payload: dict[str, Any] = {}
        if move_fixed_issues_to:
            payload["moveFixIssuesTo"] = move_fixed_issues_to
        if move_affected_issues_to:
            payload["moveAffectedIssuesTo"] = move_affected_issues_to

        return await self.client.post_json(path, data=payload)

    async def get_related_issue_counts(
        self,
        version_id: str,
    ) -> VersionIssueCounts:
        """
        获取版本关联的Issue数量

        GET /rest/api/2/version/{id}/relatedIssueCounts

        Args:
            version_id: 版本ID

        Returns:
            VersionIssueCounts: Issue数量统计
        """
        path = f"{self.BASE_PATH}/{version_id}/relatedIssueCounts"
        data = await self.client.get_json(path)
        return VersionIssueCounts.model_validate(data)

    async def get_related_issue_counts_raw(
        self,
        version_id: str,
    ) -> dict:
        """获取版本关联的Issue数量（原始JSON）"""
        path = f"{self.BASE_PATH}/{version_id}/relatedIssueCounts"
        return await self.client.get_json(path)

    async def get_unresolved_issue_count(
        self,
        version_id: str,
    ) -> VersionUnresolvedIssueCount:
        """
        获取版本未解决的Issue数量

        GET /rest/api/2/version/{id}/unresolvedIssueCount

        Args:
            version_id: 版本ID

        Returns:
            VersionUnresolvedIssueCount: 未解决Issue数量
        """
        path = f"{self.BASE_PATH}/{version_id}/unresolvedIssueCount"
        data = await self.client.get_json(path)
        return VersionUnresolvedIssueCount.model_validate(data)

    async def get_unresolved_issue_count_raw(
        self,
        version_id: str,
    ) -> dict:
        """获取版本未解决的Issue数量（原始JSON）"""
        path = f"{self.BASE_PATH}/{version_id}/unresolvedIssueCount"
        return await self.client.get_json(path)

    # ==================== Remote Links APIs ====================

    async def get_remote_links(
        self,
        version_id: str,
    ) -> list[VersionRemoteLink]:
        """
        获取版本的远程链接列表

        GET /rest/api/2/version/{versionId}/remotelink

        Args:
            version_id: 版本ID

        Returns:
            list[VersionRemoteLink]: 远程链接列表
        """
        path = f"{self.BASE_PATH}/{version_id}/remotelink"
        data = await self.client.get_json(path)
        return [VersionRemoteLink.model_validate(link) for link in data]

    async def get_remote_links_raw(
        self,
        version_id: str,
    ) -> list[dict]:
        """获取版本的远程链接列表（原始JSON）"""
        path = f"{self.BASE_PATH}/{version_id}/remotelink"
        return await self.client.get_json(path)

    async def create_remote_link(
        self,
        version_id: str,
        global_id: str,
        url: str,
        title: str,
        summary: Optional[str] = None,
        relationship: Optional[str] = None,
    ) -> VersionRemoteLink:
        """
        创建版本远程链接

        POST /rest/api/2/version/{versionId}/remotelink

        Args:
            version_id: 版本ID
            global_id: 全局ID
            url: 链接URL
            title: 链接标题
            summary: 链接摘要（可选）
            relationship: 关系类型（可选）

        Returns:
            VersionRemoteLink: 创建的远程链接
        """
        path = f"{self.BASE_PATH}/{version_id}/remotelink"
        payload: dict[str, Any] = {
            "globalId": global_id,
            "object": {
                "url": url,
                "title": title,
            }
        }
        if summary:
            payload["object"]["summary"] = summary
        if relationship:
            payload["relationship"] = relationship

        data = await self.client.post_json(path, data=payload)
        return VersionRemoteLink.model_validate(data)

    async def create_remote_link_raw(
        self,
        version_id: str,
        global_id: str,
        url: str,
        title: str,
        summary: Optional[str] = None,
        relationship: Optional[str] = None,
    ) -> dict:
        """创建版本远程链接（原始JSON）"""
        path = f"{self.BASE_PATH}/{version_id}/remotelink"
        payload: dict[str, Any] = {
            "globalId": global_id,
            "object": {
                "url": url,
                "title": title,
            }
        }
        if summary:
            payload["object"]["summary"] = summary
        if relationship:
            payload["relationship"] = relationship

        return await self.client.post_json(path, data=payload)

    async def get_remote_link(
        self,
        version_id: str,
        global_id: str,
    ) -> VersionRemoteLink:
        """
        获取版本远程链接

        GET /rest/api/2/version/{versionId}/remotelink/{globalId}

        Args:
            version_id: 版本ID
            global_id: 全局ID

        Returns:
            VersionRemoteLink: 远程链接详情
        """
        path = f"{self.BASE_PATH}/{version_id}/remotelink/{global_id}"
        data = await self.client.get_json(path)
        return VersionRemoteLink.model_validate(data)

    async def get_remote_link_raw(
        self,
        version_id: str,
        global_id: str,
    ) -> dict:
        """获取版本远程链接（原始JSON）"""
        path = f"{self.BASE_PATH}/{version_id}/remotelink/{global_id}"
        return await self.client.get_json(path)

    async def update_remote_link(
        self,
        version_id: str,
        global_id: str,
        url: Optional[str] = None,
        title: Optional[str] = None,
        summary: Optional[str] = None,
        relationship: Optional[str] = None,
    ) -> VersionRemoteLink:
        """
        更新版本远程链接

        PUT /rest/api/2/version/{versionId}/remotelink/{globalId}

        Args:
            version_id: 版本ID
            global_id: 全局ID
            url: 链接URL（可选）
            title: 链接标题（可选）
            summary: 链接摘要（可选）
            relationship: 关系类型（可选）

        Returns:
            VersionRemoteLink: 更新后的远程链接
        """
        path = f"{self.BASE_PATH}/{version_id}/remotelink/{global_id}"
        payload: dict[str, Any] = {"object": {}}
        if url:
            payload["object"]["url"] = url
        if title:
            payload["object"]["title"] = title
        if summary:
            payload["object"]["summary"] = summary
        if relationship:
            payload["relationship"] = relationship

        data = await self.client.put_json(path, data=payload)
        return VersionRemoteLink.model_validate(data)

    async def update_remote_link_raw(
        self,
        version_id: str,
        global_id: str,
        url: Optional[str] = None,
        title: Optional[str] = None,
        summary: Optional[str] = None,
        relationship: Optional[str] = None,
    ) -> dict:
        """更新版本远程链接（原始JSON）"""
        path = f"{self.BASE_PATH}/{version_id}/remotelink/{global_id}"
        payload: dict[str, Any] = {"object": {}}
        if url:
            payload["object"]["url"] = url
        if title:
            payload["object"]["title"] = title
        if summary:
            payload["object"]["summary"] = summary
        if relationship:
            payload["relationship"] = relationship

        return await self.client.put_json(path, data=payload)

    async def delete_remote_link(
        self,
        version_id: str,
        global_id: str,
    ) -> None:
        """
        删除版本远程链接

        DELETE /rest/api/2/version/{versionId}/remotelink/{globalId}

        Args:
            version_id: 版本ID
            global_id: 全局ID
        """
        path = f"{self.BASE_PATH}/{version_id}/remotelink/{global_id}"
        await self.client.delete(path)

    async def delete_remote_links_by_global_id(
        self,
        version_id: str,
        global_id: str,
    ) -> None:
        """
        按全局ID删除版本远程链接

        DELETE /rest/api/2/version/{versionId}/remotelink

        Args:
            version_id: 版本ID
            global_id: 全局ID
        """
        path = f"{self.BASE_PATH}/{version_id}/remotelink"
        params = {"globalId": global_id}
        await self.client.delete(path, params=params)
