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
from atlassian.jira.resources.search import SearchResource
from atlassian.jira.resources.component import ComponentResource
from atlassian.jira.resources.version import VersionResource
from atlassian.jira.resources.user import UserResource
from atlassian.jira.resources.filter import FilterResource
from atlassian.jira.resources.group import GroupResource
from atlassian.jira.resources.workflow import WorkflowResource
from atlassian.jira.resources.workflow_scheme import WorkflowSchemeResource
from atlassian.jira.resources.status import StatusResource
from atlassian.jira.resources.resolution import ResolutionResource
from atlassian.jira.resources.permission_scheme import PermissionSchemeResource
from atlassian.jira.resources.role import RoleResource
from atlassian.jira.resources.security_level import SecurityLevelResource
from atlassian.jira.resources.issue_type import IssueTypeResource
from atlassian.jira.resources.issue_type_scheme import IssueTypeSchemeResource
from atlassian.jira.resources.field import FieldResource
from atlassian.jira.resources.screen import ScreenResource
from atlassian.jira.resources.priority import PriorityResource
from atlassian.jira.resources.priority_scheme import PrioritySchemeResource

__all__ = [
    "MyselfResource",
    "IssueResource",
    "IssueLinkResource",
    "IssueLinkTypeResource",
    "AttachmentResource",
    "CustomFieldsResource",
    "ProjectResource",
    "SearchResource",
    "ComponentResource",
    "VersionResource",
    "UserResource",
    "FilterResource",
    "GroupResource",
    "WorkflowResource",
    "WorkflowSchemeResource",
    "StatusResource",
    "ResolutionResource",
    "PermissionSchemeResource",
    "RoleResource",
    "SecurityLevelResource",
    "IssueTypeResource",
    "IssueTypeSchemeResource",
    "FieldResource",
    "ScreenResource",
    "PriorityResource",
    "PrioritySchemeResource",
]
