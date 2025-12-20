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
    Worklog,
    WorklogList,
    Watchers,
    Votes,
    RemoteObject,
    RemoteLink,
    EditMeta,
    CreateMeta,
    IssuePickerSuggestion,
    IssuePickerSection,
    IssuePickerResults,
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

# Common models
from atlassian.jira.models.common import (
    PaginatedResponse,
    SimpleListResponse,
    ErrorMessage,
    EntityProperty,
    EntityPropertyKeys,
    SimpleLink,
    NamedResource,
    Visibility,
    TimeTracking,
    ServerInfo,
    Scope,
)

# Workflow models
from atlassian.jira.models.workflow import (
    Transition,
    Workflow,
    WorkflowScheme,
    WorkflowSchemeAssociations,
    WorkflowMapping,
    WorkflowStatus,
    TransitionScreenDetails,
    TransitionRule,
    IssueTypeMapping,
    DefaultWorkflow,
    WorkflowSchemeDraft,
)

# Field models
from atlassian.jira.models.field import (
    FieldMetadata,
    AllowedValue,
    FieldConfiguration,
    FieldConfigurationItem,
    FieldConfigurationScheme,
    Screen,
    ScreenTab,
    ScreenableField,
    ScreenScheme,
    IssueTypeScreenScheme,
    CustomFieldOption,
    CustomFieldContext,
    FieldCreateMetadata,
    FieldEditMetadata,
)

# Avatar models
from atlassian.jira.models.avatar import (
    Avatar,
    SystemAvatar,
    CustomAvatar,
    TemporaryAvatar,
    AvatarCropping,
    ProjectAvatar,
    IssueTypeAvatar,
    UserAvatar,
)

# Search models
from atlassian.jira.models.search import SearchResults

# Component models
from atlassian.jira.models.component import Component, ComponentIssueCounts

# Version models
from atlassian.jira.models.version import (
    Version,
    VersionRemoteLink,
    VersionIssueCounts,
    VersionUnresolvedIssueCount,
)

# Filter models
from atlassian.jira.models.filter import (
    Filter,
    FilterPermission,
    FilterSubscription,
    Column,
)

# Group models
from atlassian.jira.models.group import (
    Group,
    GroupMember,
    GroupMembers,
)

# Permission models
from atlassian.jira.models.permission import (
    PermissionGrant,
    PermissionScheme,
    Role,
    RoleActor,
    SecurityLevel,
)

# IssueType models
from atlassian.jira.models.issue_type import (
    IssueTypeScheme,
    IssueTypeSchemeMapping,
    IssueTypeSchemeProjects,
    PriorityScheme,
)

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
    "Worklog",
    "WorklogList",
    "Watchers",
    "Votes",
    "RemoteObject",
    "RemoteLink",
    "EditMeta",
    "CreateMeta",
    "IssuePickerSuggestion",
    "IssuePickerSection",
    "IssuePickerResults",
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
    # Common
    "PaginatedResponse",
    "SimpleListResponse",
    "ErrorMessage",
    "EntityProperty",
    "EntityPropertyKeys",
    "SimpleLink",
    "NamedResource",
    "Visibility",
    "TimeTracking",
    "ServerInfo",
    "Scope",
    # Workflow
    "Transition",
    "Workflow",
    "WorkflowScheme",
    "WorkflowSchemeAssociations",
    "WorkflowMapping",
    "WorkflowStatus",
    "TransitionScreenDetails",
    "TransitionRule",
    "IssueTypeMapping",
    "DefaultWorkflow",
    "WorkflowSchemeDraft",
    # Field
    "FieldMetadata",
    "AllowedValue",
    "FieldConfiguration",
    "FieldConfigurationItem",
    "FieldConfigurationScheme",
    "Screen",
    "ScreenTab",
    "ScreenableField",
    "ScreenScheme",
    "IssueTypeScreenScheme",
    "CustomFieldOption",
    "CustomFieldContext",
    "FieldCreateMetadata",
    "FieldEditMetadata",
    # Avatar
    "Avatar",
    "SystemAvatar",
    "CustomAvatar",
    "TemporaryAvatar",
    "AvatarCropping",
    "ProjectAvatar",
    "IssueTypeAvatar",
    "UserAvatar",
    # Search
    "SearchResults",
    # Component
    "Component",
    "ComponentIssueCounts",
    # Version
    "Version",
    "VersionRemoteLink",
    "VersionIssueCounts",
    "VersionUnresolvedIssueCount",
    # Filter
    "Filter",
    "FilterPermission",
    "FilterSubscription",
    "Column",
    # Group
    "Group",
    "GroupMember",
    "GroupMembers",
    # Permission
    "PermissionGrant",
    "PermissionScheme",
    "Role",
    "RoleActor",
    "SecurityLevel",
    # IssueType
    "IssueTypeScheme",
    "IssueTypeSchemeMapping",
    "IssueTypeSchemeProjects",
    "PriorityScheme",
]
