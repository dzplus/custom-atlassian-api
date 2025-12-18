"""
Jira Models - Pydantic 数据模型
"""

from atlassian.jira.models.user import User, UserDetails, AvatarUrls
from atlassian.jira.models.issue import (
    Issue,
    IssueFields,
    IssueType,
    Priority,
    Status,
    StatusCategory,
    Resolution,
    IssueTransition,
    IssueComment,
    IssueComments,
    CreateIssueRequest,
    CreateIssueResponse,
    UpdateIssueRequest,
)
from atlassian.jira.models.issue_link import (
    IssueLink,
    IssueLinkType,
    LinkedIssue,
    CreateIssueLinkRequest,
    IssueLinkTypeList,
)
from atlassian.jira.models.attachment import Attachment, AttachmentMeta, ArchiveEntry, ExpandedArchive
from atlassian.jira.models.project import Project, ProjectCategory, ProjectComponent, ProjectVersion, ProjectStatus
from atlassian.jira.models.custom_field import CustomField, CustomFieldsResponse

__all__ = [
    # User
    "User",
    "UserDetails",
    "AvatarUrls",
    # Issue
    "Issue",
    "IssueFields",
    "IssueType",
    "Priority",
    "Status",
    "StatusCategory",
    "Resolution",
    "IssueTransition",
    "IssueComment",
    "IssueComments",
    "CreateIssueRequest",
    "CreateIssueResponse",
    "UpdateIssueRequest",
    # Issue Link
    "IssueLink",
    "IssueLinkType",
    "LinkedIssue",
    "CreateIssueLinkRequest",
    "IssueLinkTypeList",
    # Attachment
    "Attachment",
    "AttachmentMeta",
    "ArchiveEntry",
    "ExpandedArchive",
    # Project
    "Project",
    "ProjectCategory",
    "ProjectComponent",
    "ProjectVersion",
    "ProjectStatus",
    # Custom Field
    "CustomField",
    "CustomFieldsResponse",
]
