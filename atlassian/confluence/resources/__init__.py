"""
Confluence Resources - API 资源类
"""

from atlassian.confluence.resources.content import ContentResource
from atlassian.confluence.resources.space import SpaceResource
from atlassian.confluence.resources.user import UserResource
from atlassian.confluence.resources.search import SearchResource

__all__ = [
    "ContentResource",
    "SpaceResource",
    "UserResource",
    "SearchResource",
]
