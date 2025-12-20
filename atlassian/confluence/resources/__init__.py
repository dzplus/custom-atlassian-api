"""
Confluence Resources - API 资源类
"""

from atlassian.confluence.resources.content import ContentResource
from atlassian.confluence.resources.space import SpaceResource
from atlassian.confluence.resources.user import UserResource
from atlassian.confluence.resources.search import SearchResource
from atlassian.confluence.resources.notification import NotificationResource
from atlassian.confluence.resources.group import GroupResource
from atlassian.confluence.resources.audit import AuditResource
from atlassian.confluence.resources.longtask import LongTaskResource
from atlassian.confluence.resources.webhook import WebhookResource
from atlassian.confluence.resources.accessmode import AccessModeResource

__all__ = [
    "ContentResource",
    "SpaceResource",
    "UserResource",
    "SearchResource",
    "NotificationResource",
    "GroupResource",
    "AuditResource",
    "LongTaskResource",
    "WebhookResource",
    "AccessModeResource",
]
