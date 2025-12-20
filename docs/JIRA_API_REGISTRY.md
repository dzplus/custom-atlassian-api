# Jira REST API 对接登记表

> 基于 Jira REST API 8.13.5 官方文档
>
> 文档地址: https://docs.atlassian.com/software/jira/docs/api/REST/8.13.5/

**统计信息**:
- 官方 API 总数: 366 个
- 已实现: 32 个 (8.7%)
- 已测试: 0 个 (0%)
- **测试覆盖率**: 0% (0/32 已实现的API)

---

## 实现概览

### 已实现资源统计

| 资源 | 已实现API数 | 总API数 | 实现率 |
|------|-----------|---------|-------|
| Attachment | 5 | 5 | 100% |
| Customfields | 1 | 1 | 100% |
| Issue | 12 | 47 | 26% |
| Issuelink | 3 | 3 | 100% |
| Issuelinktype | 5 | 5 | 100% |
| Myself | 1 | 3 | 33% |
| Project | 5 | 39 | 13% |
| **总计** | **32** | **366** | **8.7%** |

---

## 详细API列表

### 图例
- ✅ 已实现
- ❌ 未实现

---

## Issue（问题/工单） - 20/80 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ✅ | POST | /rest/api/2/issue | Create issue | issue.create() |
| ✅ | POST | /rest/api/2/issue/bulk | Create issues | issue.bulk_create() |
| ✅ | PUT | /rest/api/2/issue/{issueIdOrKey} | Edit issue | issue.update() |
| ✅ | GET | /rest/api/2/issue/{issueIdOrKey} | Get issue | issue.get() |
| ✅ | DELETE | /rest/api/2/issue/{issueIdOrKey} | Delete issue | issue.delete() |
| ❌ | PUT | /rest/api/2/issue/{issueIdOrKey}/archive | Archive issue | - |
| ✅ | PUT | /rest/api/2/issue/{issueIdOrKey}/assignee | Assign | issue.assign() |
| ✅ | GET | /rest/api/2/issue/{issueIdOrKey}/comment | Get comments | issue.get_comments() |
| ✅ | POST | /rest/api/2/issue/{issueIdOrKey}/comment | Add comment | issue.add_comment() |
| ❌ | GET | /rest/api/2/issue/{issueIdOrKey}/comment/{id} | Get comment | - |
| ❌ | PUT | /rest/api/2/issue/{issueIdOrKey}/comment/{id} | Update comment | - |
| ❌ | DELETE | /rest/api/2/issue/{issueIdOrKey}/comment/{id} | Delete comment | - |
| ❌ | GET | /rest/api/2/issue/{issueIdOrKey}/editmeta | Get edit issue meta | - |
| ❌ | POST | /rest/api/2/issue/{issueIdOrKey}/notify | Notify | - |
| ❌ | GET | /rest/api/2/issue/{issueIdOrKey}/remotelink | Get remote issue links | - |
| ❌ | POST | /rest/api/2/issue/{issueIdOrKey}/remotelink | Create or update remote issue link | - |
| ❌ | DELETE | /rest/api/2/issue/{issueIdOrKey}/remotelink | Delete remote issue link by global id | - |
| ❌ | GET | /rest/api/2/issue/{issueIdOrKey}/remotelink/{linkId} | Get remote issue link by id | - |
| ❌ | PUT | /rest/api/2/issue/{issueIdOrKey}/remotelink/{linkId} | Update remote issue link | - |
| ❌ | DELETE | /rest/api/2/issue/{issueIdOrKey}/remotelink/{linkId} | Delete remote issue link by id | - |
| ❌ | PUT | /rest/api/2/issue/{issueIdOrKey}/restore | Restore issue | - |
| ✅ | GET | /rest/api/2/issue/{issueIdOrKey}/transitions | Get transitions | issue.get_transitions() |
| ✅ | POST | /rest/api/2/issue/{issueIdOrKey}/transitions | Do transition | issue.do_transition() |
| ❌ | DELETE | /rest/api/2/issue/{issueIdOrKey}/votes | Remove vote | - |
| ❌ | POST | /rest/api/2/issue/{issueIdOrKey}/votes | Add vote | - |
| ❌ | GET | /rest/api/2/issue/{issueIdOrKey}/votes | Get votes | - |
| ❌ | GET | /rest/api/2/issue/{issueIdOrKey}/watchers | Get issue watchers | - |
| ❌ | POST | /rest/api/2/issue/{issueIdOrKey}/watchers | Add watcher | - |
| ❌ | DELETE | /rest/api/2/issue/{issueIdOrKey}/watchers | Remove watcher | - |
| ❌ | GET | /rest/api/2/issue/{issueIdOrKey}/worklog | Get issue worklog | - |
| ❌ | POST | /rest/api/2/issue/{issueIdOrKey}/worklog | Add worklog | - |
| ❌ | GET | /rest/api/2/issue/{issueIdOrKey}/worklog/{id} | Get worklog | - |
| ❌ | PUT | /rest/api/2/issue/{issueIdOrKey}/worklog/{id} | Update worklog | - |
| ❌ | DELETE | /rest/api/2/issue/{issueIdOrKey}/worklog/{id} | Delete worklog | - |
| ❌ | POST | /rest/api/2/issue/archive | Archive issues | - |
| ❌ | GET | /rest/api/2/issue/createmeta | Get create issue meta | - |
| ❌ | GET | /rest/api/2/issue/createmeta/{projectIdOrKey}/issuetypes | Get create issue meta project issue types | - |
| ❌ | GET | /rest/api/2/issue/createmeta/{projectIdOrKey}/issuetypes/{issueTypeId} | Get create issue meta fields | - |
| ❌ | GET | /rest/api/2/issue/picker | Get issue picker resource | - |
| ✅ | POST | /rest/api/2/issue/{issueIdOrKey}/attachments | Add attachment | issue.add_attachment() |
| ❌ | GET | /rest/api/2/issue/{issueIdOrKey}/properties | Get properties keys | - |
| ❌ | DELETE | /rest/api/2/issue/{issueIdOrKey}/properties/{propertyKey} | Delete property | - |
| ❌ | PUT | /rest/api/2/issue/{issueIdOrKey}/properties/{propertyKey} | Set property | - |
| ❌ | GET | /rest/api/2/issue/{issueIdOrKey}/properties/{propertyKey} | Get property | - |
| ✅ | GET | /rest/api/2/issue/{issueIdOrKey}/subtask | Get sub tasks | issue.get_subtasks() |
| ❌ | POST | /rest/api/2/issue/{issueIdOrKey}/subtask/move | Move sub tasks | - |
| ❌ | GET | /rest/api/2/issue/{issueIdOrKey}/subtask/move | Can move sub task | - |
| ✅ | POST | /rest/api/2/issueLink | Link issues | issue_link.create() |
| ✅ | GET | /rest/api/2/issueLink/{linkId} | Get issue link | issue_link.get() |
| ✅ | DELETE | /rest/api/2/issueLink/{linkId} | Delete issue link | issue_link.delete() |
| ✅ | GET | /rest/api/2/issueLinkType | Get issue link types | issue_link_type.get_all() |
| ✅ | POST | /rest/api/2/issueLinkType | Create issue link type | issue_link_type.create() |
| ✅ | GET | /rest/api/2/issueLinkType/{issueLinkTypeId} | Get issue link type | issue_link_type.get() |
| ✅ | DELETE | /rest/api/2/issueLinkType/{issueLinkTypeId} | Delete issue link type | issue_link_type.delete() |
| ✅ | PUT | /rest/api/2/issueLinkType/{issueLinkTypeId} | Update issue link type | issue_link_type.update() |
| ❌ | GET | /rest/api/2/issuetype | Get issue all types | - |
| ❌ | POST | /rest/api/2/issuetype | Create issue type | - |
| ❌ | PUT | /rest/api/2/issuetype/{id} | Update issue type | - |
| ❌ | GET | /rest/api/2/issuetype/{id} | Get issue type | - |
| ❌ | DELETE | /rest/api/2/issuetype/{id} | Delete issue type | - |
| ❌ | GET | /rest/api/2/issuetype/{id}/alternatives | Get alternative issue types | - |
| ❌ | POST | /rest/api/2/issuetype/{id}/avatar | Create avatar from temporary | - |
| ❌ | POST | /rest/api/2/issuetype/{id}/avatar/temporary | Store temporary avatar | - |
| ❌ | POST | /rest/api/2/issuetype/{id}/avatar/temporary | Store temporary avatar using multi part | - |
| ❌ | GET | /rest/api/2/issuetype/{issueTypeId}/properties | Get property keys | - |
| ❌ | DELETE | /rest/api/2/issuetype/{issueTypeId}/properties/{propertyKey} | Delete property | - |
| ❌ | PUT | /rest/api/2/issuetype/{issueTypeId}/properties/{propertyKey} | Set property | - |
| ❌ | GET | /rest/api/2/issuetype/{issueTypeId}/properties/{propertyKey} | Get property | - |
| ❌ | POST | /rest/api/2/issuetypescheme | Create issue type scheme | - |
| ❌ | GET | /rest/api/2/issuetypescheme | Get all issue type schemes | - |
| ❌ | GET | /rest/api/2/issuetypescheme/{schemeId} | Get issue type scheme | - |
| ❌ | PUT | /rest/api/2/issuetypescheme/{schemeId} | Update issue type scheme | - |
| ❌ | DELETE | /rest/api/2/issuetypescheme/{schemeId} | Delete issue type scheme | - |
| ❌ | POST | /rest/api/2/issuetypescheme/{schemeId}/associations | Add project associations to scheme | - |
| ❌ | GET | /rest/api/2/issuetypescheme/{schemeId}/associations | Get associated projects | - |
| ❌ | PUT | /rest/api/2/issuetypescheme/{schemeId}/associations | Set project associations for scheme | - |
| ❌ | DELETE | /rest/api/2/issuetypescheme/{schemeId}/associations | Remove all project associations | - |
| ❌ | DELETE | /rest/api/2/issuetypescheme/{schemeId}/associations/{projIdOrKey} | Remove project association | - |
| ❌ | GET | /rest/api/2/issuesecurityschemes | Get issue security schemes | - |
| ❌ | GET | /rest/api/2/issuesecurityschemes/{id} | Get issue security scheme | - |

---

## Project（项目） - 5/66 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ✅ | GET | /rest/api/2/project | Get all projects | project.get_all() |
| ❌ | POST | /rest/api/2/project | Create project | - |
| ✅ | GET | /rest/api/2/project/{projectIdOrKey} | Get project | project.get() |
| ❌ | PUT | /rest/api/2/project/{projectIdOrKey} | Update project | - |
| ❌ | DELETE | /rest/api/2/project/{projectIdOrKey} | Delete project | - |
| ❌ | PUT | /rest/api/2/project/{projectIdOrKey}/archive | Archive project | - |
| ❌ | POST | /rest/api/2/project/{projectIdOrKey}/avatar | Create avatar from temporary | - |
| ❌ | PUT | /rest/api/2/project/{projectIdOrKey}/avatar | Update project avatar | - |
| ❌ | DELETE | /rest/api/2/project/{projectIdOrKey}/avatar/{id} | Delete avatar | - |
| ❌ | POST | /rest/api/2/project/{projectIdOrKey}/avatar/temporary | Store temporary avatar | - |
| ❌ | POST | /rest/api/2/project/{projectIdOrKey}/avatar/temporary | Store temporary avatar using multi part | - |
| ❌ | GET | /rest/api/2/project/{projectIdOrKey}/avatars | Get all avatars | - |
| ✅ | GET | /rest/api/2/project/{projectIdOrKey}/components | Get project components | project.get_components() |
| ❌ | PUT | /rest/api/2/project/{projectIdOrKey}/restore | Restore project | - |
| ✅ | GET | /rest/api/2/project/{projectIdOrKey}/statuses | Get all statuses | project.get_statuses() |
| ❌ | PUT | /rest/api/2/project/{projectIdOrKey}/type/{newProjectTypeKey} | Update project type | - |
| ❌ | GET | /rest/api/2/project/{projectIdOrKey}/version | Get project versions paginated | - |
| ✅ | GET | /rest/api/2/project/{projectIdOrKey}/versions | Get project versions | project.get_versions() |
| ❌ | GET | /rest/api/2/project/{projectIdOrKey}/properties | Get properties keys | - |
| ❌ | DELETE | /rest/api/2/project/{projectIdOrKey}/properties/{propertyKey} | Delete property | - |
| ❌ | PUT | /rest/api/2/project/{projectIdOrKey}/properties/{propertyKey} | Set property | - |
| ❌ | GET | /rest/api/2/project/{projectIdOrKey}/properties/{propertyKey} | Get property | - |
| ❌ | GET | /rest/api/2/project/{projectIdOrKey}/role | Get project roles | - |
| ❌ | GET | /rest/api/2/project/{projectIdOrKey}/role/{id} | Get project role | - |
| ❌ | PUT | /rest/api/2/project/{projectIdOrKey}/role/{id} | Set actors | - |
| ❌ | POST | /rest/api/2/project/{projectIdOrKey}/role/{id} | Add actor users | - |
| ❌ | DELETE | /rest/api/2/project/{projectIdOrKey}/role/{id} | Delete actor | - |
| ❌ | GET | /rest/api/2/project/{projectKeyOrId}/issuesecuritylevelscheme | Get issue security scheme | - |
| ❌ | GET | /rest/api/2/project/{projectKeyOrId}/notificationscheme | Get notification scheme | - |
| ❌ | PUT | /rest/api/2/project/{projectKeyOrId}/permissionscheme | Assign permission scheme | - |
| ❌ | GET | /rest/api/2/project/{projectKeyOrId}/permissionscheme | Get assigned permission scheme | - |
| ❌ | PUT | /rest/api/2/project/{projectKeyOrId}/priorityscheme | Assign priority scheme | - |
| ❌ | GET | /rest/api/2/project/{projectKeyOrId}/priorityscheme | Get assigned priority scheme | - |
| ❌ | DELETE | /rest/api/2/project/{projectKeyOrId}/priorityscheme/{schemeId} | Unassign priority scheme | - |
| ❌ | GET | /rest/api/2/project/{projectKeyOrId}/securitylevel | Get security levels for project | - |
| ❌ | GET | /rest/api/2/project/{projectKeyOrId}/workflowscheme | Get workflow scheme for project | - |
| ❌ | GET | /rest/api/2/project/type | Get all project types | - |
| ❌ | GET | /rest/api/2/project/type/{projectTypeKey} | Get project type by key | - |
| ❌ | GET | /rest/api/2/project/type/{projectTypeKey}/accessible | Get accessible project type by key | - |
| ❌ | GET | /rest/api/2/projectCategory | Get all project categories | - |
| ❌ | POST | /rest/api/2/projectCategory | Create project category | - |
| ❌ | GET | /rest/api/2/projectCategory/{id} | Get project category by id | - |
| ❌ | DELETE | /rest/api/2/projectCategory/{id} | Remove project category | - |
| ❌ | PUT | /rest/api/2/projectCategory/{id} | Update project category | - |
| ❌ | GET | /rest/api/2/projectvalidate/key | Get project | - |
| ❌ | POST | /rest/api/2/component | Create component | - |
| ❌ | GET | /rest/api/2/component/{id} | Get component | - |
| ❌ | PUT | /rest/api/2/component/{id} | Update component | - |
| ❌ | DELETE | /rest/api/2/component/{id} | Delete | - |
| ❌ | GET | /rest/api/2/component/{id}/relatedIssueCounts | Get component related issues | - |
| ❌ | POST | /rest/api/2/version | Create version | - |
| ❌ | POST | /rest/api/2/version/{id}/move | Move version | - |
| ❌ | GET | /rest/api/2/version/{id} | Get version | - |
| ❌ | PUT | /rest/api/2/version/{id} | Update version | - |
| ❌ | DELETE | /rest/api/2/version/{id} | Delete | - |
| ❌ | PUT | /rest/api/2/version/{id}/mergeto/{moveIssuesTo} | Merge | - |
| ❌ | GET | /rest/api/2/version/{id}/relatedIssueCounts | Get version related issues | - |
| ❌ | POST | /rest/api/2/version/{id}/removeAndSwap | Delete | - |
| ❌ | GET | /rest/api/2/version/{id}/unresolvedIssueCount | Get version unresolved issues | - |
| ❌ | GET | /rest/api/2/version/{versionId}/remotelink | Get remote version links by version id | - |
| ❌ | POST | /rest/api/2/version/{versionId}/remotelink | Create or update remote version link | - |
| ❌ | DELETE | /rest/api/2/version/{versionId}/remotelink | Delete remote version links by version id | - |
| ❌ | GET | /rest/api/2/version/{versionId}/remotelink/{globalId} | Get remote version link | - |
| ❌ | POST | /rest/api/2/version/{versionId}/remotelink/{globalId} | Create or update remote version link | - |
| ❌ | DELETE | /rest/api/2/version/{versionId}/remotelink/{globalId} | Delete remote version link | - |
| ❌ | GET | /rest/api/2/version/remotelink | Get remote version links | - |

---

## Search & Filter（搜索和过滤） - 0/18 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | POST | /rest/api/2/search | Search using search request | - |
| ❌ | GET | /rest/api/2/search | Search | - |
| ❌ | POST | /rest/api/2/filter | Create filter | - |
| ❌ | GET | /rest/api/2/filter/{id} | Get filter | - |
| ❌ | PUT | /rest/api/2/filter/{id} | Edit filter | - |
| ❌ | DELETE | /rest/api/2/filter/{id} | Delete filter | - |
| ❌ | GET | /rest/api/2/filter/{id}/columns | Default columns | - |
| ❌ | PUT | /rest/api/2/filter/{id}/columns | Set columns | - |
| ❌ | DELETE | /rest/api/2/filter/{id}/columns | Reset columns | - |
| ❌ | GET | /rest/api/2/filter/{id}/permission | Get share permissions | - |
| ❌ | POST | /rest/api/2/filter/{id}/permission | Add share permission | - |
| ❌ | GET | /rest/api/2/filter/{id}/permission/{permissionId} | Get share permission | - |
| ❌ | DELETE | /rest/api/2/filter/{id}/permission/{permission-id} | Delete share permission | - |
| ❌ | GET | /rest/api/2/filter/defaultShareScope | Get default share scope | - |
| ❌ | PUT | /rest/api/2/filter/defaultShareScope | Set default share scope | - |
| ❌ | GET | /rest/api/2/filter/favourite | Get favourite filters | - |
| ❌ | GET | /rest/api/2/jql/autocompletedata | Get auto complete | - |
| ❌ | GET | /rest/api/2/jql/autocompletedata/suggestions | Get field auto complete for query string | - |

---

## User & Group（用户和组） - 1/44 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | GET | /rest/api/2/user | Get user | - |
| ❌ | POST | /rest/api/2/user | Create user | - |
| ❌ | PUT | /rest/api/2/user | Update user | - |
| ❌ | DELETE | /rest/api/2/user | Remove user | - |
| ❌ | POST | /rest/api/2/user/application | Add user to application | - |
| ❌ | DELETE | /rest/api/2/user/application | Remove user from application | - |
| ❌ | GET | /rest/api/2/user/assignable/multiProjectSearch | Find bulk assignable users | - |
| ❌ | GET | /rest/api/2/user/assignable/search | Find assignable users | - |
| ❌ | POST | /rest/api/2/user/avatar | Create avatar from temporary | - |
| ❌ | PUT | /rest/api/2/user/avatar | Update project avatar | - |
| ❌ | DELETE | /rest/api/2/user/avatar/{id} | Delete avatar | - |
| ❌ | POST | /rest/api/2/user/avatar/temporary | Store temporary avatar | - |
| ❌ | POST | /rest/api/2/user/avatar/temporary | Store temporary avatar using multi part | - |
| ❌ | GET | /rest/api/2/user/avatars | Get all avatars | - |
| ❌ | GET | /rest/api/2/user/columns | Default columns | - |
| ❌ | PUT | /rest/api/2/user/columns | Set columns | - |
| ❌ | DELETE | /rest/api/2/user/columns | Reset columns | - |
| ❌ | PUT | /rest/api/2/user/password | Change user password | - |
| ❌ | GET | /rest/api/2/user/permission/search | Find users with all permissions | - |
| ❌ | GET | /rest/api/2/user/picker | Find users for picker | - |
| ❌ | GET | /rest/api/2/user/search | Find users | - |
| ❌ | GET | /rest/api/2/user/viewissue/search | Find users with browse permission | - |
| ❌ | GET | /rest/api/2/user/a11y/personal-settings | Get a11y personal settings | - |
| ❌ | POST | /rest/api/2/user/anonymization | Schedule user anonymization | - |
| ❌ | GET | /rest/api/2/user/anonymization | Validate user anonymization | - |
| ❌ | POST | /rest/api/2/user/anonymization/rerun | Schedule user anonymization rerun | - |
| ❌ | GET | /rest/api/2/user/anonymization/rerun | Validate user anonymization rerun | - |
| ❌ | GET | /rest/api/2/user/anonymization/progress | Get progress | - |
| ❌ | DELETE | /rest/api/2/user/anonymization/unlock | Unlock anonymization | - |
| ❌ | GET | /rest/api/2/user/properties | Get properties keys | - |
| ❌ | DELETE | /rest/api/2/user/properties/{propertyKey} | Delete property | - |
| ❌ | PUT | /rest/api/2/user/properties/{propertyKey} | Set property | - |
| ❌ | GET | /rest/api/2/user/properties/{propertyKey} | Get property | - |
| ✅ | GET | /rest/api/2/myself | Get user | myself.get() |
| ❌ | PUT | /rest/api/2/myself | Update user | - |
| ❌ | PUT | /rest/api/2/myself/password | Change my password | - |
| ❌ | POST | /rest/api/2/group | Create group | - |
| ❌ | DELETE | /rest/api/2/group | Remove group | - |
| ❌ | GET | /rest/api/2/group | Get group | - |
| ❌ | GET | /rest/api/2/group/member | Get users from group | - |
| ❌ | POST | /rest/api/2/group/user | Add user to group | - |
| ❌ | DELETE | /rest/api/2/group/user | Remove user from group | - |
| ❌ | GET | /rest/api/2/groups/picker | Find groups | - |
| ❌ | GET | /rest/api/2/groupuserpicker | Find users and groups | - |

---

## Workflow（工作流） - 0/37 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | GET | /rest/api/2/workflow | Get all workflows | - |
| ❌ | PUT | /rest/api/2/workflow/{id}/properties | Update property | - |
| ❌ | POST | /rest/api/2/workflow/{id}/properties | Create property | - |
| ❌ | DELETE | /rest/api/2/workflow/{id}/properties | Delete property | - |
| ❌ | GET | /rest/api/2/workflow/{id}/properties | Get properties | - |
| ❌ | POST | /rest/api/2/workflowscheme | Create scheme | - |
| ❌ | DELETE | /rest/api/2/workflowscheme/{id} | Delete scheme | - |
| ❌ | GET | /rest/api/2/workflowscheme/{id} | Get by id | - |
| ❌ | PUT | /rest/api/2/workflowscheme/{id} | Update | - |
| ❌ | POST | /rest/api/2/workflowscheme/{id}/createdraft | Create draft for parent | - |
| ❌ | DELETE | /rest/api/2/workflowscheme/{id}/default | Delete default | - |
| ❌ | PUT | /rest/api/2/workflowscheme/{id}/default | Update default | - |
| ❌ | GET | /rest/api/2/workflowscheme/{id}/default | Get default | - |
| ❌ | DELETE | /rest/api/2/workflowscheme/{id}/draft | Delete draft by id | - |
| ❌ | PUT | /rest/api/2/workflowscheme/{id}/draft | Update draft | - |
| ❌ | GET | /rest/api/2/workflowscheme/{id}/draft | Get draft by id | - |
| ❌ | GET | /rest/api/2/workflowscheme/{id}/draft/default | Get draft default | - |
| ❌ | DELETE | /rest/api/2/workflowscheme/{id}/draft/default | Delete draft default | - |
| ❌ | PUT | /rest/api/2/workflowscheme/{id}/draft/default | Update draft default | - |
| ❌ | GET | /rest/api/2/workflowscheme/{id}/draft/issuetype/{issueType} | Get draft issue type | - |
| ❌ | DELETE | /rest/api/2/workflowscheme/{id}/draft/issuetype/{issueType} | Delete draft issue type | - |
| ❌ | PUT | /rest/api/2/workflowscheme/{id}/draft/issuetype/{issueType} | Set draft issue type | - |
| ❌ | GET | /rest/api/2/workflowscheme/{id}/draft/workflow | Get draft workflow | - |
| ❌ | DELETE | /rest/api/2/workflowscheme/{id}/draft/workflow | Delete draft workflow mapping | - |
| ❌ | PUT | /rest/api/2/workflowscheme/{id}/draft/workflow | Update draft workflow mapping | - |
| ❌ | GET | /rest/api/2/workflowscheme/{id}/issuetype/{issueType} | Get issue type | - |
| ❌ | DELETE | /rest/api/2/workflowscheme/{id}/issuetype/{issueType} | Delete issue type | - |
| ❌ | PUT | /rest/api/2/workflowscheme/{id}/issuetype/{issueType} | Set issue type | - |
| ❌ | GET | /rest/api/2/workflowscheme/{id}/workflow | Get workflow | - |
| ❌ | DELETE | /rest/api/2/workflowscheme/{id}/workflow | Delete workflow mapping | - |
| ❌ | PUT | /rest/api/2/workflowscheme/{id}/workflow | Update workflow mapping | - |
| ❌ | GET | /rest/api/2/status | Get statuses | - |
| ❌ | GET | /rest/api/2/status/{idOrName} | Get status | - |
| ❌ | GET | /rest/api/2/statuscategory | Get status categories | - |
| ❌ | GET | /rest/api/2/statuscategory/{idOrKey} | Get status category | - |
| ❌ | GET | /rest/api/2/resolution | Get resolutions | - |
| ❌ | GET | /rest/api/2/resolution/{id} | Get resolution | - |

---

## Permission & Role（权限和角色） - 0/21 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | GET | /rest/api/2/permissionscheme | Get permission schemes | - |
| ❌ | POST | /rest/api/2/permissionscheme | Create permission scheme | - |
| ❌ | GET | /rest/api/2/permissionscheme/{permissionSchemeId}/attribute/{attributeKey} | Get scheme attribute | - |
| ❌ | PUT | /rest/api/2/permissionscheme/{permissionSchemeId}/attribute/{key} | Set scheme attribute | - |
| ❌ | GET | /rest/api/2/permissionscheme/{schemeId} | Get permission scheme | - |
| ❌ | DELETE | /rest/api/2/permissionscheme/{schemeId} | Delete permission scheme | - |
| ❌ | PUT | /rest/api/2/permissionscheme/{schemeId} | Update permission scheme | - |
| ❌ | GET | /rest/api/2/permissionscheme/{schemeId}/permission | Get permission scheme grants | - |
| ❌ | POST | /rest/api/2/permissionscheme/{schemeId}/permission | Create permission grant | - |
| ❌ | DELETE | /rest/api/2/permissionscheme/{schemeId}/permission/{permissionId} | Delete permission scheme entity | - |
| ❌ | GET | /rest/api/2/permissionscheme/{schemeId}/permission/{permissionId} | Get permission scheme grant | - |
| ❌ | GET | /rest/api/2/role | Get project roles | - |
| ❌ | POST | /rest/api/2/role | Create project role | - |
| ❌ | GET | /rest/api/2/role/{id} | Get project roles by id | - |
| ❌ | POST | /rest/api/2/role/{id} | Partial update project role | - |
| ❌ | PUT | /rest/api/2/role/{id} | Fully update project role | - |
| ❌ | DELETE | /rest/api/2/role/{id} | Delete project role | - |
| ❌ | GET | /rest/api/2/role/{id}/actors | Get project role actors for role | - |
| ❌ | POST | /rest/api/2/role/{id}/actors | Add project role actors to role | - |
| ❌ | DELETE | /rest/api/2/role/{id}/actors | Delete project role actors from role | - |
| ❌ | GET | /rest/api/2/securitylevel/{id} | Get issuesecuritylevel | - |

---

## Field & Screen（字段和屏幕） - 1/16 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | POST | /rest/api/2/field | Create custom field | - |
| ❌ | GET | /rest/api/2/field | Get fields | - |
| ✅ | GET | /rest/api/2/customFields | Get custom fields | custom_fields.get_all() |
| ❌ | GET | /rest/api/2/customFieldOption/{id} | Get custom field option | - |
| ❌ | GET | /rest/api/2/screens | Get all screens | - |
| ❌ | GET | /rest/api/2/screens/{screenId}/availableFields | Get fields to add | - |
| ❌ | POST | /rest/api/2/screens/{screenId}/tabs | Add tab | - |
| ❌ | GET | /rest/api/2/screens/{screenId}/tabs | Get all tabs | - |
| ❌ | PUT | /rest/api/2/screens/{screenId}/tabs/{tabId} | Rename tab | - |
| ❌ | DELETE | /rest/api/2/screens/{screenId}/tabs/{tabId} | Delete tab | - |
| ❌ | POST | /rest/api/2/screens/{screenId}/tabs/{tabId}/fields | Add field | - |
| ❌ | GET | /rest/api/2/screens/{screenId}/tabs/{tabId}/fields | Get all fields | - |
| ❌ | DELETE | /rest/api/2/screens/{screenId}/tabs/{tabId}/fields/{id} | Remove field | - |
| ❌ | POST | /rest/api/2/screens/{screenId}/tabs/{tabId}/fields/{id}/move | Move field | - |
| ❌ | POST | /rest/api/2/screens/{screenId}/tabs/{tabId}/move/{pos} | Move tab | - |
| ❌ | POST | /rest/api/2/screens/addToDefault/{fieldId} | Add field to default screen | - |

---

## Priority（优先级） - 0/7 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | GET | /rest/api/2/priority | Get priorities | - |
| ❌ | GET | /rest/api/2/priority/{id} | Get priority | - |
| ❌ | POST | /rest/api/2/priorityschemes | Create priority scheme | - |
| ❌ | GET | /rest/api/2/priorityschemes | Get priority schemes | - |
| ❌ | DELETE | /rest/api/2/priorityschemes/{schemeId} | Delete priority scheme | - |
| ❌ | PUT | /rest/api/2/priorityschemes/{schemeId} | Update priority scheme | - |
| ❌ | GET | /rest/api/2/priorityschemes/{schemeId} | Get priority scheme | - |

---

## Notification（通知） - 0/2 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | GET | /rest/api/2/notificationscheme | Get notification schemes | - |
| ❌ | GET | /rest/api/2/notificationscheme/{id} | Get notification scheme | - |

---

## Dashboard（仪表板） - 0/6 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | GET | /rest/api/2/dashboard | List | - |
| ❌ | GET | /rest/api/2/dashboard/{id} | Get dashboard | - |
| ❌ | GET | /rest/api/2/dashboard/{dashboardId}/items/{itemId}/properties | Get properties keys | - |
| ❌ | DELETE | /rest/api/2/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey} | Delete property | - |
| ❌ | PUT | /rest/api/2/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey} | Set property | - |
| ❌ | GET | /rest/api/2/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey} | Get property | - |

---

## Attachment & Avatar（附件和头像） - 5/13 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ✅ | DELETE | /rest/api/2/attachment/{id} | Remove attachment | attachment.delete() |
| ✅ | GET | /rest/api/2/attachment/{id} | Get attachment | attachment.get() |
| ✅ | GET | /rest/api/2/attachment/{id}/expand/human | Expand for humans | attachment.expand_human() |
| ✅ | GET | /rest/api/2/attachment/{id}/expand/raw | Expand for machines | attachment.expand_raw() |
| ✅ | GET | /rest/api/2/attachment/meta | Get attachment meta | attachment.get_meta() |
| ❌ | GET | /rest/api/2/avatar/{type}/system | Get all system avatars | - |
| ❌ | POST | /rest/api/2/avatar/{type}/temporary | Store temporary avatar | - |
| ❌ | POST | /rest/api/2/avatar/{type}/temporaryCrop | Create avatar from temporary | - |
| ❌ | GET | /rest/api/2/universal_avatar/type/{type}/owner/{owningObjectId} | Get avatars | - |
| ❌ | POST | /rest/api/2/universal_avatar/type/{type}/owner/{owningObjectId}/avatar | Create avatar from temporary | - |
| ❌ | DELETE | /rest/api/2/universal_avatar/type/{type}/owner/{owningObjectId}/avatar/{id} | Delete avatar | - |
| ❌ | POST | /rest/api/2/universal_avatar/type/{type}/owner/{owningObjectId}/temp | Store temporary avatar | - |
| ❌ | POST | /rest/api/2/universal_avatar/type/{type}/owner/{owningObjectId}/temp | Store temporary avatar using multi part | - |

---

## Comment & Worklog（评论和工作日志） - 0/7 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | GET | /rest/api/2/comment/{commentId}/properties | Get properties keys | - |
| ❌ | DELETE | /rest/api/2/comment/{commentId}/properties/{propertyKey} | Delete property | - |
| ❌ | PUT | /rest/api/2/comment/{commentId}/properties/{propertyKey} | Set property | - |
| ❌ | GET | /rest/api/2/comment/{commentId}/properties/{propertyKey} | Get property | - |
| ❌ | GET | /rest/api/2/worklog/deleted | Get ids of worklogs deleted since | - |
| ❌ | POST | /rest/api/2/worklog/list | Get worklogs for ids | - |
| ❌ | GET | /rest/api/2/worklog/updated | Get ids of worklogs modified since | - |

---

## Application & Configuration（应用和配置） - 0/12 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | GET | /rest/api/2/application-properties | Get property | - |
| ❌ | PUT | /rest/api/2/application-properties/{id} | Set property via restful table | - |
| ❌ | GET | /rest/api/2/application-properties/advanced-settings | Get advanced settings | - |
| ❌ | GET | /rest/api/2/applicationrole | Get all | - |
| ❌ | PUT | /rest/api/2/applicationrole | Put bulk | - |
| ❌ | GET | /rest/api/2/applicationrole/{key} | Get | - |
| ❌ | PUT | /rest/api/2/applicationrole/{key} | Put | - |
| ❌ | GET | /rest/api/2/configuration | Get configuration | - |
| ❌ | PUT | /rest/api/2/settings/baseUrl | Set base u r l | - |
| ❌ | GET | /rest/api/2/settings/columns | Get issue navigator default columns | - |
| ❌ | PUT | /rest/api/2/settings/columns | Set issue navigator default columns | - |
| ❌ | GET | /rest/api/2/serverInfo | Get server info | - |

---

## Audit & Monitoring（审计和监控） - 0/13 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | POST | /rest/api/2/auditing/record | Add record | - |
| ❌ | GET | /rest/api/2/auditing/record | Get records | - |
| ❌ | GET | /rest/api/2/monitoring/jmx/areMetricsExposed | Are metrics exposed | - |
| ❌ | GET | /rest/api/2/monitoring/jmx/getAvailableMetrics | Get available metrics | - |
| ❌ | POST | /rest/api/2/monitoring/jmx/startExposing | Start | - |
| ❌ | POST | /rest/api/2/monitoring/jmx/stopExposing | Stop | - |
| ❌ | POST | /rest/api/2/reindex | Reindex | - |
| ❌ | GET | /rest/api/2/reindex | Get reindex info | - |
| ❌ | POST | /rest/api/2/reindex/issue | Reindex issues | - |
| ❌ | GET | /rest/api/2/reindex/progress | Get reindex progress | - |
| ❌ | POST | /rest/api/2/reindex/request | Process requests | - |
| ❌ | GET | /rest/api/2/reindex/request/{requestId} | Get progress | - |
| ❌ | GET | /rest/api/2/reindex/request/bulk | Get progress bulk | - |

---

## Password & Preferences（密码和偏好设置） - 0/6 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | GET | /rest/api/2/password/policy | Get password policy | - |
| ❌ | POST | /rest/api/2/password/policy/createUser | Policy check create user | - |
| ❌ | POST | /rest/api/2/password/policy/updateUser | Policy check update user | - |
| ❌ | GET | /rest/api/2/mypreferences | Get preference | - |
| ❌ | PUT | /rest/api/2/mypreferences | Set preference | - |
| ❌ | DELETE | /rest/api/2/mypreferences | Remove preference | - |

---

## Cluster & Upgrade（集群和升级） - 0/10 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | GET | /rest/api/2/cluster/nodes | Get all nodes | - |
| ❌ | DELETE | /rest/api/2/cluster/node/{nodeId} | Delete node | - |
| ❌ | PUT | /rest/api/2/cluster/node/{nodeId}/offline | Change node state to offline | - |
| ❌ | POST | /rest/api/2/cluster/zdu/approve | Approve upgrade | - |
| ❌ | POST | /rest/api/2/cluster/zdu/cancel | Cancel upgrade | - |
| ❌ | POST | /rest/api/2/cluster/zdu/retryUpgrade | Acknowledge errors | - |
| ❌ | POST | /rest/api/2/cluster/zdu/start | Set ready to upgrade | - |
| ❌ | GET | /rest/api/2/cluster/zdu/state | Get state | - |
| ❌ | POST | /rest/api/2/upgrade | Run upgrades now | - |
| ❌ | GET | /rest/api/2/upgrade | Get upgrade result | - |

---

## License（许可证） - 0/1 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | POST | /rest/api/2/licenseValidator | Validate | - |

---

## Index（索引） - 0/1 已实现

| 状态 | HTTP方法 | API路径 | 接口描述 | 对应的API |
|------|---------|---------|---------|----------|
| ❌ | GET | /rest/api/2/index/summary | Get index summary | - |

---

## 统计汇总

### 按资源分类统计

| 资源类型 | 官方API数量 | 已实现 | 实现率 | 已测试 | 测试率 |
|---------|-----------|-------|-------|-------|-------|
| Application | 3 | 0 | 0% | 0 | 0% |
| Applicationrole | 4 | 0 | 0% | 0 | 0% |
| Attachment | 5 | 5 | 100% | 0 | 0% |
| Auditing | 2 | 0 | 0% | 0 | 0% |
| Avatar | 3 | 0 | 0% | 0 | 0% |
| Cluster | 8 | 0 | 0% | 0 | 0% |
| Comment | 4 | 0 | 0% | 0 | 0% |
| Component | 5 | 0 | 0% | 0 | 0% |
| Configuration | 1 | 0 | 0% | 0 | 0% |
| Customfieldoption | 1 | 0 | 0% | 0 | 0% |
| Customfields | 1 | 1 | 100% | 0 | 0% |
| Dashboard | 6 | 0 | 0% | 0 | 0% |
| Field | 2 | 0 | 0% | 0 | 0% |
| Filter | 14 | 0 | 0% | 0 | 0% |
| Group | 6 | 0 | 0% | 0 | 0% |
| Groups | 1 | 0 | 0% | 0 | 0% |
| Groupuserpicker | 1 | 0 | 0% | 0 | 0% |
| Index | 1 | 0 | 0% | 0 | 0% |
| Issue | 47 | 12 | 26% | 0 | 0% |
| Issuelink | 3 | 3 | 100% | 0 | 0% |
| Issuelinktype | 5 | 5 | 100% | 0 | 0% |
| Issuesecurityschemes | 2 | 0 | 0% | 0 | 0% |
| Issuetype | 13 | 0 | 0% | 0 | 0% |
| Issuetypescheme | 10 | 0 | 0% | 0 | 0% |
| Jql | 2 | 0 | 0% | 0 | 0% |
| Licensevalidator | 1 | 0 | 0% | 0 | 0% |
| Monitoring | 4 | 0 | 0% | 0 | 0% |
| Mypreferences | 3 | 0 | 0% | 0 | 0% |
| Myself | 3 | 1 | 33% | 0 | 0% |
| Notificationscheme | 2 | 0 | 0% | 0 | 0% |
| Password | 3 | 0 | 0% | 0 | 0% |
| Permissionscheme | 11 | 0 | 0% | 0 | 0% |
| Priority | 2 | 0 | 0% | 0 | 0% |
| Priorityschemes | 5 | 0 | 0% | 0 | 0% |
| Project | 39 | 5 | 13% | 0 | 0% |
| Projectcategory | 5 | 0 | 0% | 0 | 0% |
| Projectvalidate | 1 | 0 | 0% | 0 | 0% |
| Reindex | 7 | 0 | 0% | 0 | 0% |
| Resolution | 2 | 0 | 0% | 0 | 0% |
| Role | 9 | 0 | 0% | 0 | 0% |
| Screens | 12 | 0 | 0% | 0 | 0% |
| Search | 2 | 0 | 0% | 0 | 0% |
| Securitylevel | 1 | 0 | 0% | 0 | 0% |
| Serverinfo | 1 | 0 | 0% | 0 | 0% |
| Settings | 3 | 0 | 0% | 0 | 0% |
| Status | 2 | 0 | 0% | 0 | 0% |
| Statuscategory | 2 | 0 | 0% | 0 | 0% |
| Universal_avatar | 5 | 0 | 0% | 0 | 0% |
| Upgrade | 2 | 0 | 0% | 0 | 0% |
| User | 33 | 0 | 0% | 0 | 0% |
| Version | 16 | 0 | 0% | 0 | 0% |
| Workflow | 5 | 0 | 0% | 0 | 0% |
| Workflowscheme | 26 | 0 | 0% | 0 | 0% |
| Worklog | 3 | 0 | 0% | 0 | 0% |
| **总计** | **366** | **32** | **8.7%** | **0** | **0%** |

---

## 优先级建议

### 第一阶段 - 核心功能（部分已实现）

1. **Issue 问题管理** ✅ 部分实现
   - ✅ 基础CRUD操作
   - ✅ 转换/工作流操作
   - ✅ 评论管理
   - ✅ 附件上传
   - ✅ 子任务查询
   - ❌ 工作日志（待实现）
   - ❌ 监视者和投票（待实现）
   - ❌ 远程链接（待实现）

2. **Project 项目管理** ✅ 部分实现
   - ✅ 获取项目列表和详情
   - ✅ 获取项目组件
   - ✅ 获取项目版本
   - ✅ 获取项目状态
   - ❌ 项目CRUD操作（待实现）
   - ❌ 项目角色管理（待实现）

3. **Search 搜索** ❌ 未实现
   - ❌ JQL搜索

4. **User 用户管理** ✅ 部分实现
   - ✅ 获取当前用户
   - ❌ 用户CRUD操作（待实现）
   - ❌ 用户搜索（待实现）

### 第二阶段 - 扩展功能

1. **Attachment 附件** ✅ 已实现
   - ✅ 获取附件元数据
   - ✅ 删除附件
   - ✅ 获取附件配置
   - ✅ 展开归档内容

2. **Issue Link 问题链接** ✅ 已实现
   - ✅ 创建、获取、删除链接

3. **Issue Link Type 链接类型** ✅ 已实现
   - ✅ 完整CRUD操作

4. **Custom Fields 自定义字段** ✅ 已实现
   - ✅ 获取自定义字段列表

5. **Workflow 工作流** ❌ 未实现
6. **Filter 过滤器** ❌ 未实现
7. **Dashboard 仪表板** ❌ 未实现

### 待实现的重点API

#### Issue相关（高优先级）
- ❌ GET/POST/PUT/DELETE /rest/api/2/issue/{issueIdOrKey}/comment/{id} - 评论管理
- ❌ GET/POST /rest/api/2/issue/{issueIdOrKey}/worklog - 工作日志
- ❌ GET/POST/DELETE /rest/api/2/issue/{issueIdOrKey}/watchers - 监视者
- ❌ GET/POST/DELETE /rest/api/2/issue/{issueIdOrKey}/votes - 投票
- ❌ GET /rest/api/2/issue/{issueIdOrKey}/remotelink - 远程链接

#### Project相关（高优先级）
- ❌ POST /rest/api/2/project - 创建项目
- ❌ PUT /rest/api/2/project/{projectIdOrKey} - 更新项目
- ❌ DELETE /rest/api/2/project/{projectIdOrKey} - 删除项目
- ❌ GET /rest/api/2/project/{projectIdOrKey}/role - 项目角色

#### Search相关（高优先级）
- ❌ GET/POST /rest/api/2/search - JQL搜索

#### User相关（中优先级）
- ❌ GET /rest/api/2/user - 获取用户
- ❌ GET /rest/api/2/user/search - 搜索用户
- ❌ POST /rest/api/2/user - 创建用户
- ❌ PUT /rest/api/2/user - 更新用户
- ❌ DELETE /rest/api/2/user - 删除用户

---

## 更新日志

| 日期 | 更新内容 |
|------|---------|
| 2025-12-20 | 初始创建，基于 Jira REST API 8.13.5 从官方文档提取完整API列表 |
| 2025-12-20 | 成功提取 366 个API，分布在 54 个资源中 |
| 2025-12-20 | 对比现有代码，已实现 32 个API (8.7%) |

---

## 参考文档

- [Jira REST API 8.13.5 官方文档](https://docs.atlassian.com/software/jira/docs/api/REST/8.13.5/)
- [Jira REST API 开发者指南](https://developer.atlassian.com/server/jira/platform/rest-apis/)

---

## 注意事项

1. **API版本**: 当前使用 `/rest/api/2/` 作为基础路径
2. **认证方式**: 支持 Basic Auth、OAuth 1.0a、OAuth 2.0
3. **返回格式**: JSON
4. **字符编码**: UTF-8
5. **分页**: 使用 `startAt` 和 `maxResults` 参数
6. **展开参数**: 使用 `expand` 参数获取额外信息
7. **字段过滤**: 使用 `fields` 参数选择返回字段
8. **总API数量**: 366 个API
9. **资源数量**: 54 个资源
10. **当前实现率**: 8.7%

