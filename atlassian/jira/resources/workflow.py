"""
Workflow Resource - 工作流资源

GET /rest/api/2/workflow                - 获取所有工作流
GET /rest/api/2/workflow/{workflowName} - 获取工作流详情
POST /rest/api/2/workflow               - 创建工作流
PUT /rest/api/2/workflow/{workflowName} - 更新工作流
DELETE /rest/api/2/workflow/{workflowName} - 删除工作流
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.workflow import Workflow


class WorkflowResource(BaseResource):
    """
    工作流资源

    API: /rest/api/2/workflow
    """

    BASE_PATH = "/rest/api/2/workflow"

    # ==================== Workflow Management ====================

    async def get_all(
        self,
        workflow_name: Optional[str] = None,
    ) -> list[Workflow]:
        """
        获取所有工作流

        GET /rest/api/2/workflow

        Args:
            workflow_name: 可选，按名称过滤工作流

        Returns:
            list[Workflow]: 工作流列表
        """
        params = {}
        if workflow_name:
            params["workflowName"] = workflow_name

        data = await self.client.get_json(self.BASE_PATH, params=params)
        return [Workflow.model_validate(w) for w in data]

    async def get_all_raw(
        self,
        workflow_name: Optional[str] = None,
    ) -> list[dict]:
        """获取所有工作流（原始JSON）"""
        params = {}
        if workflow_name:
            params["workflowName"] = workflow_name

        return await self.client.get_json(self.BASE_PATH, params=params)

    async def get(
        self,
        workflow_name: str,
    ) -> Workflow:
        """
        获取工作流详情

        GET /rest/api/2/workflow/{workflowName}

        Args:
            workflow_name: 工作流名称

        Returns:
            Workflow: 工作流详情
        """
        path = f"{self.BASE_PATH}/{workflow_name}"
        data = await self.client.get_json(path)
        return Workflow.model_validate(data)

    async def get_raw(
        self,
        workflow_name: str,
    ) -> dict:
        """获取工作流详情（原始JSON）"""
        path = f"{self.BASE_PATH}/{workflow_name}"
        return await self.client.get_json(path)

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        steps: Optional[list[dict]] = None,
        statuses: Optional[list[dict]] = None,
    ) -> Workflow:
        """
        创建工作流

        POST /rest/api/2/workflow

        Args:
            name: 工作流名称
            description: 工作流描述（可选）
            steps: 工作流步骤列表（可选）
            statuses: 状态列表（可选）

        Returns:
            Workflow: 创建的工作流
        """
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        if steps:
            payload["steps"] = steps
        if statuses:
            payload["statuses"] = statuses

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return Workflow.model_validate(data)

    async def create_raw(
        self,
        name: str,
        description: Optional[str] = None,
        steps: Optional[list[dict]] = None,
        statuses: Optional[list[dict]] = None,
    ) -> dict:
        """创建工作流（原始JSON）"""
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        if steps:
            payload["steps"] = steps
        if statuses:
            payload["statuses"] = statuses

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def update(
        self,
        workflow_name: str,
        description: Optional[str] = None,
        steps: Optional[list[dict]] = None,
        statuses: Optional[list[dict]] = None,
    ) -> Workflow:
        """
        更新工作流

        PUT /rest/api/2/workflow/{workflowName}

        Args:
            workflow_name: 工作流名称
            description: 工作流描述（可选）
            steps: 工作流步骤列表（可选）
            statuses: 状态列表（可选）

        Returns:
            Workflow: 更新后的工作流
        """
        path = f"{self.BASE_PATH}/{workflow_name}"
        payload: dict[str, Any] = {}
        if description:
            payload["description"] = description
        if steps:
            payload["steps"] = steps
        if statuses:
            payload["statuses"] = statuses

        data = await self.client.put_json(path, data=payload)
        return Workflow.model_validate(data)

    async def update_raw(
        self,
        workflow_name: str,
        description: Optional[str] = None,
        steps: Optional[list[dict]] = None,
        statuses: Optional[list[dict]] = None,
    ) -> dict:
        """更新工作流（原始JSON）"""
        path = f"{self.BASE_PATH}/{workflow_name}"
        payload: dict[str, Any] = {}
        if description:
            payload["description"] = description
        if steps:
            payload["steps"] = steps
        if statuses:
            payload["statuses"] = statuses

        return await self.client.put_json(path, data=payload)

    async def delete(
        self,
        workflow_name: str,
    ) -> None:
        """
        删除工作流

        DELETE /rest/api/2/workflow/{workflowName}

        Args:
            workflow_name: 工作流名称
        """
        path = f"{self.BASE_PATH}/{workflow_name}"
        await self.client.delete(path)
