"""
Issue Link Resource - Issue 链接 API

POST   /rest/api/2/issueLink           - 创建链接
GET    /rest/api/2/issueLink/{linkId}  - 获取链接
DELETE /rest/api/2/issueLink/{linkId}  - 删除链接
"""

from typing import Optional

from atlassian.common.base import BaseResource
from atlassian.jira.models.issue_link import IssueLink, CreateIssueLinkRequest


class IssueLinkResource(BaseResource):
    """
    Issue 链接资源

    API: /rest/api/2/issueLink
    """

    BASE_PATH = "/rest/api/2/issueLink"

    async def create(
        self,
        link_type: dict,
        inward_issue: dict,
        outward_issue: dict,
        comment: Optional[dict] = None,
    ) -> None:
        """
        创建 Issue 链接

        POST /rest/api/2/issueLink

        Args:
            link_type: 链接类型，如 {"name": "Blocks"} 或 {"id": "10000"}
            inward_issue: 内向 Issue，如 {"key": "HSP-1"}
            outward_issue: 外向 Issue，如 {"key": "MKY-1"}
            comment: 可选，评论

        Returns:
            None (201 Created)
        """
        payload = {
            "type": link_type,
            "inwardIssue": inward_issue,
            "outwardIssue": outward_issue,
        }
        if comment:
            payload["comment"] = comment

        response = await self.client.post(self.BASE_PATH, json=payload)
        response.raise_for_status()

    async def create_from_request(self, request: CreateIssueLinkRequest) -> None:
        """
        使用请求对象创建 Issue 链接

        Args:
            request: CreateIssueLinkRequest 对象
        """
        payload = request.model_dump(by_alias=True, exclude_none=True)
        response = await self.client.post(self.BASE_PATH, json=payload)
        response.raise_for_status()

    async def get(self, link_id: str) -> IssueLink:
        """
        获取 Issue 链接详情

        GET /rest/api/2/issueLink/{linkId}

        Args:
            link_id: 链接 ID

        Returns:
            IssueLink: Issue 链接信息
        """
        path = f"{self.BASE_PATH}/{link_id}"
        data = await self.client.get_json(path)
        return IssueLink.model_validate(data)

    async def get_raw(self, link_id: str) -> dict:
        """
        获取 Issue 链接详情（原始 JSON）

        Args:
            link_id: 链接 ID

        Returns:
            dict: 原始 JSON 响应
        """
        path = f"{self.BASE_PATH}/{link_id}"
        return await self.client.get_json(path)

    async def delete(self, link_id: str) -> None:
        """
        删除 Issue 链接

        DELETE /rest/api/2/issueLink/{linkId}

        Args:
            link_id: 链接 ID
        """
        path = f"{self.BASE_PATH}/{link_id}"
        response = await self.client.delete(path)
        response.raise_for_status()
