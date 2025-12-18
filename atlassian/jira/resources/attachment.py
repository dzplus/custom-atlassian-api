"""
Attachment Resource - 附件 API

GET    /rest/api/2/attachment/{id}              - 获取附件元数据
DELETE /rest/api/2/attachment/{id}              - 删除附件
GET    /rest/api/2/attachment/meta              - 获取附件配置
GET    /rest/api/2/attachment/{id}/expand/human - 展开归档（人类可读）
GET    /rest/api/2/attachment/{id}/expand/raw   - 展开归档（原始格式）
"""

from atlassian.common.base import BaseResource
from atlassian.jira.models.attachment import Attachment, AttachmentMeta, ExpandedArchive


class AttachmentResource(BaseResource):
    """
    附件资源

    API: /rest/api/2/attachment
    """

    BASE_PATH = "/rest/api/2/attachment"

    async def get(self, attachment_id: str) -> Attachment:
        """
        获取附件元数据

        GET /rest/api/2/attachment/{id}

        Args:
            attachment_id: 附件 ID

        Returns:
            Attachment: 附件信息
        """
        path = f"{self.BASE_PATH}/{attachment_id}"
        data = await self.client.get_json(path)
        return Attachment.model_validate(data)

    async def get_raw(self, attachment_id: str) -> dict:
        """
        获取附件元数据（原始 JSON）

        Args:
            attachment_id: 附件 ID

        Returns:
            dict: 原始 JSON 响应
        """
        path = f"{self.BASE_PATH}/{attachment_id}"
        return await self.client.get_json(path)

    async def delete(self, attachment_id: str) -> None:
        """
        删除附件

        DELETE /rest/api/2/attachment/{id}

        Args:
            attachment_id: 附件 ID
        """
        path = f"{self.BASE_PATH}/{attachment_id}"
        response = await self.client.delete(path)
        response.raise_for_status()

    async def get_meta(self) -> AttachmentMeta:
        """
        获取附件配置信息

        GET /rest/api/2/attachment/meta

        Returns:
            AttachmentMeta: 附件配置，包含是否启用和上传限制
        """
        path = f"{self.BASE_PATH}/meta"
        data = await self.client.get_json(path)
        return AttachmentMeta.model_validate(data)

    async def get_meta_raw(self) -> dict:
        """
        获取附件配置信息（原始 JSON）

        Returns:
            dict: 原始 JSON 响应
        """
        path = f"{self.BASE_PATH}/meta"
        return await self.client.get_json(path)

    async def expand_human(self, attachment_id: str) -> ExpandedArchive:
        """
        展开归档内容（人类可读格式）

        GET /rest/api/2/attachment/{id}/expand/human

        适用于 ZIP 等归档文件

        Args:
            attachment_id: 附件 ID

        Returns:
            ExpandedArchive: 归档内容
        """
        path = f"{self.BASE_PATH}/{attachment_id}/expand/human"
        data = await self.client.get_json(path)
        return ExpandedArchive.model_validate(data)

    async def expand_raw(self, attachment_id: str) -> ExpandedArchive:
        """
        展开归档内容（原始格式）

        GET /rest/api/2/attachment/{id}/expand/raw

        适用于 ZIP 等归档文件

        Args:
            attachment_id: 附件 ID

        Returns:
            ExpandedArchive: 归档内容
        """
        path = f"{self.BASE_PATH}/{attachment_id}/expand/raw"
        data = await self.client.get_json(path)
        return ExpandedArchive.model_validate(data)

    async def download(self, attachment_id: str) -> bytes:
        """
        下载附件内容

        Args:
            attachment_id: 附件 ID

        Returns:
            bytes: 附件内容
        """
        # 先获取附件信息，得到下载 URL
        attachment = await self.get(attachment_id)
        if not attachment.content:
            raise ValueError(f"Attachment {attachment_id} has no content URL")

        # 下载内容
        response = await self.client.get(attachment.content)
        response.raise_for_status()
        return response.content

    async def download_by_url(self, content_url: str) -> bytes:
        """
        通过 URL 下载附件内容

        Args:
            content_url: 附件的 content URL

        Returns:
            bytes: 附件内容
        """
        response = await self.client.get(content_url)
        response.raise_for_status()
        return response.content
