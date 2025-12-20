"""
Component Resource - 组件资源

POST   /rest/api/2/component            - 创建组件
GET    /rest/api/2/component/{id}       - 获取组件
PUT    /rest/api/2/component/{id}       - 更新组件
DELETE /rest/api/2/component/{id}       - 删除组件
GET    /rest/api/2/component/{id}/relatedIssueCounts - 获取关联Issue数量
"""

from typing import Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.component import Component, ComponentIssueCounts


class ComponentResource(BaseResource):
    """
    组件资源

    API: /rest/api/2/component
    """

    BASE_PATH = "/rest/api/2/component"

    async def create(
        self,
        name: str,
        project: str,
        description: Optional[str] = None,
        lead_user_name: Optional[str] = None,
        assignee_type: Optional[str] = None,
    ) -> Component:
        """
        创建组件

        POST /rest/api/2/component

        Args:
            name: 组件名称
            project: 项目Key或ID
            description: 组件描述（可选）
            lead_user_name: 负责人用户名（可选）
            assignee_type: 经办人类型（可选，如"PROJECT_LEAD"、"COMPONENT_LEAD"、"PROJECT_DEFAULT"、"UNASSIGNED"）

        Returns:
            Component: 创建的组件
        """
        payload = {
            "name": name,
            "project": project,
        }
        if description:
            payload["description"] = description
        if lead_user_name:
            payload["leadUserName"] = lead_user_name
        if assignee_type:
            payload["assigneeType"] = assignee_type

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return Component.model_validate(data)

    async def create_raw(
        self,
        name: str,
        project: str,
        description: Optional[str] = None,
        lead_user_name: Optional[str] = None,
        assignee_type: Optional[str] = None,
    ) -> dict:
        """创建组件（原始JSON）"""
        payload = {
            "name": name,
            "project": project,
        }
        if description:
            payload["description"] = description
        if lead_user_name:
            payload["leadUserName"] = lead_user_name
        if assignee_type:
            payload["assigneeType"] = assignee_type

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def get(
        self,
        component_id: str,
    ) -> Component:
        """
        获取组件详情

        GET /rest/api/2/component/{id}

        Args:
            component_id: 组件ID

        Returns:
            Component: 组件详情
        """
        path = f"{self.BASE_PATH}/{component_id}"
        data = await self.client.get_json(path)
        return Component.model_validate(data)

    async def get_raw(
        self,
        component_id: str,
    ) -> dict:
        """获取组件详情（原始JSON）"""
        path = f"{self.BASE_PATH}/{component_id}"
        return await self.client.get_json(path)

    async def update(
        self,
        component_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        lead_user_name: Optional[str] = None,
        assignee_type: Optional[str] = None,
    ) -> Component:
        """
        更新组件

        PUT /rest/api/2/component/{id}

        Args:
            component_id: 组件ID
            name: 组件名称（可选）
            description: 组件描述（可选）
            lead_user_name: 负责人用户名（可选）
            assignee_type: 经办人类型（可选）

        Returns:
            Component: 更新后的组件
        """
        path = f"{self.BASE_PATH}/{component_id}"
        payload = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if lead_user_name:
            payload["leadUserName"] = lead_user_name
        if assignee_type:
            payload["assigneeType"] = assignee_type

        data = await self.client.put_json(path, data=payload)
        return Component.model_validate(data)

    async def update_raw(
        self,
        component_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        lead_user_name: Optional[str] = None,
        assignee_type: Optional[str] = None,
    ) -> dict:
        """更新组件（原始JSON）"""
        path = f"{self.BASE_PATH}/{component_id}"
        payload = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if lead_user_name:
            payload["leadUserName"] = lead_user_name
        if assignee_type:
            payload["assigneeType"] = assignee_type

        return await self.client.put_json(path, data=payload)

    async def delete(
        self,
        component_id: str,
        move_issues_to: Optional[str] = None,
    ) -> None:
        """
        删除组件

        DELETE /rest/api/2/component/{id}

        Args:
            component_id: 组件ID
            move_issues_to: 将关联的Issues移动到的组件ID（可选）
        """
        path = f"{self.BASE_PATH}/{component_id}"
        params = {}
        if move_issues_to:
            params["moveIssuesTo"] = move_issues_to
        await self.client.delete(path, params=params)

    async def get_related_issue_counts(
        self,
        component_id: str,
    ) -> ComponentIssueCounts:
        """
        获取组件关联的Issue数量

        GET /rest/api/2/component/{id}/relatedIssueCounts

        Args:
            component_id: 组件ID

        Returns:
            ComponentIssueCounts: Issue数量
        """
        path = f"{self.BASE_PATH}/{component_id}/relatedIssueCounts"
        data = await self.client.get_json(path)
        return ComponentIssueCounts.model_validate(data)

    async def get_related_issue_counts_raw(
        self,
        component_id: str,
    ) -> dict:
        """获取组件关联的Issue数量（原始JSON）"""
        path = f"{self.BASE_PATH}/{component_id}/relatedIssueCounts"
        return await self.client.get_json(path)
