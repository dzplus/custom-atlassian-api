"""
Content Resource - Content API

GET    /rest/api/content                              - 获取内容列表
POST   /rest/api/content                              - 创建内容
GET    /rest/api/content/{id}                         - 获取内容
PUT    /rest/api/content/{id}                         - 更新内容
DELETE /rest/api/content/{id}                         - 删除内容
GET    /rest/api/content/search                       - 搜索内容 (CQL)

GET    /rest/api/content/{id}/child                   - 获取子内容
GET    /rest/api/content/{id}/child/{type}            - 获取指定类型子内容
GET    /rest/api/content/{id}/child/attachment        - 获取附件
POST   /rest/api/content/{id}/child/attachment        - 上传附件
GET    /rest/api/content/{id}/child/comment           - 获取评论

GET    /rest/api/content/{id}/descendant              - 获取所有后代
GET    /rest/api/content/{id}/descendant/{type}       - 获取指定类型后代

GET    /rest/api/content/{id}/property                - 获取属性列表
POST   /rest/api/content/{id}/property                - 创建属性
GET    /rest/api/content/{id}/property/{key}          - 获取属性
PUT    /rest/api/content/{id}/property/{key}          - 更新属性
DELETE /rest/api/content/{id}/property/{key}          - 删除属性

GET    /rest/api/content/{id}/label                   - 获取标签
POST   /rest/api/content/{id}/label                   - 添加标签
DELETE /rest/api/content/{id}/label/{label}           - 删除标签

GET    /rest/api/content/{id}/restriction/byOperation - 获取限制
"""

from typing import Any, Optional
from pathlib import Path

from atlassian.common.base import BaseResource
from atlassian.confluence.models.content import (
    Content,
    ContentList,
    ContentLabel,
    ContentLabelList,
    ContentProperty,
    ContentPropertyList,
    Attachment,
    AttachmentList,
    Comment,
    CommentList,
)


class ContentResource(BaseResource):
    """
    Content 资源

    API: /rest/api/content
    """

    BASE_PATH = "/rest/api/content"

    # ========== Content CRUD ==========

    async def get_all(
        self,
        type: Optional[str] = None,
        space_key: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = None,
        posting_day: Optional[str] = None,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
    ) -> ContentList:
        """
        获取内容列表

        GET /rest/api/content

        Args:
            type: 内容类型 (page, blogpost)
            space_key: 空间 key
            title: 标题（精确匹配）
            status: 状态 (current, trashed, draft, any)
            posting_day: 博客发布日期 (yyyy-mm-dd)
            expand: 展开的字段
            start: 起始位置
            limit: 返回数量

        Returns:
            ContentList: 内容列表
        """
        params: dict[str, Any] = {"start": start, "limit": limit}
        if type:
            params["type"] = type
        if space_key:
            params["spaceKey"] = space_key
        if title:
            params["title"] = title
        if status:
            params["status"] = status
        if posting_day:
            params["postingDay"] = posting_day
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(self.BASE_PATH, params=params)
        return ContentList.model_validate(data)

    async def get(
        self,
        content_id: str,
        status: Optional[str] = None,
        version: Optional[int] = None,
        expand: Optional[str] = None,
    ) -> Content:
        """
        获取内容详情

        GET /rest/api/content/{id}

        Args:
            content_id: 内容 ID
            status: 状态筛选
            version: 版本号
            expand: 展开的字段

        Returns:
            Content: 内容详情
        """
        path = f"{self.BASE_PATH}/{content_id}"
        params: dict[str, Any] = {}
        if status:
            params["status"] = status
        if version:
            params["version"] = version
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return Content.model_validate(data)

    async def get_raw(
        self,
        content_id: str,
        status: Optional[str] = None,
        version: Optional[int] = None,
        expand: Optional[str] = None,
    ) -> dict:
        """
        获取内容详情（原始 JSON）

        Args:
            content_id: 内容 ID
            status: 状态筛选
            version: 版本号
            expand: 展开的字段

        Returns:
            dict: 原始 JSON 响应
        """
        path = f"{self.BASE_PATH}/{content_id}"
        params: dict[str, Any] = {}
        if status:
            params["status"] = status
        if version:
            params["version"] = version
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    async def create(
        self,
        type: str,
        title: str,
        space_key: str,
        body: str,
        body_format: str = "storage",
        parent_id: Optional[str] = None,
        status: str = "current",
    ) -> Content:
        """
        创建内容

        POST /rest/api/content

        Args:
            type: 内容类型 (page, blogpost)
            title: 标题
            space_key: 空间 key
            body: 内容主体
            body_format: 内容格式 (storage, wiki, editor, editor2)
            parent_id: 父页面 ID（可选）
            status: 状态 (current, draft)

        Returns:
            Content: 创建的内容
        """
        payload: dict[str, Any] = {
            "type": type,
            "title": title,
            "space": {"key": space_key},
            "status": status,
            "body": {
                body_format: {
                    "value": body,
                    "representation": body_format,
                }
            },
        }

        if parent_id:
            payload["ancestors"] = [{"id": parent_id}]

        data = await self.client.post_json(self.BASE_PATH, data=payload)
        return Content.model_validate(data)

    async def create_raw(self, payload: dict) -> dict:
        """
        使用原始 payload 创建内容

        Args:
            payload: 原始请求体

        Returns:
            dict: 创建结果
        """
        return await self.client.post_json(self.BASE_PATH, data=payload)

    async def update(
        self,
        content_id: str,
        title: str,
        body: str,
        version_number: int,
        type: str = "page",
        body_format: str = "storage",
        status: str = "current",
        version_message: Optional[str] = None,
        minor_edit: bool = False,
    ) -> Content:
        """
        更新内容

        PUT /rest/api/content/{id}

        注意: version_number 必须比当前版本大 1

        Args:
            content_id: 内容 ID
            title: 标题
            body: 内容主体
            version_number: 新版本号（当前版本 + 1）
            type: 内容类型
            body_format: 内容格式
            status: 状态
            version_message: 版本说明
            minor_edit: 是否为小修改

        Returns:
            Content: 更新后的内容
        """
        path = f"{self.BASE_PATH}/{content_id}"
        payload: dict[str, Any] = {
            "type": type,
            "title": title,
            "status": status,
            "body": {
                body_format: {
                    "value": body,
                    "representation": body_format,
                }
            },
            "version": {
                "number": version_number,
                "minorEdit": minor_edit,
            },
        }

        if version_message:
            payload["version"]["message"] = version_message

        data = await self.client.put_json(path, data=payload)
        return Content.model_validate(data)

    async def update_raw(self, content_id: str, payload: dict) -> dict:
        """
        使用原始 payload 更新内容

        Args:
            content_id: 内容 ID
            payload: 原始请求体

        Returns:
            dict: 更新结果
        """
        path = f"{self.BASE_PATH}/{content_id}"
        return await self.client.put_json(path, data=payload)

    async def delete(self, content_id: str, status: Optional[str] = None) -> None:
        """
        删除内容

        DELETE /rest/api/content/{id}

        Args:
            content_id: 内容 ID
            status: 如果设为 "trashed"，则永久删除已在回收站的内容
        """
        path = f"{self.BASE_PATH}/{content_id}"
        params = {}
        if status:
            params["status"] = status

        response = await self.client.delete(path, params=params)
        response.raise_for_status()

    # ========== Search ==========

    async def search(
        self,
        cql: str,
        cql_context: Optional[str] = None,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
    ) -> ContentList:
        """
        搜索内容 (CQL)

        GET /rest/api/content/search

        Args:
            cql: Confluence Query Language 查询
            cql_context: CQL 上下文
            expand: 展开的字段
            start: 起始位置
            limit: 返回数量

        Returns:
            ContentList: 搜索结果
        """
        params: dict[str, Any] = {
            "cql": cql,
            "start": start,
            "limit": limit,
        }
        if cql_context:
            params["cqlcontext"] = cql_context
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(f"{self.BASE_PATH}/search", params=params)
        return ContentList.model_validate(data)

    # ========== Children ==========

    async def get_children(
        self,
        content_id: str,
        expand: Optional[str] = None,
        parent_version: Optional[int] = None,
    ) -> dict:
        """
        获取所有子内容

        GET /rest/api/content/{id}/child

        Args:
            content_id: 内容 ID
            expand: 展开的字段
            parent_version: 父版本号

        Returns:
            dict: 子内容（按类型分组）
        """
        path = f"{self.BASE_PATH}/{content_id}/child"
        params: dict[str, Any] = {}
        if expand:
            params["expand"] = expand
        if parent_version:
            params["parentVersion"] = parent_version

        return await self.client.get_json(path, params=params)

    async def get_children_by_type(
        self,
        content_id: str,
        child_type: str,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
    ) -> ContentList:
        """
        获取指定类型的子内容

        GET /rest/api/content/{id}/child/{type}

        Args:
            content_id: 内容 ID
            child_type: 子内容类型 (page, comment, attachment)
            expand: 展开的字段
            start: 起始位置
            limit: 返回数量

        Returns:
            ContentList: 子内容列表
        """
        path = f"{self.BASE_PATH}/{content_id}/child/{child_type}"
        params: dict[str, Any] = {"start": start, "limit": limit}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return ContentList.model_validate(data)

    # ========== Attachments ==========

    async def get_attachments(
        self,
        content_id: str,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
        filename: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> AttachmentList:
        """
        获取附件列表

        GET /rest/api/content/{id}/child/attachment

        Args:
            content_id: 内容 ID
            expand: 展开的字段
            start: 起始位置
            limit: 返回数量
            filename: 文件名筛选
            media_type: 媒体类型筛选

        Returns:
            AttachmentList: 附件列表
        """
        path = f"{self.BASE_PATH}/{content_id}/child/attachment"
        params: dict[str, Any] = {"start": start, "limit": limit}
        if expand:
            params["expand"] = expand
        if filename:
            params["filename"] = filename
        if media_type:
            params["mediaType"] = media_type

        data = await self.client.get_json(path, params=params)
        return AttachmentList.model_validate(data)

    async def add_attachment(
        self,
        content_id: str,
        file_path: str,
        filename: Optional[str] = None,
        comment: Optional[str] = None,
        minor_edit: bool = False,
    ) -> AttachmentList:
        """
        上传附件

        POST /rest/api/content/{id}/child/attachment

        Args:
            content_id: 内容 ID
            file_path: 文件路径
            filename: 文件名（可选，默认使用文件原名）
            comment: 附件说明
            minor_edit: 是否为小修改

        Returns:
            AttachmentList: 上传的附件
        """
        path = f"{self.BASE_PATH}/{content_id}/child/attachment"
        file_path_obj = Path(file_path)

        if filename is None:
            filename = file_path_obj.name

        with open(file_path_obj, "rb") as f:
            files = {"file": (filename, f)}
            data = {}
            if comment:
                data["comment"] = comment
            if minor_edit:
                data["minorEdit"] = "true"

            headers = {
                "X-Atlassian-Token": "no-check",
            }
            auth_headers = self.client._get_auth_headers()
            auth_headers.pop("Content-Type", None)
            headers.update(auth_headers)

            response = await self.client._get_client().post(
                path,
                files=files,
                data=data if data else None,
                headers=headers,
            )
            response.raise_for_status()
            result = response.json()

        return AttachmentList.model_validate(result)

    async def add_attachment_bytes(
        self,
        content_id: str,
        content: bytes,
        filename: str,
        comment: Optional[str] = None,
        minor_edit: bool = False,
    ) -> AttachmentList:
        """
        上传字节内容作为附件

        Args:
            content_id: 内容 ID
            content: 文件内容（字节）
            filename: 文件名
            comment: 附件说明
            minor_edit: 是否为小修改

        Returns:
            AttachmentList: 上传的附件
        """
        path = f"{self.BASE_PATH}/{content_id}/child/attachment"

        files = {"file": (filename, content)}
        data = {}
        if comment:
            data["comment"] = comment
        if minor_edit:
            data["minorEdit"] = "true"

        headers = {
            "X-Atlassian-Token": "no-check",
        }
        auth_headers = self.client._get_auth_headers()
        auth_headers.pop("Content-Type", None)
        headers.update(auth_headers)

        response = await self.client._get_client().post(
            path,
            files=files,
            data=data if data else None,
            headers=headers,
        )
        response.raise_for_status()
        result = response.json()

        return AttachmentList.model_validate(result)

    # ========== Comments ==========

    async def get_comments(
        self,
        content_id: str,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
        location: Optional[str] = None,
        depth: Optional[str] = None,
    ) -> CommentList:
        """
        获取评论列表

        GET /rest/api/content/{id}/child/comment

        Args:
            content_id: 内容 ID
            expand: 展开的字段
            start: 起始位置
            limit: 返回数量
            location: 评论位置筛选 (inline, footer, resolved)
            depth: 深度 (空字符串表示仅顶级，"all" 表示所有)

        Returns:
            CommentList: 评论列表
        """
        path = f"{self.BASE_PATH}/{content_id}/child/comment"
        params: dict[str, Any] = {"start": start, "limit": limit}
        if expand:
            params["expand"] = expand
        if location:
            params["location"] = location
        if depth:
            params["depth"] = depth

        data = await self.client.get_json(path, params=params)
        return CommentList.model_validate(data)

    # ========== Descendants ==========

    async def get_descendants(
        self,
        content_id: str,
        expand: Optional[str] = None,
    ) -> dict:
        """
        获取所有后代内容

        GET /rest/api/content/{id}/descendant

        Args:
            content_id: 内容 ID
            expand: 展开的字段

        Returns:
            dict: 后代内容（按类型分组）
        """
        path = f"{self.BASE_PATH}/{content_id}/descendant"
        params: dict[str, Any] = {}
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    async def get_descendants_by_type(
        self,
        content_id: str,
        descendant_type: str,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
    ) -> ContentList:
        """
        获取指定类型的后代内容

        GET /rest/api/content/{id}/descendant/{type}

        Args:
            content_id: 内容 ID
            descendant_type: 后代类型 (page, comment, attachment)
            expand: 展开的字段
            start: 起始位置
            limit: 返回数量

        Returns:
            ContentList: 后代内容列表
        """
        path = f"{self.BASE_PATH}/{content_id}/descendant/{descendant_type}"
        params: dict[str, Any] = {"start": start, "limit": limit}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return ContentList.model_validate(data)

    # ========== Properties ==========

    async def get_properties(
        self,
        content_id: str,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
    ) -> ContentPropertyList:
        """
        获取内容属性列表

        GET /rest/api/content/{id}/property

        Args:
            content_id: 内容 ID
            expand: 展开的字段
            start: 起始位置
            limit: 返回数量

        Returns:
            ContentPropertyList: 属性列表
        """
        path = f"{self.BASE_PATH}/{content_id}/property"
        params: dict[str, Any] = {"start": start, "limit": limit}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return ContentPropertyList.model_validate(data)

    async def get_property(
        self,
        content_id: str,
        key: str,
        expand: Optional[str] = None,
    ) -> ContentProperty:
        """
        获取内容属性

        GET /rest/api/content/{id}/property/{key}

        Args:
            content_id: 内容 ID
            key: 属性 key
            expand: 展开的字段

        Returns:
            ContentProperty: 属性
        """
        path = f"{self.BASE_PATH}/{content_id}/property/{key}"
        params: dict[str, Any] = {}
        if expand:
            params["expand"] = expand

        data = await self.client.get_json(path, params=params)
        return ContentProperty.model_validate(data)

    async def create_property(
        self,
        content_id: str,
        key: str,
        value: Any,
    ) -> ContentProperty:
        """
        创建内容属性

        POST /rest/api/content/{id}/property

        Args:
            content_id: 内容 ID
            key: 属性 key
            value: 属性值

        Returns:
            ContentProperty: 创建的属性
        """
        path = f"{self.BASE_PATH}/{content_id}/property"
        payload = {"key": key, "value": value}

        data = await self.client.post_json(path, data=payload)
        return ContentProperty.model_validate(data)

    async def update_property(
        self,
        content_id: str,
        key: str,
        value: Any,
        version_number: int,
    ) -> ContentProperty:
        """
        更新内容属性

        PUT /rest/api/content/{id}/property/{key}

        Args:
            content_id: 内容 ID
            key: 属性 key
            value: 属性值
            version_number: 新版本号

        Returns:
            ContentProperty: 更新的属性
        """
        path = f"{self.BASE_PATH}/{content_id}/property/{key}"
        payload = {
            "key": key,
            "value": value,
            "version": {"number": version_number},
        }

        data = await self.client.put_json(path, data=payload)
        return ContentProperty.model_validate(data)

    async def delete_property(self, content_id: str, key: str) -> None:
        """
        删除内容属性

        DELETE /rest/api/content/{id}/property/{key}

        Args:
            content_id: 内容 ID
            key: 属性 key
        """
        path = f"{self.BASE_PATH}/{content_id}/property/{key}"
        response = await self.client.delete(path)
        response.raise_for_status()

    # ========== Labels ==========

    async def get_labels(
        self,
        content_id: str,
        prefix: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
    ) -> ContentLabelList:
        """
        获取内容标签

        GET /rest/api/content/{id}/label

        Args:
            content_id: 内容 ID
            prefix: 前缀筛选 (global, my, team)
            start: 起始位置
            limit: 返回数量

        Returns:
            ContentLabelList: 标签列表
        """
        path = f"{self.BASE_PATH}/{content_id}/label"
        params: dict[str, Any] = {"start": start, "limit": limit}
        if prefix:
            params["prefix"] = prefix

        data = await self.client.get_json(path, params=params)
        return ContentLabelList.model_validate(data)

    async def add_labels(
        self,
        content_id: str,
        labels: list[str],
        prefix: str = "global",
    ) -> ContentLabelList:
        """
        添加内容标签

        POST /rest/api/content/{id}/label

        Args:
            content_id: 内容 ID
            labels: 标签列表
            prefix: 标签前缀

        Returns:
            ContentLabelList: 添加后的标签列表
        """
        path = f"{self.BASE_PATH}/{content_id}/label"
        payload = [{"prefix": prefix, "name": label} for label in labels]

        data = await self.client.post_json(path, data=payload)
        return ContentLabelList.model_validate(data)

    async def delete_label(self, content_id: str, label: str) -> None:
        """
        删除内容标签

        DELETE /rest/api/content/{id}/label/{label}

        Args:
            content_id: 内容 ID
            label: 标签名称
        """
        path = f"{self.BASE_PATH}/{content_id}/label/{label}"
        response = await self.client.delete(path)
        response.raise_for_status()

    # ========== Restrictions ==========

    async def get_restrictions(
        self,
        content_id: str,
        expand: Optional[str] = None,
    ) -> dict:
        """
        获取内容限制

        GET /rest/api/content/{id}/restriction/byOperation

        Args:
            content_id: 内容 ID
            expand: 展开的字段

        Returns:
            dict: 限制信息
        """
        path = f"{self.BASE_PATH}/{content_id}/restriction/byOperation"
        params: dict[str, Any] = {}
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    async def get_restrictions_for_operation(
        self,
        content_id: str,
        operation_key: str,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
    ) -> dict:
        """
        获取指定操作的限制

        GET /rest/api/content/{id}/restriction/byOperation/{operationKey}

        Args:
            content_id: 内容 ID
            operation_key: 操作类型 (read, update)
            expand: 展开的字段
            start: 起始位置
            limit: 返回数量

        Returns:
            dict: 限制信息
        """
        path = f"{self.BASE_PATH}/{content_id}/restriction/byOperation/{operation_key}"
        params: dict[str, Any] = {"start": start, "limit": limit}
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    # ========== History ==========

    async def get_history(
        self,
        content_id: str,
        expand: Optional[str] = None,
    ) -> dict:
        """
        获取内容历史记录

        GET /rest/api/content/{id}/history

        Args:
            content_id: 内容 ID
            expand: 展开的字段 (previousVersion, nextVersion, lastUpdated, contributors)

        Returns:
            dict: 历史记录
            {
                "latest": true,
                "createdBy": {...},
                "createdDate": "...",
                "lastUpdated": {...},
                "previousVersion": {...},
                "nextVersion": {...},
                "contributors": {...},
                "_links": {...}
            }
        """
        path = f"{self.BASE_PATH}/{content_id}/history"
        params: dict[str, Any] = {}
        if expand:
            params["expand"] = expand

        return await self.client.get_json(path, params=params)

    # ========== Attachment Update ==========

    async def update_attachment(
        self,
        content_id: str,
        attachment_id: str,
        attachment_data: dict,
    ) -> dict:
        """
        更新附件元数据

        PUT /rest/api/content/{id}/child/attachment/{attachmentId}

        Args:
            content_id: 内容 ID
            attachment_id: 附件 ID
            attachment_data: 附件数据 (title, version 等)

        Returns:
            dict: 更新后的附件信息
        """
        path = f"{self.BASE_PATH}/{content_id}/child/attachment/{attachment_id}"
        return await self.client.put_json(path, data=attachment_data)

    async def update_attachment_data(
        self,
        content_id: str,
        attachment_id: str,
        file_path: str,
        comment: Optional[str] = None,
        minor_edit: bool = False,
    ) -> dict:
        """
        更新附件二进制数据

        POST /rest/api/content/{id}/child/attachment/{attachmentId}/data

        Args:
            content_id: 内容 ID
            attachment_id: 附件 ID
            file_path: 文件路径
            comment: 更新注释
            minor_edit: 是否为小修改

        Returns:
            dict: 更新后的附件信息
        """
        from pathlib import Path

        path = f"{self.BASE_PATH}/{content_id}/child/attachment/{attachment_id}/data"

        file_path_obj = Path(file_path)
        filename = file_path_obj.name

        with open(file_path, "rb") as f:
            files = {"file": (filename, f, "application/octet-stream")}
            data = {"minorEdit": str(minor_edit).lower()}
            if comment:
                data["comment"] = comment

            response = await self.client.post(path, data=data, files=files)
            response.raise_for_status()
            return response.json()

    # ========== ContentBody Convert ==========

    async def convert_contentbody(
        self,
        value: str,
        representation_from: str,
        representation_to: str,
    ) -> dict:
        """
        转换内容格式

        POST /rest/api/contentbody/convert/{to}

        Args:
            value: 要转换的内容
            representation_from: 源格式 (storage, editor, view, export_view, wiki)
            representation_to: 目标格式 (storage, editor, view, export_view)

        Returns:
            dict: 转换后的内容
            {
                "value": "<p>Converted content</p>",
                "representation": "storage"
            }
        """
        path = f"/rest/api/contentbody/convert/{representation_to}"
        payload = {
            "value": value,
            "representation": representation_from,
        }
        return await self.client.post_json(path, data=payload)

    # ========== Blueprint ==========

    async def publish_legacy_draft(
        self,
        draft_id: str,
        status: str = "current",
    ) -> dict:
        """
        发布遗留草稿

        POST /rest/api/content/blueprint/instance/{draftId}

        Args:
            draft_id: 草稿 ID
            status: 发布状态 (默认 "current")

        Returns:
            dict: 发布后的内容
        """
        path = f"/rest/api/content/blueprint/instance/{draft_id}"
        payload = {"status": status}
        return await self.client.post_json(path, data=payload)

    async def publish_shared_draft(
        self,
        draft_id: str,
        status: str = "current",
    ) -> dict:
        """
        发布共享草稿

        PUT /rest/api/content/blueprint/instance/{draftId}

        Args:
            draft_id: 草稿 ID
            status: 发布状态 (默认 "current")

        Returns:
            dict: 发布后的内容
        """
        path = f"/rest/api/content/blueprint/instance/{draft_id}"
        payload = {"status": status}
        return await self.client.put_json(path, data=payload)
