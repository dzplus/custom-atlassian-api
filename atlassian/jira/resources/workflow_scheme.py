"""
Workflow Scheme Resource - 工作流方案资源

Scheme CRUD:
POST   /rest/api/2/workflowscheme                              - 创建工作流方案
GET    /rest/api/2/workflowscheme/{id}                         - 获取工作流方案
PUT    /rest/api/2/workflowscheme/{id}                         - 更新工作流方案
DELETE /rest/api/2/workflowscheme/{id}                         - 删除工作流方案

Default Workflow:
GET    /rest/api/2/workflowscheme/{id}/default                 - 获取默认工作流
PUT    /rest/api/2/workflowscheme/{id}/default                 - 设置默认工作流
DELETE /rest/api/2/workflowscheme/{id}/default                 - 删除默认工作流

Issue Type Mapping:
GET    /rest/api/2/workflowscheme/{id}/issuetype/{issueType}   - 获取Issue类型工作流
PUT    /rest/api/2/workflowscheme/{id}/issuetype/{issueType}   - 设置Issue类型工作流
DELETE /rest/api/2/workflowscheme/{id}/issuetype/{issueType}   - 删除Issue类型工作流

Workflow Mapping:
GET    /rest/api/2/workflowscheme/{id}/workflow                - 获取工作流映射
PUT    /rest/api/2/workflowscheme/{id}/workflow                - 更新工作流映射
DELETE /rest/api/2/workflowscheme/{id}/workflow                - 删除工作流映射

Draft Management:
GET    /rest/api/2/workflowscheme/{id}/createdraft             - 创建草稿
GET    /rest/api/2/workflowscheme/{id}/draft                   - 获取草稿
PUT    /rest/api/2/workflowscheme/{id}/draft                   - 更新草稿
DELETE /rest/api/2/workflowscheme/{id}/draft                   - 删除草稿
POST   /rest/api/2/workflowscheme/{id}/draft/publish           - 发布草稿
GET    /rest/api/2/workflowscheme/{id}/draft/default           - 获取草稿默认工作流
PUT    /rest/api/2/workflowscheme/{id}/draft/default           - 设置草稿默认工作流
DELETE /rest/api/2/workflowscheme/{id}/draft/default           - 删除草稿默认工作流
GET    /rest/api/2/workflowscheme/{id}/draft/issuetype/{issueType} - 获取草稿Issue类型工作流
PUT    /rest/api/2/workflowscheme/{id}/draft/issuetype/{issueType} - 设置草稿Issue类型工作流
DELETE /rest/api/2/workflowscheme/{id}/draft/issuetype/{issueType} - 删除草稿Issue类型工作流
GET    /rest/api/2/workflowscheme/{id}/draft/workflow          - 获取草稿工作流映射
PUT    /rest/api/2/workflowscheme/{id}/draft/workflow          - 更新草稿工作流映射
DELETE /rest/api/2/workflowscheme/{id}/draft/workflow          - 删除草稿工作流映射
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.workflow import (
    WorkflowScheme,
    WorkflowSchemeDraft,
    DefaultWorkflow,
    IssueTypeMapping,
    WorkflowMapping,
)


class WorkflowSchemeResource(BaseResource):
    """
    工作流方案资源

    API: /rest/api/2/workflowscheme
    """

    BASE_PATH = "/rest/api/2/workflowscheme"

    # ==================== Scheme CRUD ====================

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        default_workflow: Optional[str] = None,
        issue_type_mappings: Optional[dict[str, str]] = None,
        draft: bool = False,
    ) -> WorkflowScheme:
        """
        创建工作流方案

        POST /rest/api/2/workflowscheme

        Args:
            name: 方案名称
            description: 方案描述（可选）
            default_workflow: 默认工作流名称（可选）
            issue_type_mappings: Issue类型到工作流的映射（可选）
            draft: 是否创建为草稿（默认False）

        Returns:
            WorkflowScheme: 创建的工作流方案
        """
        payload: dict[str, Any] = {
            "name": name,
            "draft": draft,
        }
        if description:
            payload["description"] = description
        if default_workflow:
            payload["defaultWorkflow"] = default_workflow
        if issue_type_mappings:
            payload["issueTypeMappings"] = issue_type_mappings

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return WorkflowScheme.model_validate(data)

    async def create_raw(
        self,
        name: str,
        description: Optional[str] = None,
        default_workflow: Optional[str] = None,
        issue_type_mappings: Optional[dict[str, str]] = None,
        draft: bool = False,
    ) -> dict:
        """创建工作流方案（原始JSON）"""
        payload: dict[str, Any] = {
            "name": name,
            "draft": draft,
        }
        if description:
            payload["description"] = description
        if default_workflow:
            payload["defaultWorkflow"] = default_workflow
        if issue_type_mappings:
            payload["issueTypeMappings"] = issue_type_mappings

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def get(
        self,
        scheme_id: int,
        return_draft_if_exists: bool = False,
    ) -> WorkflowScheme:
        """
        获取工作流方案

        GET /rest/api/2/workflowscheme/{id}

        Args:
            scheme_id: 方案ID
            return_draft_if_exists: 如果存在草稿则返回草稿（默认False）

        Returns:
            WorkflowScheme: 工作流方案详情
        """
        path = f"{self.BASE_PATH}/{scheme_id}"
        params = {}
        if return_draft_if_exists:
            params["returnDraftIfExists"] = "true"

        data = await self.client.get_json(path, params=params)
        return WorkflowScheme.model_validate(data)

    async def get_raw(
        self,
        scheme_id: int,
        return_draft_if_exists: bool = False,
    ) -> dict:
        """获取工作流方案（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}"
        params = {}
        if return_draft_if_exists:
            params["returnDraftIfExists"] = "true"

        return await self.client.get_json(path, params=params)

    async def update(
        self,
        scheme_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        default_workflow: Optional[str] = None,
        issue_type_mappings: Optional[dict[str, str]] = None,
        update_draft_if_needed: bool = False,
    ) -> WorkflowScheme:
        """
        更新工作流方案

        PUT /rest/api/2/workflowscheme/{id}

        Args:
            scheme_id: 方案ID
            name: 方案名称（可选）
            description: 方案描述（可选）
            default_workflow: 默认工作流名称（可选）
            issue_type_mappings: Issue类型到工作流的映射（可选）
            update_draft_if_needed: 如果需要则更新草稿（默认False）

        Returns:
            WorkflowScheme: 更新后的工作流方案
        """
        path = f"{self.BASE_PATH}/{scheme_id}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if default_workflow:
            payload["defaultWorkflow"] = default_workflow
        if issue_type_mappings:
            payload["issueTypeMappings"] = issue_type_mappings
        if update_draft_if_needed:
            payload["updateDraftIfNeeded"] = update_draft_if_needed

        data = await self.client.put_json(path, data=payload)
        return WorkflowScheme.model_validate(data)

    async def update_raw(
        self,
        scheme_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        default_workflow: Optional[str] = None,
        issue_type_mappings: Optional[dict[str, str]] = None,
        update_draft_if_needed: bool = False,
    ) -> dict:
        """更新工作流方案（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if default_workflow:
            payload["defaultWorkflow"] = default_workflow
        if issue_type_mappings:
            payload["issueTypeMappings"] = issue_type_mappings
        if update_draft_if_needed:
            payload["updateDraftIfNeeded"] = update_draft_if_needed

        return await self.client.put_json(path, data=payload)

    async def delete(
        self,
        scheme_id: int,
    ) -> None:
        """
        删除工作流方案

        DELETE /rest/api/2/workflowscheme/{id}

        Args:
            scheme_id: 方案ID
        """
        path = f"{self.BASE_PATH}/{scheme_id}"
        await self.client.delete(path)

    # ==================== Default Workflow ====================

    async def get_default_workflow(
        self,
        scheme_id: int,
        return_draft_if_exists: bool = False,
    ) -> DefaultWorkflow:
        """
        获取默认工作流

        GET /rest/api/2/workflowscheme/{id}/default

        Args:
            scheme_id: 方案ID
            return_draft_if_exists: 如果存在草稿则返回草稿（默认False）

        Returns:
            DefaultWorkflow: 默认工作流
        """
        path = f"{self.BASE_PATH}/{scheme_id}/default"
        params = {}
        if return_draft_if_exists:
            params["returnDraftIfExists"] = "true"

        data = await self.client.get_json(path, params=params)
        return DefaultWorkflow.model_validate(data)

    async def get_default_workflow_raw(
        self,
        scheme_id: int,
        return_draft_if_exists: bool = False,
    ) -> dict:
        """获取默认工作流（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/default"
        params = {}
        if return_draft_if_exists:
            params["returnDraftIfExists"] = "true"

        return await self.client.get_json(path, params=params)

    async def set_default_workflow(
        self,
        scheme_id: int,
        workflow: str,
        update_draft_if_needed: bool = False,
    ) -> WorkflowScheme:
        """
        设置默认工作流

        PUT /rest/api/2/workflowscheme/{id}/default

        Args:
            scheme_id: 方案ID
            workflow: 工作流名称
            update_draft_if_needed: 如果需要则更新草稿（默认False）

        Returns:
            WorkflowScheme: 更新后的工作流方案
        """
        path = f"{self.BASE_PATH}/{scheme_id}/default"
        payload = {
            "workflow": workflow,
            "updateDraftIfNeeded": update_draft_if_needed,
        }

        data = await self.client.put_json(path, data=payload)
        return WorkflowScheme.model_validate(data)

    async def set_default_workflow_raw(
        self,
        scheme_id: int,
        workflow: str,
        update_draft_if_needed: bool = False,
    ) -> dict:
        """设置默认工作流（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/default"
        payload = {
            "workflow": workflow,
            "updateDraftIfNeeded": update_draft_if_needed,
        }

        return await self.client.put_json(path, data=payload)

    async def delete_default_workflow(
        self,
        scheme_id: int,
        update_draft_if_needed: bool = False,
    ) -> WorkflowScheme:
        """
        删除默认工作流

        DELETE /rest/api/2/workflowscheme/{id}/default

        Args:
            scheme_id: 方案ID
            update_draft_if_needed: 如果需要则更新草稿（默认False）

        Returns:
            WorkflowScheme: 更新后的工作流方案
        """
        path = f"{self.BASE_PATH}/{scheme_id}/default"
        params = {}
        if update_draft_if_needed:
            params["updateDraftIfNeeded"] = "true"

        data = await self.client.delete(path, params=params)
        return WorkflowScheme.model_validate(data)

    async def delete_default_workflow_raw(
        self,
        scheme_id: int,
        update_draft_if_needed: bool = False,
    ) -> dict:
        """删除默认工作流（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/default"
        params = {}
        if update_draft_if_needed:
            params["updateDraftIfNeeded"] = "true"

        return await self.client.delete(path, params=params)

    # ==================== Issue Type Mapping ====================

    async def get_issue_type_workflow(
        self,
        scheme_id: int,
        issue_type: str,
        return_draft_if_exists: bool = False,
    ) -> IssueTypeMapping:
        """
        获取Issue类型工作流

        GET /rest/api/2/workflowscheme/{id}/issuetype/{issueType}

        Args:
            scheme_id: 方案ID
            issue_type: Issue类型ID
            return_draft_if_exists: 如果存在草稿则返回草稿（默认False）

        Returns:
            IssueTypeMapping: Issue类型工作流映射
        """
        path = f"{self.BASE_PATH}/{scheme_id}/issuetype/{issue_type}"
        params = {}
        if return_draft_if_exists:
            params["returnDraftIfExists"] = "true"

        data = await self.client.get_json(path, params=params)
        return IssueTypeMapping.model_validate(data)

    async def get_issue_type_workflow_raw(
        self,
        scheme_id: int,
        issue_type: str,
        return_draft_if_exists: bool = False,
    ) -> dict:
        """获取Issue类型工作流（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/issuetype/{issue_type}"
        params = {}
        if return_draft_if_exists:
            params["returnDraftIfExists"] = "true"

        return await self.client.get_json(path, params=params)

    async def set_issue_type_workflow(
        self,
        scheme_id: int,
        issue_type: str,
        workflow: str,
        update_draft_if_needed: bool = False,
    ) -> WorkflowScheme:
        """
        设置Issue类型工作流

        PUT /rest/api/2/workflowscheme/{id}/issuetype/{issueType}

        Args:
            scheme_id: 方案ID
            issue_type: Issue类型ID
            workflow: 工作流名称
            update_draft_if_needed: 如果需要则更新草稿（默认False）

        Returns:
            WorkflowScheme: 更新后的工作流方案
        """
        path = f"{self.BASE_PATH}/{scheme_id}/issuetype/{issue_type}"
        payload = {
            "issueType": issue_type,
            "workflow": workflow,
            "updateDraftIfNeeded": update_draft_if_needed,
        }

        data = await self.client.put_json(path, data=payload)
        return WorkflowScheme.model_validate(data)

    async def set_issue_type_workflow_raw(
        self,
        scheme_id: int,
        issue_type: str,
        workflow: str,
        update_draft_if_needed: bool = False,
    ) -> dict:
        """设置Issue类型工作流（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/issuetype/{issue_type}"
        payload = {
            "issueType": issue_type,
            "workflow": workflow,
            "updateDraftIfNeeded": update_draft_if_needed,
        }

        return await self.client.put_json(path, data=payload)

    async def delete_issue_type_workflow(
        self,
        scheme_id: int,
        issue_type: str,
        update_draft_if_needed: bool = False,
    ) -> WorkflowScheme:
        """
        删除Issue类型工作流

        DELETE /rest/api/2/workflowscheme/{id}/issuetype/{issueType}

        Args:
            scheme_id: 方案ID
            issue_type: Issue类型ID
            update_draft_if_needed: 如果需要则更新草稿（默认False）

        Returns:
            WorkflowScheme: 更新后的工作流方案
        """
        path = f"{self.BASE_PATH}/{scheme_id}/issuetype/{issue_type}"
        params = {}
        if update_draft_if_needed:
            params["updateDraftIfNeeded"] = "true"

        data = await self.client.delete(path, params=params)
        return WorkflowScheme.model_validate(data)

    async def delete_issue_type_workflow_raw(
        self,
        scheme_id: int,
        issue_type: str,
        update_draft_if_needed: bool = False,
    ) -> dict:
        """删除Issue类型工作流（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/issuetype/{issue_type}"
        params = {}
        if update_draft_if_needed:
            params["updateDraftIfNeeded"] = "true"

        return await self.client.delete(path, params=params)

    # ==================== Workflow Mapping ====================

    async def get_workflow_mappings(
        self,
        scheme_id: int,
        workflow_name: Optional[str] = None,
        return_draft_if_exists: bool = False,
    ) -> list[WorkflowMapping]:
        """
        获取工作流映射

        GET /rest/api/2/workflowscheme/{id}/workflow

        Args:
            scheme_id: 方案ID
            workflow_name: 工作流名称（可选，用于过滤）
            return_draft_if_exists: 如果存在草稿则返回草稿（默认False）

        Returns:
            list[WorkflowMapping]: 工作流映射列表
        """
        path = f"{self.BASE_PATH}/{scheme_id}/workflow"
        params = {}
        if workflow_name:
            params["workflowName"] = workflow_name
        if return_draft_if_exists:
            params["returnDraftIfExists"] = "true"

        data = await self.client.get_json(path, params=params)
        return [WorkflowMapping.model_validate(m) for m in data]

    async def get_workflow_mappings_raw(
        self,
        scheme_id: int,
        workflow_name: Optional[str] = None,
        return_draft_if_exists: bool = False,
    ) -> list[dict]:
        """获取工作流映射（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/workflow"
        params = {}
        if workflow_name:
            params["workflowName"] = workflow_name
        if return_draft_if_exists:
            params["returnDraftIfExists"] = "true"

        return await self.client.get_json(path, params=params)

    async def update_workflow_mappings(
        self,
        scheme_id: int,
        workflow: str,
        issue_types: list[str],
        update_draft_if_needed: bool = False,
    ) -> WorkflowScheme:
        """
        更新工作流映射

        PUT /rest/api/2/workflowscheme/{id}/workflow

        Args:
            scheme_id: 方案ID
            workflow: 工作流名称
            issue_types: Issue类型ID列表
            update_draft_if_needed: 如果需要则更新草稿（默认False）

        Returns:
            WorkflowScheme: 更新后的工作流方案
        """
        path = f"{self.BASE_PATH}/{scheme_id}/workflow"
        payload = {
            "workflow": workflow,
            "issueTypes": issue_types,
            "updateDraftIfNeeded": update_draft_if_needed,
        }

        data = await self.client.put_json(path, data=payload)
        return WorkflowScheme.model_validate(data)

    async def update_workflow_mappings_raw(
        self,
        scheme_id: int,
        workflow: str,
        issue_types: list[str],
        update_draft_if_needed: bool = False,
    ) -> dict:
        """更新工作流映射（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/workflow"
        payload = {
            "workflow": workflow,
            "issueTypes": issue_types,
            "updateDraftIfNeeded": update_draft_if_needed,
        }

        return await self.client.put_json(path, data=payload)

    async def delete_workflow_mapping(
        self,
        scheme_id: int,
        workflow_name: str,
        update_draft_if_needed: bool = False,
    ) -> None:
        """
        删除工作流映射

        DELETE /rest/api/2/workflowscheme/{id}/workflow

        Args:
            scheme_id: 方案ID
            workflow_name: 工作流名称
            update_draft_if_needed: 如果需要则更新草稿（默认False）
        """
        path = f"{self.BASE_PATH}/{scheme_id}/workflow"
        params = {"workflowName": workflow_name}
        if update_draft_if_needed:
            params["updateDraftIfNeeded"] = "true"

        await self.client.delete(path, params=params)

    # ==================== Draft Management ====================

    async def create_draft(
        self,
        scheme_id: int,
    ) -> WorkflowSchemeDraft:
        """
        创建草稿

        GET /rest/api/2/workflowscheme/{id}/createdraft

        Args:
            scheme_id: 方案ID

        Returns:
            WorkflowSchemeDraft: 创建的草稿
        """
        path = f"{self.BASE_PATH}/{scheme_id}/createdraft"
        data = await self.client.get_json(path)
        return WorkflowSchemeDraft.model_validate(data)

    async def create_draft_raw(
        self,
        scheme_id: int,
    ) -> dict:
        """创建草稿（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/createdraft"
        return await self.client.get_json(path)

    async def get_draft(
        self,
        scheme_id: int,
    ) -> WorkflowSchemeDraft:
        """
        获取草稿

        GET /rest/api/2/workflowscheme/{id}/draft

        Args:
            scheme_id: 方案ID

        Returns:
            WorkflowSchemeDraft: 草稿详情
        """
        path = f"{self.BASE_PATH}/{scheme_id}/draft"
        data = await self.client.get_json(path)
        return WorkflowSchemeDraft.model_validate(data)

    async def get_draft_raw(
        self,
        scheme_id: int,
    ) -> dict:
        """获取草稿（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/draft"
        return await self.client.get_json(path)

    async def update_draft(
        self,
        scheme_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        default_workflow: Optional[str] = None,
        issue_type_mappings: Optional[dict[str, str]] = None,
    ) -> WorkflowSchemeDraft:
        """
        更新草稿

        PUT /rest/api/2/workflowscheme/{id}/draft

        Args:
            scheme_id: 方案ID
            name: 方案名称（可选）
            description: 方案描述（可选）
            default_workflow: 默认工作流名称（可选）
            issue_type_mappings: Issue类型到工作流的映射（可选）

        Returns:
            WorkflowSchemeDraft: 更新后的草稿
        """
        path = f"{self.BASE_PATH}/{scheme_id}/draft"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if default_workflow:
            payload["defaultWorkflow"] = default_workflow
        if issue_type_mappings:
            payload["issueTypeMappings"] = issue_type_mappings

        data = await self.client.put_json(path, data=payload)
        return WorkflowSchemeDraft.model_validate(data)

    async def update_draft_raw(
        self,
        scheme_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        default_workflow: Optional[str] = None,
        issue_type_mappings: Optional[dict[str, str]] = None,
    ) -> dict:
        """更新草稿（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/draft"
        payload: dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if default_workflow:
            payload["defaultWorkflow"] = default_workflow
        if issue_type_mappings:
            payload["issueTypeMappings"] = issue_type_mappings

        return await self.client.put_json(path, data=payload)

    async def delete_draft(
        self,
        scheme_id: int,
    ) -> None:
        """
        删除草稿

        DELETE /rest/api/2/workflowscheme/{id}/draft

        Args:
            scheme_id: 方案ID
        """
        path = f"{self.BASE_PATH}/{scheme_id}/draft"
        await self.client.delete(path)

    async def publish_draft(
        self,
        scheme_id: int,
        validate_only: bool = False,
    ) -> dict:
        """
        发布草稿

        POST /rest/api/2/workflowscheme/{id}/draft/publish

        Args:
            scheme_id: 方案ID
            validate_only: 仅验证不发布（默认False）

        Returns:
            dict: 发布结果
        """
        path = f"{self.BASE_PATH}/{scheme_id}/draft/publish"
        params = {}
        if validate_only:
            params["validateOnly"] = "true"

        return await self.client.post_json(path, params=params, data=None)

    async def get_draft_default_workflow(
        self,
        scheme_id: int,
    ) -> DefaultWorkflow:
        """
        获取草稿默认工作流

        GET /rest/api/2/workflowscheme/{id}/draft/default

        Args:
            scheme_id: 方案ID

        Returns:
            DefaultWorkflow: 默认工作流
        """
        path = f"{self.BASE_PATH}/{scheme_id}/draft/default"
        data = await self.client.get_json(path)
        return DefaultWorkflow.model_validate(data)

    async def get_draft_default_workflow_raw(
        self,
        scheme_id: int,
    ) -> dict:
        """获取草稿默认工作流（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/draft/default"
        return await self.client.get_json(path)

    async def set_draft_default_workflow(
        self,
        scheme_id: int,
        workflow: str,
    ) -> WorkflowSchemeDraft:
        """
        设置草稿默认工作流

        PUT /rest/api/2/workflowscheme/{id}/draft/default

        Args:
            scheme_id: 方案ID
            workflow: 工作流名称

        Returns:
            WorkflowSchemeDraft: 更新后的草稿
        """
        path = f"{self.BASE_PATH}/{scheme_id}/draft/default"
        payload = {"workflow": workflow}

        data = await self.client.put_json(path, data=payload)
        return WorkflowSchemeDraft.model_validate(data)

    async def set_draft_default_workflow_raw(
        self,
        scheme_id: int,
        workflow: str,
    ) -> dict:
        """设置草稿默认工作流（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/draft/default"
        payload = {"workflow": workflow}

        return await self.client.put_json(path, data=payload)

    async def delete_draft_default_workflow(
        self,
        scheme_id: int,
    ) -> WorkflowSchemeDraft:
        """
        删除草稿默认工作流

        DELETE /rest/api/2/workflowscheme/{id}/draft/default

        Args:
            scheme_id: 方案ID

        Returns:
            WorkflowSchemeDraft: 更新后的草稿
        """
        path = f"{self.BASE_PATH}/{scheme_id}/draft/default"
        data = await self.client.delete(path)
        return WorkflowSchemeDraft.model_validate(data)

    async def delete_draft_default_workflow_raw(
        self,
        scheme_id: int,
    ) -> dict:
        """删除草稿默认工作流（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/draft/default"
        return await self.client.delete(path)

    async def get_draft_issue_type_workflow(
        self,
        scheme_id: int,
        issue_type: str,
    ) -> IssueTypeMapping:
        """
        获取草稿Issue类型工作流

        GET /rest/api/2/workflowscheme/{id}/draft/issuetype/{issueType}

        Args:
            scheme_id: 方案ID
            issue_type: Issue类型ID

        Returns:
            IssueTypeMapping: Issue类型工作流映射
        """
        path = f"{self.BASE_PATH}/{scheme_id}/draft/issuetype/{issue_type}"
        data = await self.client.get_json(path)
        return IssueTypeMapping.model_validate(data)

    async def get_draft_issue_type_workflow_raw(
        self,
        scheme_id: int,
        issue_type: str,
    ) -> dict:
        """获取草稿Issue类型工作流（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/draft/issuetype/{issue_type}"
        return await self.client.get_json(path)

    async def set_draft_issue_type_workflow(
        self,
        scheme_id: int,
        issue_type: str,
        workflow: str,
    ) -> WorkflowSchemeDraft:
        """
        设置草稿Issue类型工作流

        PUT /rest/api/2/workflowscheme/{id}/draft/issuetype/{issueType}

        Args:
            scheme_id: 方案ID
            issue_type: Issue类型ID
            workflow: 工作流名称

        Returns:
            WorkflowSchemeDraft: 更新后的草稿
        """
        path = f"{self.BASE_PATH}/{scheme_id}/draft/issuetype/{issue_type}"
        payload = {
            "issueType": issue_type,
            "workflow": workflow,
        }

        data = await self.client.put_json(path, data=payload)
        return WorkflowSchemeDraft.model_validate(data)

    async def set_draft_issue_type_workflow_raw(
        self,
        scheme_id: int,
        issue_type: str,
        workflow: str,
    ) -> dict:
        """设置草稿Issue类型工作流（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/draft/issuetype/{issue_type}"
        payload = {
            "issueType": issue_type,
            "workflow": workflow,
        }

        return await self.client.put_json(path, data=payload)

    async def delete_draft_issue_type_workflow(
        self,
        scheme_id: int,
        issue_type: str,
    ) -> WorkflowSchemeDraft:
        """
        删除草稿Issue类型工作流

        DELETE /rest/api/2/workflowscheme/{id}/draft/issuetype/{issueType}

        Args:
            scheme_id: 方案ID
            issue_type: Issue类型ID

        Returns:
            WorkflowSchemeDraft: 更新后的草稿
        """
        path = f"{self.BASE_PATH}/{scheme_id}/draft/issuetype/{issue_type}"
        data = await self.client.delete(path)
        return WorkflowSchemeDraft.model_validate(data)

    async def delete_draft_issue_type_workflow_raw(
        self,
        scheme_id: int,
        issue_type: str,
    ) -> dict:
        """删除草稿Issue类型工作流（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/draft/issuetype/{issue_type}"
        return await self.client.delete(path)

    async def get_draft_workflow_mappings(
        self,
        scheme_id: int,
        workflow_name: Optional[str] = None,
    ) -> list[WorkflowMapping]:
        """
        获取草稿工作流映射

        GET /rest/api/2/workflowscheme/{id}/draft/workflow

        Args:
            scheme_id: 方案ID
            workflow_name: 工作流名称（可选，用于过滤）

        Returns:
            list[WorkflowMapping]: 工作流映射列表
        """
        path = f"{self.BASE_PATH}/{scheme_id}/draft/workflow"
        params = {}
        if workflow_name:
            params["workflowName"] = workflow_name

        data = await self.client.get_json(path, params=params)
        return [WorkflowMapping.model_validate(m) for m in data]

    async def get_draft_workflow_mappings_raw(
        self,
        scheme_id: int,
        workflow_name: Optional[str] = None,
    ) -> list[dict]:
        """获取草稿工作流映射（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/draft/workflow"
        params = {}
        if workflow_name:
            params["workflowName"] = workflow_name

        return await self.client.get_json(path, params=params)

    async def update_draft_workflow_mappings(
        self,
        scheme_id: int,
        workflow: str,
        issue_types: list[str],
    ) -> WorkflowSchemeDraft:
        """
        更新草稿工作流映射

        PUT /rest/api/2/workflowscheme/{id}/draft/workflow

        Args:
            scheme_id: 方案ID
            workflow: 工作流名称
            issue_types: Issue类型ID列表

        Returns:
            WorkflowSchemeDraft: 更新后的草稿
        """
        path = f"{self.BASE_PATH}/{scheme_id}/draft/workflow"
        payload = {
            "workflow": workflow,
            "issueTypes": issue_types,
        }

        data = await self.client.put_json(path, data=payload)
        return WorkflowSchemeDraft.model_validate(data)

    async def update_draft_workflow_mappings_raw(
        self,
        scheme_id: int,
        workflow: str,
        issue_types: list[str],
    ) -> dict:
        """更新草稿工作流映射（原始JSON）"""
        path = f"{self.BASE_PATH}/{scheme_id}/draft/workflow"
        payload = {
            "workflow": workflow,
            "issueTypes": issue_types,
        }

        return await self.client.put_json(path, data=payload)

    async def delete_draft_workflow_mapping(
        self,
        scheme_id: int,
        workflow_name: str,
    ) -> None:
        """
        删除草稿工作流映射

        DELETE /rest/api/2/workflowscheme/{id}/draft/workflow

        Args:
            scheme_id: 方案ID
            workflow_name: 工作流名称
        """
        path = f"{self.BASE_PATH}/{scheme_id}/draft/workflow"
        params = {"workflowName": workflow_name}

        await self.client.delete(path, params=params)
