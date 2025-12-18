"""
Jira Resources - API 资源类
"""

from atlassian.jira.resources.myself import MyselfResource
from atlassian.jira.resources.issue import IssueResource
from atlassian.jira.resources.issue_link import IssueLinkResource
from atlassian.jira.resources.issue_link_type import IssueLinkTypeResource
from atlassian.jira.resources.attachment import AttachmentResource
from atlassian.jira.resources.custom_fields import CustomFieldsResource
from atlassian.jira.resources.project import ProjectResource

__all__ = [
    "MyselfResource",
    "IssueResource",
    "IssueLinkResource",
    "IssueLinkTypeResource",
    "AttachmentResource",
    "CustomFieldsResource",
    "ProjectResource",
]
