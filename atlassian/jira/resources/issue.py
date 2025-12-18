"""
Issue Resource - Issue API

POST   /rest/api/2/issue                           - 创建 Issue
POST   /rest/api/2/issue/bulk                      - 批量创建 Issue
GET    /rest/api/2/issue/{issueIdOrKey}            - 获取 Issue
PUT    /rest/api/2/issue/{issueIdOrKey}            - 更新 Issue
DELETE /rest/api/2/issue/{issueIdOrKey}            - 删除 Issue
PUT    /rest/api/2/issue/{issueIdOrKey}/assignee   - 分配 Issue
GET    /rest/api/2/issue/{issueIdOrKey}/transitions - 获取转换
POST   /rest/api/2/issue/{issueIdOrKey}/transitions - 执行转换
GET    /rest/api/2/issue/{issueIdOrKey}/comment    - 获取评论
POST   /rest/api/2/issue/{issueIdOrKey}/comment    - 添加评论
GET    /rest/api/2/issue/{issueIdOrKey}/subtask    - 获取子任务
POST   /rest/api/2/issue/{issueIdOrKey}/attachments - 上传附件
"""

from typing import Any, Optional
from pathlib import Path

from atlassian.common.base import BaseResource
from atlassian.jira.models.issue import (
    Issue,
    IssueTransition,
    IssueComment,
    IssueComments,
    CreateIssueResponse,
)
from atlassian.jira.models.attachment import Attachment


class IssueResource(BaseResource):
    """
    Issue 资源

    API: /rest/api/2/issue
    """

    BASE_PATH = "/rest/api/2/issue"

    # ========== Issue CRUD ==========

    async def create(
        self,
        project: str,
        summary: str,
        issue_type: str,
        description: Optional[str] = None,
        assignee: Optional[str] = None,
        priority: Optional[str] = None,
        labels: Optional[list[str]] = None,
        components: Optional[list[str]] = None,
        custom_fields: Optional[dict] = None,
        **extra_fields,
    ) -> CreateIssueResponse:
        """
        创建 Issue

        POST /rest/api/2/issue

        Args:
            project: 项目 key 或 ID
            summary: 摘要
            issue_type: Issue 类型名称或 ID
            description: 描述（可选）
            assignee: 分配人用户名（可选）
            priority: 优先级名称（可选）
            labels: 标签列表（可选）
            components: 组件名称列表（可选）
            custom_fields: 自定义字段（可选），如 {"customfield_10001": "value"}
            **extra_fields: 其他字段

        Returns:
            CreateIssueResponse: 创建结果，包含 id, key, self
        """
        fields: dict[str, Any] = {
            "project": {"key": project} if not project.isdigit() else {"id": project},
            "summary": summary,
            "issuetype": {"name": issue_type} if not issue_type.isdigit() else {"id": issue_type},
        }

        if description:
            fields["description"] = description
        if assignee:
            fields["assignee"] = {"name": assignee}
        if priority:
            fields["priority"] = {"name": priority}
        if labels:
            fields["labels"] = labels
        if components:
            fields["components"] = [{"name": c} for c in components]
        if custom_fields:
            fields.update(custom_fields)

        fields.update(extra_fields)

        payload = {"fields": fields}
        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return CreateIssueResponse.model_validate(data)

    async def create_raw(self, payload: dict) -> dict:
        """
        使用原始 payload 创建 Issue

        Args:
            payload: 原始请求体

        Returns:
            dict: 创建结果
        """
        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def bulk_create(self, issues: list[dict]) -> dict:
        """
        批量创建 Issue

        POST /rest/api/2/issue/bulk

        Args:
            issues: Issue 列表，每个元素为 {"fields": {...}} 格式

        Returns:
            dict: 创建结果
        """
        payload = {"issueUpdates": issues}
        return await self.client.post_json(f"{self.BASE_PATH}/bulk", data=payload)

    async def get(
        self,
        issue_id_or_key: str,
        fields: Optional[list[str]] = None,
        expand: Optional[str] = None,
    ) -> Issue:
        """
        获取 Issue

        GET /rest/api/2/issue/{issueIdOrKey}

        Args:
            issue_id_or_key: Issue ID 或 Key
            fields: 要返回的字段列表（可选）
            expand: 展开的字段（可选），如 "renderedFields,transitions,changelog"

        Returns:
            Issue: Issue 信息
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}"
        params = {}
        if fields:
            params["fields"] = ",".join(fields)
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return Issue.model_validate(data)

    async def get_raw(
        self,
        issue_id_or_key: str,
        fields: Optional[list[str]] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """
        获取 Issue（原始 JSON）

        Args:
            issue_id_or_key: Issue ID 或 Key
            fields: 要返回的字段列表（可选）
            expand: 展开的字段（可选）

        Returns:
            dict: 原始 JSON 响应
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}"
        params = {}
        if fields:
            params["fields"] = ",".join(fields)
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    async def update(
        self,
        issue_id_or_key: str,
        fields: Optional[dict] = None,
        update: Optional[dict] = None,
        notify_users: bool = True,
    ) -> None:
        """
        更新 Issue

        PUT /rest/api/2/issue/{issueIdOrKey}

        Args:
            issue_id_or_key: Issue ID 或 Key
            fields: 要更新的字段（直接设置）
            update: 要更新的字段（使用操作，如 add/set/remove）
            notify_users: 是否通知用户（默认 True）
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}"
        params = {}
        if not notify_users:
            params["notifyUsers"] = "false"

        payload = {}
        if fields:
            payload["fields"] = fields
        if update:
            payload["update"] = update

        response = await self.client.put(path, json=payload, params=params)
        response.raise_for_status()

    async def delete(
        self,
        issue_id_or_key: str,
        delete_subtasks: bool = False,
    ) -> None:
        """
        删除 Issue

        DELETE /rest/api/2/issue/{issueIdOrKey}

        Args:
            issue_id_or_key: Issue ID 或 Key
            delete_subtasks: 是否删除子任务（默认 False）
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}"
        params = {}
        if delete_subtasks:
            params["deleteSubtasks"] = "true"

        response = await self.client.delete(path, params=params)
        response.raise_for_status()

    # ========== Assignee ==========

    async def assign(self, issue_id_or_key: str, assignee: Optional[str]) -> None:
        """
        分配 Issue

        PUT /rest/api/2/issue/{issueIdOrKey}/assignee

        Args:
            issue_id_or_key: Issue ID 或 Key
            assignee: 分配人用户名，None 表示取消分配
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/assignee"
        payload = {"name": assignee}
        response = await self.client.put(path, json=payload)
        response.raise_for_status()

    # ========== Transitions ==========

    async def get_transitions(
        self,
        issue_id_or_key: str,
        expand: Optional[str] = None,
    ) -> list[IssueTransition]:
        """
        获取 Issue 可用转换

        GET /rest/api/2/issue/{issueIdOrKey}/transitions

        Args:
            issue_id_or_key: Issue ID 或 Key
            expand: 展开的字段（可选），如 "transitions.fields"

        Returns:
            list[IssueTransition]: 转换列表
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/transitions"
        params = {}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        transitions = data.get("transitions", [])
        return [IssueTransition.model_validate(t) for t in transitions]

    async def do_transition(
        self,
        issue_id_or_key: str,
        transition_id: str,
        fields: Optional[dict] = None,
        update: Optional[dict] = None,
        comment: Optional[str] = None,
    ) -> None:
        """
        执行 Issue 转换

        POST /rest/api/2/issue/{issueIdOrKey}/transitions

        Args:
            issue_id_or_key: Issue ID 或 Key
            transition_id: 转换 ID
            fields: 转换时设置的字段（可选）
            update: 转换时更新的字段（可选）
            comment: 转换时添加的评论（可选）
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/transitions"
        payload: dict[str, Any] = {"transition": {"id": transition_id}}

        if fields:
            payload["fields"] = fields
        if update:
            payload["update"] = update
        if comment:
            if "update" not in payload:
                payload["update"] = {}
            payload["update"]["comment"] = [{"add": {"body": comment}}]

        response = await self.client.post(path, json=payload)
        response.raise_for_status()

    # ========== Comments ==========

    async def get_comments(
        self,
        issue_id_or_key: str,
        start_at: int = 0,
        max_results: int = 50,
        expand: Optional[str] = None,
    ) -> IssueComments:
        """
        获取 Issue 评论

        GET /rest/api/2/issue/{issueIdOrKey}/comment

        Args:
            issue_id_or_key: Issue ID 或 Key
            start_at: 起始位置
            max_results: 最大结果数
            expand: 展开的字段（可选），如 "renderedBody"

        Returns:
            IssueComments: 评论列表
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/comment"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return IssueComments.model_validate(data)

    async def add_comment(
        self,
        issue_id_or_key: str,
        body: str,
        visibility: Optional[dict] = None,
    ) -> IssueComment:
        """
        添加 Issue 评论

        POST /rest/api/2/issue/{issueIdOrKey}/comment

        Args:
            issue_id_or_key: Issue ID 或 Key
            body: 评论内容
            visibility: 可见性设置（可选），如 {"type": "role", "value": "Administrators"}

        Returns:
            IssueComment: 创建的评论
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/comment"
        payload: dict[str, Any] = {"body": body}
        if visibility:
            payload["visibility"] = visibility

        data = await self.client.post_json(path, data=payload)
        return IssueComment.model_validate(data)

    # ========== Subtasks ==========

    async def get_subtasks(self, issue_id_or_key: str) -> list[dict]:
        """
        获取 Issue 子任务

        GET /rest/api/2/issue/{issueIdOrKey}/subtask

        Args:
            issue_id_or_key: Issue ID 或 Key

        Returns:
            list[dict]: 子任务列表
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/subtask"
        return await self.client.get_json(path)

    async def create_subtask(
        self,
        parent_issue_key: str,
        summary: str,
        issue_type: str = "Sub-task",
        description: Optional[str] = None,
        assignee: Optional[str] = None,
        **extra_fields,
    ) -> CreateIssueResponse:
        """
        创建子任务

        POST /rest/api/2/issue

        Args:
            parent_issue_key: 父 Issue Key
            summary: 摘要
            issue_type: 子任务类型名称（默认 "Sub-task"）
            description: 描述（可选）
            assignee: 分配人用户名（可选）
            **extra_fields: 其他字段

        Returns:
            CreateIssueResponse: 创建结果
        """
        # 先获取父 Issue 的项目
        parent = await self.get_raw(parent_issue_key, fields=["project"])
        project_key = parent["fields"]["project"]["key"]

        fields: dict[str, Any] = {
            "project": {"key": project_key},
            "parent": {"key": parent_issue_key},
            "summary": summary,
            "issuetype": {"name": issue_type},
        }

        if description:
            fields["description"] = description
        if assignee:
            fields["assignee"] = {"name": assignee}

        fields.update(extra_fields)

        payload = {"fields": fields}
        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return CreateIssueResponse.model_validate(data)

    # ========== Attachments ==========

    async def add_attachment(
        self,
        issue_id_or_key: str,
        file_path: str,
        filename: Optional[str] = None,
    ) -> list[Attachment]:
        """
        上传附件到 Issue

        POST /rest/api/2/issue/{issueIdOrKey}/attachments

        Args:
            issue_id_or_key: Issue ID 或 Key
            file_path: 文件路径
            filename: 文件名（可选，默认使用文件原名）

        Returns:
            list[Attachment]: 上传的附件列表
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/attachments"
        file_path_obj = Path(file_path)

        if filename is None:
            filename = file_path_obj.name

        with open(file_path_obj, "rb") as f:
            files = {"file": (filename, f)}
            headers = {
                "X-Atlassian-Token": "no-check",
            }
            # 移除 Content-Type，让 httpx 自动设置 multipart/form-data
            auth_headers = self.client._get_auth_headers()
            auth_headers.pop("Content-Type", None)
            headers.update(auth_headers)

            response = await self.client._get_client().post(
                path,
                files=files,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

        return [Attachment.model_validate(a) for a in data]

    async def add_attachment_bytes(
        self,
        issue_id_or_key: str,
        content: bytes,
        filename: str,
    ) -> list[Attachment]:
        """
        上传字节内容作为附件

        Args:
            issue_id_or_key: Issue ID 或 Key
            content: 文件内容（字节）
            filename: 文件名

        Returns:
            list[Attachment]: 上传的附件列表
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/attachments"

        files = {"file": (filename, content)}
        headers = {
            "X-Atlassian-Token": "no-check",
        }
        auth_headers = self.client._get_auth_headers()
        auth_headers.pop("Content-Type", None)
        headers.update(auth_headers)

        response = await self.client._get_client().post(
            path,
            files=files,
            headers=headers,
        )
        response.raise_for_status()
        data = response.json()

        return [Attachment.model_validate(a) for a in data]
