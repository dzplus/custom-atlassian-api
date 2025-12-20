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
    Worklog,
    WorklogList,
    Watchers,
    Votes,
    RemoteLink,
    EditMeta,
    CreateMeta,
    IssuePickerResults,
)
from atlassian.jira.models.attachment import Attachment
from atlassian.jira.models.common import EntityProperty, EntityPropertyKeys


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

    # ==================== Worklog APIs ====================

    async def get_worklogs(
        self,
        issue_id_or_key: str,
        start_at: int = 0,
        max_results: int = 50,
    ) -> WorklogList:
        """
        获取Issue的工作日志列表

        GET /rest/api/2/issue/{issueIdOrKey}/worklog

        Args:
            issue_id_or_key: Issue ID 或 Key
            start_at: 起始位置
            max_results: 最大结果数

        Returns:
            WorklogList: 工作日志列表
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/worklog"
        params = {"startAt": start_at, "maxResults": max_results}
        data = await self.client.get_json(path, params=params)
        return WorklogList.model_validate(data)

    async def get_worklogs_raw(
        self,
        issue_id_or_key: str,
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict:
        """获取工作日志列表（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/worklog"
        params = {"startAt": start_at, "maxResults": max_results}
        return await self.client.get_json(path, params=params)

    async def add_worklog(
        self,
        issue_id_or_key: str,
        time_spent: str,
        comment: Optional[str] = None,
        started: Optional[str] = None,
        visibility: Optional[dict] = None,
    ) -> Worklog:
        """
        添加工作日志

        POST /rest/api/2/issue/{issueIdOrKey}/worklog

        Args:
            issue_id_or_key: Issue ID 或 Key
            time_spent: 花费时间（如 "1h 30m", "2d"）
            comment: 评论内容（可选）
            started: 开始时间（ISO 8601格式，可选）
            visibility: 可见性设置（可选）

        Returns:
            Worklog: 创建的工作日志
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/worklog"
        payload: dict[str, Any] = {"timeSpent": time_spent}
        if comment:
            payload["comment"] = comment
        if started:
            payload["started"] = started
        if visibility:
            payload["visibility"] = visibility
        data = await self.client.post_json(path, data=payload)
        return Worklog.model_validate(data)

    async def add_worklog_raw(
        self,
        issue_id_or_key: str,
        time_spent: str,
        comment: Optional[str] = None,
        started: Optional[str] = None,
        visibility: Optional[dict] = None,
    ) -> dict:
        """添加工作日志（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/worklog"
        payload: dict[str, Any] = {"timeSpent": time_spent}
        if comment:
            payload["comment"] = comment
        if started:
            payload["started"] = started
        if visibility:
            payload["visibility"] = visibility
        return await self.client.post_json(path, data=payload)

    async def get_worklog(
        self,
        issue_id_or_key: str,
        worklog_id: str,
    ) -> Worklog:
        """
        获取单个工作日志

        GET /rest/api/2/issue/{issueIdOrKey}/worklog/{id}

        Args:
            issue_id_or_key: Issue ID 或 Key
            worklog_id: 工作日志ID

        Returns:
            Worklog: 工作日志详情
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/worklog/{worklog_id}"
        data = await self.client.get_json(path)
        return Worklog.model_validate(data)

    async def get_worklog_raw(
        self,
        issue_id_or_key: str,
        worklog_id: str,
    ) -> dict:
        """获取单个工作日志（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/worklog/{worklog_id}"
        return await self.client.get_json(path)

    async def update_worklog(
        self,
        issue_id_or_key: str,
        worklog_id: str,
        time_spent: Optional[str] = None,
        comment: Optional[str] = None,
        started: Optional[str] = None,
        visibility: Optional[dict] = None,
    ) -> Worklog:
        """
        更新工作日志

        PUT /rest/api/2/issue/{issueIdOrKey}/worklog/{id}

        Args:
            issue_id_or_key: Issue ID 或 Key
            worklog_id: 工作日志ID
            time_spent: 花费时间（可选）
            comment: 评论内容（可选）
            started: 开始时间（可选）
            visibility: 可见性设置（可选）

        Returns:
            Worklog: 更新后的工作日志
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/worklog/{worklog_id}"
        payload: dict[str, Any] = {}
        if time_spent:
            payload["timeSpent"] = time_spent
        if comment:
            payload["comment"] = comment
        if started:
            payload["started"] = started
        if visibility:
            payload["visibility"] = visibility
        data = await self.client.put_json(path, data=payload)
        return Worklog.model_validate(data)

    async def update_worklog_raw(
        self,
        issue_id_or_key: str,
        worklog_id: str,
        time_spent: Optional[str] = None,
        comment: Optional[str] = None,
        started: Optional[str] = None,
        visibility: Optional[dict] = None,
    ) -> dict:
        """更新工作日志（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/worklog/{worklog_id}"
        payload: dict[str, Any] = {}
        if time_spent:
            payload["timeSpent"] = time_spent
        if comment:
            payload["comment"] = comment
        if started:
            payload["started"] = started
        if visibility:
            payload["visibility"] = visibility
        return await self.client.put_json(path, data=payload)

    async def delete_worklog(
        self,
        issue_id_or_key: str,
        worklog_id: str,
    ) -> None:
        """
        删除工作日志

        DELETE /rest/api/2/issue/{issueIdOrKey}/worklog/{id}

        Args:
            issue_id_or_key: Issue ID 或 Key
            worklog_id: 工作日志ID
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/worklog/{worklog_id}"
        await self.client.delete(path)

    # ==================== Watchers APIs ====================

    async def get_watchers(
        self,
        issue_id_or_key: str,
    ) -> Watchers:
        """
        获取Issue的监视者

        GET /rest/api/2/issue/{issueIdOrKey}/watchers

        Args:
            issue_id_or_key: Issue ID 或 Key

        Returns:
            Watchers: 监视者信息
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/watchers"
        data = await self.client.get_json(path)
        return Watchers.model_validate(data)

    async def get_watchers_raw(
        self,
        issue_id_or_key: str,
    ) -> dict:
        """获取监视者（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/watchers"
        return await self.client.get_json(path)

    async def add_watcher(
        self,
        issue_id_or_key: str,
        username: str,
    ) -> None:
        """
        添加监视者

        POST /rest/api/2/issue/{issueIdOrKey}/watchers

        Args:
            issue_id_or_key: Issue ID 或 Key
            username: 用户名
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/watchers"
        # Jira API expects username as JSON string (quoted string)
        await self.client.post_json(path, data=username)

    async def remove_watcher(
        self,
        issue_id_or_key: str,
        username: str,
    ) -> None:
        """
        移除监视者

        DELETE /rest/api/2/issue/{issueIdOrKey}/watchers

        Args:
            issue_id_or_key: Issue ID 或 Key
            username: 用户名
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/watchers"
        params = {"username": username}
        await self.client.delete(path, params=params)

    # ==================== Votes APIs ====================

    async def get_votes(
        self,
        issue_id_or_key: str,
    ) -> Votes:
        """
        获取Issue的投票信息

        GET /rest/api/2/issue/{issueIdOrKey}/votes

        Args:
            issue_id_or_key: Issue ID 或 Key

        Returns:
            Votes: 投票信息
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/votes"
        data = await self.client.get_json(path)
        return Votes.model_validate(data)

    async def get_votes_raw(
        self,
        issue_id_or_key: str,
    ) -> dict:
        """获取投票信息（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/votes"
        return await self.client.get_json(path)

    async def add_vote(
        self,
        issue_id_or_key: str,
    ) -> None:
        """
        为Issue投票

        POST /rest/api/2/issue/{issueIdOrKey}/votes

        Args:
            issue_id_or_key: Issue ID 或 Key
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/votes"
        await self.client.post_json(path, data=None)

    async def remove_vote(
        self,
        issue_id_or_key: str,
    ) -> None:
        """
        移除投票

        DELETE /rest/api/2/issue/{issueIdOrKey}/votes

        Args:
            issue_id_or_key: Issue ID 或 Key
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/votes"
        await self.client.delete(path)

    # ==================== Remote Links APIs ====================

    async def get_remote_links(
        self,
        issue_id_or_key: str,
        global_id: Optional[str] = None,
    ) -> list[RemoteLink]:
        """
        获取Issue的远程链接列表

        GET /rest/api/2/issue/{issueIdOrKey}/remotelink

        Args:
            issue_id_or_key: Issue ID 或 Key
            global_id: 全局ID（可选，用于过滤）

        Returns:
            list[RemoteLink]: 远程链接列表
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/remotelink"
        params = {}
        if global_id:
            params["globalId"] = global_id
        data = await self.client.get_json(path, params=params)
        return [RemoteLink.model_validate(link) for link in data]

    async def get_remote_links_raw(
        self,
        issue_id_or_key: str,
        global_id: Optional[str] = None,
    ) -> list[dict]:
        """获取远程链接列表（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/remotelink"
        params = {}
        if global_id:
            params["globalId"] = global_id
        return await self.client.get_json(path, params=params)

    async def create_or_update_remote_link(
        self,
        issue_id_or_key: str,
        url: str,
        title: str,
        summary: Optional[str] = None,
        global_id: Optional[str] = None,
        relationship: Optional[str] = None,
    ) -> dict:
        """
        创建或更新远程链接

        POST /rest/api/2/issue/{issueIdOrKey}/remotelink

        Args:
            issue_id_or_key: Issue ID 或 Key
            url: 远程链接URL
            title: 链接标题
            summary: 链接摘要（可选）
            global_id: 全局ID（可选）
            relationship: 关系类型（可选）

        Returns:
            dict: 创建结果
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/remotelink"
        payload: dict[str, Any] = {
            "object": {
                "url": url,
                "title": title,
            }
        }
        if summary:
            payload["object"]["summary"] = summary
        if global_id:
            payload["globalId"] = global_id
        if relationship:
            payload["relationship"] = relationship
        return await self.client.post_json(path, data=payload)

    async def get_remote_link(
        self,
        issue_id_or_key: str,
        link_id: str,
    ) -> RemoteLink:
        """
        按ID获取远程链接

        GET /rest/api/2/issue/{issueIdOrKey}/remotelink/{linkId}

        Args:
            issue_id_or_key: Issue ID 或 Key
            link_id: 链接ID

        Returns:
            RemoteLink: 远程链接详情
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/remotelink/{link_id}"
        data = await self.client.get_json(path)
        return RemoteLink.model_validate(data)

    async def get_remote_link_raw(
        self,
        issue_id_or_key: str,
        link_id: str,
    ) -> dict:
        """按ID获取远程链接（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/remotelink/{link_id}"
        return await self.client.get_json(path)

    async def update_remote_link(
        self,
        issue_id_or_key: str,
        link_id: str,
        url: Optional[str] = None,
        title: Optional[str] = None,
        summary: Optional[str] = None,
        relationship: Optional[str] = None,
    ) -> None:
        """
        更新远程链接

        PUT /rest/api/2/issue/{issueIdOrKey}/remotelink/{linkId}

        Args:
            issue_id_or_key: Issue ID 或 Key
            link_id: 链接ID
            url: 远程链接URL（可选）
            title: 链接标题（可选）
            summary: 链接摘要（可选）
            relationship: 关系类型（可选）
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/remotelink/{link_id}"
        payload: dict[str, Any] = {"object": {}}
        if url:
            payload["object"]["url"] = url
        if title:
            payload["object"]["title"] = title
        if summary:
            payload["object"]["summary"] = summary
        if relationship:
            payload["relationship"] = relationship
        await self.client.put_json(path, data=payload)

    async def delete_remote_link_by_id(
        self,
        issue_id_or_key: str,
        link_id: str,
    ) -> None:
        """
        按ID删除远程链接

        DELETE /rest/api/2/issue/{issueIdOrKey}/remotelink/{linkId}

        Args:
            issue_id_or_key: Issue ID 或 Key
            link_id: 链接ID
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/remotelink/{link_id}"
        await self.client.delete(path)

    async def delete_remote_link_by_global_id(
        self,
        issue_id_or_key: str,
        global_id: str,
    ) -> None:
        """
        按全局ID删除远程链接

        DELETE /rest/api/2/issue/{issueIdOrKey}/remotelink

        Args:
            issue_id_or_key: Issue ID 或 Key
            global_id: 全局ID
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/remotelink"
        params = {"globalId": global_id}
        await self.client.delete(path, params=params)

    # ==================== Comment Management APIs ====================

    async def get_comment(
        self,
        issue_id_or_key: str,
        comment_id: str,
        expand: Optional[str] = None,
    ) -> IssueComment:
        """
        获取单个评论

        GET /rest/api/2/issue/{issueIdOrKey}/comment/{id}

        Args:
            issue_id_or_key: Issue ID 或 Key
            comment_id: 评论ID
            expand: 扩展字段（可选）

        Returns:
            IssueComment: 评论详情
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/comment/{comment_id}"
        params = {}
        if expand:
            params["expand"] = expand
        data = await self.client.get_json(path, params=params)
        return IssueComment.model_validate(data)

    async def get_comment_raw(
        self,
        issue_id_or_key: str,
        comment_id: str,
        expand: Optional[str] = None,
    ) -> dict:
        """获取单个评论（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/comment/{comment_id}"
        params = {}
        if expand:
            params["expand"] = expand
        return await self.client.get_json(path, params=params)

    async def update_comment(
        self,
        issue_id_or_key: str,
        comment_id: str,
        body: str,
        visibility: Optional[dict] = None,
    ) -> IssueComment:
        """
        更新评论

        PUT /rest/api/2/issue/{issueIdOrKey}/comment/{id}

        Args:
            issue_id_or_key: Issue ID 或 Key
            comment_id: 评论ID
            body: 评论内容
            visibility: 可见性设置（可选）

        Returns:
            IssueComment: 更新后的评论
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/comment/{comment_id}"
        payload: dict[str, Any] = {"body": body}
        if visibility:
            payload["visibility"] = visibility
        data = await self.client.put_json(path, data=payload)
        return IssueComment.model_validate(data)

    async def update_comment_raw(
        self,
        issue_id_or_key: str,
        comment_id: str,
        body: str,
        visibility: Optional[dict] = None,
    ) -> dict:
        """更新评论（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/comment/{comment_id}"
        payload: dict[str, Any] = {"body": body}
        if visibility:
            payload["visibility"] = visibility
        return await self.client.put_json(path, data=payload)

    async def delete_comment(
        self,
        issue_id_or_key: str,
        comment_id: str,
    ) -> None:
        """
        删除评论

        DELETE /rest/api/2/issue/{issueIdOrKey}/comment/{id}

        Args:
            issue_id_or_key: Issue ID 或 Key
            comment_id: 评论ID
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/comment/{comment_id}"
        await self.client.delete(path)

    # ==================== Properties APIs ====================

    async def get_property_keys(
        self,
        issue_id_or_key: str,
    ) -> EntityPropertyKeys:
        """
        获取Issue的属性键列表

        GET /rest/api/2/issue/{issueIdOrKey}/properties

        Args:
            issue_id_or_key: Issue ID 或 Key

        Returns:
            EntityPropertyKeys: 属性键列表
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/properties"
        data = await self.client.get_json(path)
        return EntityPropertyKeys.model_validate(data)

    async def get_property_keys_raw(
        self,
        issue_id_or_key: str,
    ) -> dict:
        """获取属性键列表（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/properties"
        return await self.client.get_json(path)

    async def get_property(
        self,
        issue_id_or_key: str,
        property_key: str,
    ) -> EntityProperty:
        """
        获取Issue的单个属性

        GET /rest/api/2/issue/{issueIdOrKey}/properties/{propertyKey}

        Args:
            issue_id_or_key: Issue ID 或 Key
            property_key: 属性键

        Returns:
            EntityProperty: 属性详情
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/properties/{property_key}"
        data = await self.client.get_json(path)
        return EntityProperty.model_validate(data)

    async def get_property_raw(
        self,
        issue_id_or_key: str,
        property_key: str,
    ) -> dict:
        """获取属性（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/properties/{property_key}"
        return await self.client.get_json(path)

    async def set_property(
        self,
        issue_id_or_key: str,
        property_key: str,
        value: Any,
    ) -> None:
        """
        设置Issue的属性

        PUT /rest/api/2/issue/{issueIdOrKey}/properties/{propertyKey}

        Args:
            issue_id_or_key: Issue ID 或 Key
            property_key: 属性键
            value: 属性值
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/properties/{property_key}"
        await self.client.put_json(path, data=value)

    async def delete_property(
        self,
        issue_id_or_key: str,
        property_key: str,
    ) -> None:
        """
        删除Issue的属性

        DELETE /rest/api/2/issue/{issueIdOrKey}/properties/{propertyKey}

        Args:
            issue_id_or_key: Issue ID 或 Key
            property_key: 属性键
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/properties/{property_key}"
        await self.client.delete(path)

    # ==================== Meta & Operations APIs ====================

    async def get_edit_meta(
        self,
        issue_id_or_key: str,
    ) -> EditMeta:
        """
        获取Issue编辑元数据

        GET /rest/api/2/issue/{issueIdOrKey}/editmeta

        Args:
            issue_id_or_key: Issue ID 或 Key

        Returns:
            EditMeta: 编辑元数据
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/editmeta"
        data = await self.client.get_json(path)
        return EditMeta.model_validate(data)

    async def get_edit_meta_raw(
        self,
        issue_id_or_key: str,
    ) -> dict:
        """获取编辑元数据（原始JSON）"""
        path = f"{self.BASE_PATH}/{issue_id_or_key}/editmeta"
        return await self.client.get_json(path)

    async def notify(
        self,
        issue_id_or_key: str,
        subject: str,
        text_body: str,
        html_body: Optional[str] = None,
        to_reporter: bool = False,
        to_assignee: bool = False,
        to_watchers: bool = False,
        to_voters: bool = False,
        to_users: Optional[list[dict]] = None,
        to_groups: Optional[list[dict]] = None,
    ) -> None:
        """
        发送Issue通知

        POST /rest/api/2/issue/{issueIdOrKey}/notify

        Args:
            issue_id_or_key: Issue ID 或 Key
            subject: 通知主题
            text_body: 纯文本内容
            html_body: HTML内容（可选）
            to_reporter: 发送给报告人
            to_assignee: 发送给经办人
            to_watchers: 发送给监视者
            to_voters: 发送给投票者
            to_users: 用户列表（可选）
            to_groups: 用户组列表（可选）
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/notify"
        payload: dict[str, Any] = {
            "subject": subject,
            "textBody": text_body,
            "to": {
                "reporter": to_reporter,
                "assignee": to_assignee,
                "watchers": to_watchers,
                "voters": to_voters,
            }
        }
        if html_body:
            payload["htmlBody"] = html_body
        if to_users:
            payload["to"]["users"] = to_users
        if to_groups:
            payload["to"]["groups"] = to_groups
        await self.client.post_json(path, data=payload)

    async def archive_issue(
        self,
        issue_id_or_key: str,
    ) -> None:
        """
        归档Issue

        PUT /rest/api/2/issue/{issueIdOrKey}/archive

        Args:
            issue_id_or_key: Issue ID 或 Key
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/archive"
        await self.client.put_json(path, data=None)

    async def restore_issue(
        self,
        issue_id_or_key: str,
    ) -> None:
        """
        恢复已归档的Issue

        PUT /rest/api/2/issue/{issueIdOrKey}/restore

        Args:
            issue_id_or_key: Issue ID 或 Key
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/restore"
        await self.client.put_json(path, data=None)

    async def get_create_meta(
        self,
        project_ids: Optional[list[str]] = None,
        project_keys: Optional[list[str]] = None,
        issue_type_ids: Optional[list[str]] = None,
        issue_type_names: Optional[list[str]] = None,
        expand: Optional[str] = None,
    ) -> CreateMeta:
        """
        获取创建Issue元数据

        GET /rest/api/2/issue/createmeta

        Args:
            project_ids: 项目ID列表（可选）
            project_keys: 项目Key列表（可选）
            issue_type_ids: Issue类型ID列表（可选）
            issue_type_names: Issue类型名称列表（可选）
            expand: 扩展字段（可选）

        Returns:
            CreateMeta: 创建元数据
        """
        path = f"{self.BASE_PATH}/createmeta"
        params: dict[str, Any] = {}
        if project_ids:
            params["projectIds"] = ",".join(project_ids)
        if project_keys:
            params["projectKeys"] = ",".join(project_keys)
        if issue_type_ids:
            params["issuetypeIds"] = ",".join(issue_type_ids)
        if issue_type_names:
            params["issuetypeNames"] = ",".join(issue_type_names)
        if expand:
            params["expand"] = expand
        data = await self.client.get_json(path, params=params)
        return CreateMeta.model_validate(data)

    async def get_create_meta_raw(
        self,
        project_ids: Optional[list[str]] = None,
        project_keys: Optional[list[str]] = None,
        issue_type_ids: Optional[list[str]] = None,
        issue_type_names: Optional[list[str]] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """获取创建元数据（原始JSON）"""
        path = f"{self.BASE_PATH}/createmeta"
        params: dict[str, Any] = {}
        if project_ids:
            params["projectIds"] = ",".join(project_ids)
        if project_keys:
            params["projectKeys"] = ",".join(project_keys)
        if issue_type_ids:
            params["issuetypeIds"] = ",".join(issue_type_ids)
        if issue_type_names:
            params["issuetypeNames"] = ",".join(issue_type_names)
        if expand:
            params["expand"] = expand
        return await self.client.get_json(path, params=params)

    async def get_create_meta_project_issue_types(
        self,
        project_id_or_key: str,
    ) -> dict:
        """
        获取项目的创建元数据Issue类型

        GET /rest/api/2/issue/createmeta/{projectIdOrKey}/issuetypes

        Args:
            project_id_or_key: 项目ID或Key

        Returns:
            dict: Issue类型列表
        """
        path = f"{self.BASE_PATH}/createmeta/{project_id_or_key}/issuetypes"
        return await self.client.get_json(path)

    async def get_create_meta_fields(
        self,
        project_id_or_key: str,
        issue_type_id: str,
    ) -> dict:
        """
        获取创建元数据字段

        GET /rest/api/2/issue/createmeta/{projectIdOrKey}/issuetypes/{issueTypeId}

        Args:
            project_id_or_key: 项目ID或Key
            issue_type_id: Issue类型ID

        Returns:
            dict: 字段元数据
        """
        path = f"{self.BASE_PATH}/createmeta/{project_id_or_key}/issuetypes/{issue_type_id}"
        return await self.client.get_json(path)

    # ==================== Issue Picker, Subtasks & Bulk Archive ====================

    async def get_issue_picker(
        self,
        query: Optional[str] = None,
        current_jql: Optional[str] = None,
        current_issue_key: Optional[str] = None,
        current_project_id: Optional[str] = None,
        show_sub_tasks: bool = False,
        show_sub_task_parent: bool = False,
    ) -> IssuePickerResults:
        """
        获取Issue选择器资源

        GET /rest/api/2/issue/picker

        Args:
            query: 查询字符串（可选）
            current_jql: 当前JQL（可选）
            current_issue_key: 当前Issue Key（可选）
            current_project_id: 当前项目ID（可选）
            show_sub_tasks: 是否显示子任务
            show_sub_task_parent: 是否显示子任务的父任务

        Returns:
            IssuePickerResults: 选择器结果
        """
        path = f"{self.BASE_PATH}/picker"
        params: dict[str, Any] = {
            "showSubTasks": str(show_sub_tasks).lower(),
            "showSubTaskParent": str(show_sub_task_parent).lower(),
        }
        if query:
            params["query"] = query
        if current_jql:
            params["currentJQL"] = current_jql
        if current_issue_key:
            params["currentIssueKey"] = current_issue_key
        if current_project_id:
            params["currentProjectId"] = current_project_id
        data = await self.client.get_json(path, params=params)
        return IssuePickerResults.model_validate(data)

    async def get_issue_picker_raw(
        self,
        query: Optional[str] = None,
        current_jql: Optional[str] = None,
        current_issue_key: Optional[str] = None,
        current_project_id: Optional[str] = None,
        show_sub_tasks: bool = False,
        show_sub_task_parent: bool = False,
    ) -> dict:
        """获取Issue选择器资源（原始JSON）"""
        path = f"{self.BASE_PATH}/picker"
        params: dict[str, Any] = {
            "showSubTasks": str(show_sub_tasks).lower(),
            "showSubTaskParent": str(show_sub_task_parent).lower(),
        }
        if query:
            params["query"] = query
        if current_jql:
            params["currentJQL"] = current_jql
        if current_issue_key:
            params["currentIssueKey"] = current_issue_key
        if current_project_id:
            params["currentProjectId"] = current_project_id
        return await self.client.get_json(path, params=params)

    async def move_subtasks(
        self,
        issue_id_or_key: str,
        new_parent_issue_key: str,
    ) -> None:
        """
        移动子任务到新的父Issue

        POST /rest/api/2/issue/{issueIdOrKey}/subtask/move

        Args:
            issue_id_or_key: Issue ID 或 Key
            new_parent_issue_key: 新父Issue的Key
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/subtask/move"
        payload = {"issueKey": new_parent_issue_key}
        await self.client.post_json(path, data=payload)

    async def can_move_subtask(
        self,
        issue_id_or_key: str,
    ) -> dict:
        """
        检查是否可以移动子任务

        GET /rest/api/2/issue/{issueIdOrKey}/subtask/move

        Args:
            issue_id_or_key: Issue ID 或 Key

        Returns:
            dict: 检查结果
        """
        path = f"{self.BASE_PATH}/{issue_id_or_key}/subtask/move"
        return await self.client.get_json(path)

    async def archive_issues(
        self,
        jql: str,
    ) -> dict:
        """
        批量归档Issues

        POST /rest/api/2/issue/archive

        Args:
            jql: JQL查询语句

        Returns:
            dict: 归档结果
        """
        path = f"{self.BASE_PATH}/archive"
        payload = {"jql": jql}
        return await self.client.post_json(path, data=payload)
