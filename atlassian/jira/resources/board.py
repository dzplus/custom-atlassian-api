"""
Board Resource - 敏捷看板 API

GET    /rest/agile/1.0/board                              - 获取所有看板
POST   /rest/agile/1.0/board                              - 创建看板
GET    /rest/agile/1.0/board/{boardId}                    - 获取看板详情
DELETE /rest/agile/1.0/board/{boardId}                    - 删除看板
GET    /rest/agile/1.0/board/{boardId}/configuration      - 获取看板配置
GET    /rest/agile/1.0/board/{boardId}/backlog            - 获取看板 Backlog
GET    /rest/agile/1.0/board/{boardId}/issue              - 获取看板 Issue
GET    /rest/agile/1.0/board/{boardId}/sprint             - 获取看板 Sprint
GET    /rest/agile/1.0/board/{boardId}/epic               - 获取看板 Epic
GET    /rest/agile/1.0/board/{boardId}/project            - 获取看板关联项目
GET    /rest/agile/1.0/board/{boardId}/version            - 获取看板版本
GET    /rest/agile/1.0/board/{boardId}/quickfilter        - 获取快速过滤器
"""

from typing import Any, Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.agile import (
    Board,
    BoardList,
    BoardConfiguration,
    Sprint,
    SprintList,
    Epic,
    EpicList,
    AgileIssueList,
    QuickFilterList,
)


class BoardResource(BaseResource):
    """
    敏捷看板资源

    API: /rest/agile/1.0/board
    """

    BASE_PATH = "/rest/agile/1.0/board"

    # ==================== Board CRUD ====================

    async def get_all(
        self,
        start_at: int = 0,
        max_results: int = 50,
        board_type: Optional[str] = None,
        name: Optional[str] = None,
        project_key_or_id: Optional[str] = None,
        account_id_location: Optional[str] = None,
        project_location: Optional[str] = None,
        include_private: Optional[bool] = None,
        negation_type: Optional[str] = None,
        order_by: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> BoardList:
        """
        获取所有看板

        GET /rest/agile/1.0/board

        Args:
            start_at: 起始位置
            max_results: 最大返回数量
            board_type: 看板类型 (scrum, kanban)
            name: 看板名称（模糊匹配）
            project_key_or_id: 项目 Key 或 ID
            account_id_location: 账户 ID 位置
            project_location: 项目位置
            include_private: 是否包含私有看板
            negation_type: 否定类型
            order_by: 排序字段
            expand: 展开字段

        Returns:
            BoardList: 看板列表
        """
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if board_type:
            params["type"] = board_type
        if name:
            params["name"] = name
        if project_key_or_id:
            params["projectKeyOrId"] = project_key_or_id
        if account_id_location:
            params["accountIdLocation"] = account_id_location
        if project_location:
            params["projectLocation"] = project_location
        if include_private is not None:
            params["includePrivate"] = include_private
        if negation_type:
            params["negationType"] = negation_type
        if order_by:
            params["orderBy"] = order_by
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(self.BASE_PATH, params=params)
        return BoardList.model_validate(data)

    async def get_all_raw(
        self,
        start_at: int = 0,
        max_results: int = 50,
        board_type: Optional[str] = None,
        name: Optional[str] = None,
        project_key_or_id: Optional[str] = None,
    ) -> dict:
        """获取所有看板（原始 JSON）"""
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if board_type:
            params["type"] = board_type
        if name:
            params["name"] = name
        if project_key_or_id:
            params["projectKeyOrId"] = project_key_or_id

        return await self.client.get_json(self.BASE_PATH, params=params)

    async def get(self, board_id: int) -> Board:
        """
        获取看板详情

        GET /rest/agile/1.0/board/{boardId}

        Args:
            board_id: 看板 ID

        Returns:
            Board: 看板信息
        """
        path = f"{self.BASE_PATH}/{board_id}"
        data = await self.client.get_json(path)
        return Board.model_validate(data)

    async def get_raw(self, board_id: int) -> dict:
        """获取看板详情（原始 JSON）"""
        path = f"{self.BASE_PATH}/{board_id}"
        return await self.client.get_json(path)

    async def create(
        self,
        name: str,
        board_type: str,
        filter_id: int,
        location: Optional[dict] = None,
    ) -> Board:
        """
        创建看板

        POST /rest/agile/1.0/board

        Args:
            name: 看板名称（最多255字符）
            board_type: 看板类型 (scrum, kanban)
            filter_id: 过滤器 ID
            location: 位置信息（可选）

        Returns:
            Board: 创建的看板
        """
        payload: dict[str, Any] = {
            "name": name,
            "type": board_type,
            "filterId": filter_id,
        }
        if location:
            payload["location"] = location

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return Board.model_validate(data)

    async def create_raw(
        self,
        name: str,
        board_type: str,
        filter_id: int,
        location: Optional[dict] = None,
    ) -> dict:
        """创建看板（原始 JSON）"""
        payload: dict[str, Any] = {
            "name": name,
            "type": board_type,
            "filterId": filter_id,
        }
        if location:
            payload["location"] = location

        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def delete(self, board_id: int) -> None:
        """
        删除看板

        DELETE /rest/agile/1.0/board/{boardId}

        Args:
            board_id: 看板 ID
        """
        path = f"{self.BASE_PATH}/{board_id}"
        await self.client.delete(path)

    # ==================== Board Configuration ====================

    async def get_configuration(self, board_id: int) -> BoardConfiguration:
        """
        获取看板配置

        GET /rest/agile/1.0/board/{boardId}/configuration

        Args:
            board_id: 看板 ID

        Returns:
            BoardConfiguration: 看板配置
        """
        path = f"{self.BASE_PATH}/{board_id}/configuration"
        data = await self.client.get_json(path)
        return BoardConfiguration.model_validate(data)

    async def get_configuration_raw(self, board_id: int) -> dict:
        """获取看板配置（原始 JSON）"""
        path = f"{self.BASE_PATH}/{board_id}/configuration"
        return await self.client.get_json(path)

    # ==================== Board Issues ====================

    async def get_issues(
        self,
        board_id: int,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        validate_query: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> AgileIssueList:
        """
        获取看板中的所有 Issue

        GET /rest/agile/1.0/board/{boardId}/issue

        Args:
            board_id: 看板 ID
            start_at: 起始位置
            max_results: 最大返回数量
            jql: JQL 过滤条件
            validate_query: 是否验证 JQL
            fields: 返回的字段
            expand: 展开字段

        Returns:
            AgileIssueList: Issue 列表
        """
        path = f"{self.BASE_PATH}/{board_id}/issue"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if jql:
            params["jql"] = jql
        if validate_query is not None:
            params["validateQuery"] = validate_query
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return AgileIssueList.model_validate(data)

    async def get_issues_raw(
        self,
        board_id: int,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """获取看板 Issue（原始 JSON）"""
        path = f"{self.BASE_PATH}/{board_id}/issue"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if jql:
            params["jql"] = jql
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    # ==================== Board Backlog ====================

    async def get_backlog(
        self,
        board_id: int,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        validate_query: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> AgileIssueList:
        """
        获取看板 Backlog 中的 Issue

        GET /rest/agile/1.0/board/{boardId}/backlog

        返回未分配到任何 Sprint 的 Issue

        Args:
            board_id: 看板 ID
            start_at: 起始位置
            max_results: 最大返回数量
            jql: JQL 过滤条件
            validate_query: 是否验证 JQL
            fields: 返回的字段
            expand: 展开字段

        Returns:
            AgileIssueList: Backlog Issue 列表
        """
        path = f"{self.BASE_PATH}/{board_id}/backlog"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if jql:
            params["jql"] = jql
        if validate_query is not None:
            params["validateQuery"] = validate_query
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return AgileIssueList.model_validate(data)

    async def get_backlog_raw(
        self,
        board_id: int,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """获取看板 Backlog（原始 JSON）"""
        path = f"{self.BASE_PATH}/{board_id}/backlog"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if jql:
            params["jql"] = jql
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    # ==================== Board Sprints ====================

    async def get_sprints(
        self,
        board_id: int,
        start_at: int = 0,
        max_results: int = 50,
        state: Optional[str] = None,
    ) -> SprintList:
        """
        获取看板的 Sprint 列表

        GET /rest/agile/1.0/board/{boardId}/sprint

        Args:
            board_id: 看板 ID
            start_at: 起始位置
            max_results: 最大返回数量
            state: Sprint 状态过滤 (future, active, closed)

        Returns:
            SprintList: Sprint 列表
        """
        path = f"{self.BASE_PATH}/{board_id}/sprint"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if state:
            params["state"] = state

        data = await self.client.get_json(path, params=params)
        return SprintList.model_validate(data)

    async def get_sprints_raw(
        self,
        board_id: int,
        start_at: int = 0,
        max_results: int = 50,
        state: Optional[str] = None,
    ) -> dict:
        """获取看板 Sprint（原始 JSON）"""
        path = f"{self.BASE_PATH}/{board_id}/sprint"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if state:
            params["state"] = state

        return await self.client.get_json(path, params=params)

    async def get_sprint_issues(
        self,
        board_id: int,
        sprint_id: int,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        validate_query: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> AgileIssueList:
        """
        获取看板中某个 Sprint 的 Issue

        GET /rest/agile/1.0/board/{boardId}/sprint/{sprintId}/issue

        Args:
            board_id: 看板 ID
            sprint_id: Sprint ID
            start_at: 起始位置
            max_results: 最大返回数量
            jql: JQL 过滤条件
            validate_query: 是否验证 JQL
            fields: 返回的字段
            expand: 展开字段

        Returns:
            AgileIssueList: Sprint Issue 列表
        """
        path = f"{self.BASE_PATH}/{board_id}/sprint/{sprint_id}/issue"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if jql:
            params["jql"] = jql
        if validate_query is not None:
            params["validateQuery"] = validate_query
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return AgileIssueList.model_validate(data)

    async def get_sprint_issues_raw(
        self,
        board_id: int,
        sprint_id: int,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """获取看板 Sprint Issue（原始 JSON）"""
        path = f"{self.BASE_PATH}/{board_id}/sprint/{sprint_id}/issue"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if jql:
            params["jql"] = jql
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    # ==================== Board Epics ====================

    async def get_epics(
        self,
        board_id: int,
        start_at: int = 0,
        max_results: int = 50,
        done: Optional[bool] = None,
    ) -> EpicList:
        """
        获取看板的 Epic 列表

        GET /rest/agile/1.0/board/{boardId}/epic

        Args:
            board_id: 看板 ID
            start_at: 起始位置
            max_results: 最大返回数量
            done: 是否已完成

        Returns:
            EpicList: Epic 列表
        """
        path = f"{self.BASE_PATH}/{board_id}/epic"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if done is not None:
            params["done"] = done

        data = await self.client.get_json(path, params=params)
        return EpicList.model_validate(data)

    async def get_epics_raw(
        self,
        board_id: int,
        start_at: int = 0,
        max_results: int = 50,
        done: Optional[bool] = None,
    ) -> dict:
        """获取看板 Epic（原始 JSON）"""
        path = f"{self.BASE_PATH}/{board_id}/epic"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if done is not None:
            params["done"] = done

        return await self.client.get_json(path, params=params)

    async def get_epic_issues(
        self,
        board_id: int,
        epic_id: int,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        validate_query: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> AgileIssueList:
        """
        获取看板中某个 Epic 的 Issue

        GET /rest/agile/1.0/board/{boardId}/epic/{epicId}/issue

        Args:
            board_id: 看板 ID
            epic_id: Epic ID
            start_at: 起始位置
            max_results: 最大返回数量
            jql: JQL 过滤条件
            validate_query: 是否验证 JQL
            fields: 返回的字段
            expand: 展开字段

        Returns:
            AgileIssueList: Epic Issue 列表
        """
        path = f"{self.BASE_PATH}/{board_id}/epic/{epic_id}/issue"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if jql:
            params["jql"] = jql
        if validate_query is not None:
            params["validateQuery"] = validate_query
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return AgileIssueList.model_validate(data)

    async def get_epic_issues_raw(
        self,
        board_id: int,
        epic_id: int,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """获取看板 Epic Issue（原始 JSON）"""
        path = f"{self.BASE_PATH}/{board_id}/epic/{epic_id}/issue"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if jql:
            params["jql"] = jql
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    async def get_issues_without_epic(
        self,
        board_id: int,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        validate_query: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> AgileIssueList:
        """
        获取看板中没有 Epic 的 Issue

        GET /rest/agile/1.0/board/{boardId}/epic/none/issue

        Args:
            board_id: 看板 ID
            start_at: 起始位置
            max_results: 最大返回数量
            jql: JQL 过滤条件
            validate_query: 是否验证 JQL
            fields: 返回的字段
            expand: 展开字段

        Returns:
            AgileIssueList: 无 Epic 的 Issue 列表
        """
        path = f"{self.BASE_PATH}/{board_id}/epic/none/issue"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if jql:
            params["jql"] = jql
        if validate_query is not None:
            params["validateQuery"] = validate_query
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return AgileIssueList.model_validate(data)

    async def get_issues_without_epic_raw(
        self,
        board_id: int,
        start_at: int = 0,
        max_results: int = 50,
        jql: Optional[str] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """获取看板无 Epic 的 Issue（原始 JSON）"""
        path = f"{self.BASE_PATH}/{board_id}/epic/none/issue"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if jql:
            params["jql"] = jql
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    # ==================== Board Projects & Versions ====================

    async def get_projects(
        self,
        board_id: int,
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict:
        """
        获取看板关联的项目

        GET /rest/agile/1.0/board/{boardId}/project

        Args:
            board_id: 看板 ID
            start_at: 起始位置
            max_results: 最大返回数量

        Returns:
            dict: 项目列表
        """
        path = f"{self.BASE_PATH}/{board_id}/project"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        return await self.client.get_json(path, params=params)

    async def get_versions(
        self,
        board_id: int,
        start_at: int = 0,
        max_results: int = 50,
        released: Optional[bool] = None,
    ) -> dict:
        """
        获取看板关联的版本

        GET /rest/agile/1.0/board/{boardId}/version

        Args:
            board_id: 看板 ID
            start_at: 起始位置
            max_results: 最大返回数量
            released: 是否已发布

        Returns:
            dict: 版本列表
        """
        path = f"{self.BASE_PATH}/{board_id}/version"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        if released is not None:
            params["released"] = released

        return await self.client.get_json(path, params=params)

    # ==================== Quick Filters ====================

    async def get_quick_filters(
        self,
        board_id: int,
        start_at: int = 0,
        max_results: int = 50,
    ) -> QuickFilterList:
        """
        获取看板快速过滤器

        GET /rest/agile/1.0/board/{boardId}/quickfilter

        Args:
            board_id: 看板 ID
            start_at: 起始位置
            max_results: 最大返回数量

        Returns:
            QuickFilterList: 快速过滤器列表
        """
        path = f"{self.BASE_PATH}/{board_id}/quickfilter"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        data = await self.client.get_json(path, params=params)
        return QuickFilterList.model_validate(data)

    async def get_quick_filters_raw(
        self,
        board_id: int,
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict:
        """获取看板快速过滤器（原始 JSON）"""
        path = f"{self.BASE_PATH}/{board_id}/quickfilter"
        params: dict[str, Any] = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        return await self.client.get_json(path, params=params)

    # ==================== Board Properties ====================

    async def get_property_keys(self, board_id: int) -> dict:
        """
        获取看板属性键列表

        GET /rest/agile/1.0/board/{boardId}/properties

        Args:
            board_id: 看板 ID

        Returns:
            dict: 属性键列表
        """
        path = f"{self.BASE_PATH}/{board_id}/properties"
        return await self.client.get_json(path)

    async def get_property(self, board_id: int, property_key: str) -> dict:
        """
        获取看板属性

        GET /rest/agile/1.0/board/{boardId}/properties/{propertyKey}

        Args:
            board_id: 看板 ID
            property_key: 属性键

        Returns:
            dict: 属性值
        """
        path = f"{self.BASE_PATH}/{board_id}/properties/{property_key}"
        return await self.client.get_json(path)

    async def set_property(
        self,
        board_id: int,
        property_key: str,
        value: Any,
    ) -> None:
        """
        设置看板属性

        PUT /rest/agile/1.0/board/{boardId}/properties/{propertyKey}

        Args:
            board_id: 看板 ID
            property_key: 属性键
            value: 属性值
        """
        path = f"{self.BASE_PATH}/{board_id}/properties/{property_key}"
        await self.client.put_json(path, data=value)

    async def delete_property(self, board_id: int, property_key: str) -> None:
        """
        删除看板属性

        DELETE /rest/agile/1.0/board/{boardId}/properties/{propertyKey}

        Args:
            board_id: 看板 ID
            property_key: 属性键
        """
        path = f"{self.BASE_PATH}/{board_id}/properties/{property_key}"
        await self.client.delete(path)
