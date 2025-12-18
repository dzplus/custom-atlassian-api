"""
Confluence Models - Pydantic 数据模型
"""

from atlassian.confluence.models.user import (
    ProfilePicture,
    User,
    UserWatch,
)
from atlassian.confluence.models.space import (
    SpaceDescription,
    Space,
    SpaceList,
    SpaceProperty,
    SpacePropertyList,
)
from atlassian.confluence.models.content import (
    ContentBody,
    ContentBodyContainer,
    ContentVersion,
    ContentHistory,
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
    SearchResult,
    SearchResultList,
)

__all__ = [
    # User
    "ProfilePicture",
    "User",
    "UserWatch",
    # Space
    "SpaceDescription",
    "Space",
    "SpaceList",
    "SpaceProperty",
    "SpacePropertyList",
    # Content
    "ContentBody",
    "ContentBodyContainer",
    "ContentVersion",
    "ContentHistory",
    "Content",
    "ContentList",
    "ContentLabel",
    "ContentLabelList",
    "ContentProperty",
    "ContentPropertyList",
    "Attachment",
    "AttachmentList",
    "Comment",
    "CommentList",
    "SearchResult",
    "SearchResultList",
]
