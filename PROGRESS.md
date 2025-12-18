# Atlassian API 实现进度追踪

## 项目概述
统一的 Atlassian 产品 API 客户端，支持 Jira、Confluence、Tempo 等产品
文档：
https://docs.atlassian.com/mywork-confluence-host-plugin/REST/1.1-build22/
https://docs.atlassian.com/atlassian-confluence/REST/6.6.0/

## 技术栈
- Python 3.12+
- UV (包管理)
- httpx (HTTP 客户端)
- Pydantic (数据模型)

## 项目结构

```
custom-atlassian-api/
├── PROGRESS.md                     # 进度追踪文件
├── pyproject.toml                  # UV 项目配置
├── main.py                         # 使用示例
├── atlassian/                      # 主包
│   ├── __init__.py
│   ├── common/                     # 共享基础模块
│   │   ├── __init__.py
│   │   ├── client.py              # BaseHttpClient 基础HTTP客户端
│   │   ├── base.py                # BaseResource 资源基类
│   │   └── exceptions.py          # 统一异常类
│   ├── jira/                       # Jira API
│   │   ├── __init__.py
│   │   ├── client.py              # JiraClient
│   │   ├── models/                # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── issue.py
│   │   │   ├── issue_link.py
│   │   │   ├── attachment.py
│   │   │   ├── project.py
│   │   │   └── custom_field.py
│   │   └── resources/             # API资源类
│   │       ├── __init__.py
│   │       ├── myself.py
│   │       ├── issue.py
│   │       ├── issue_link.py
│   │       ├── issue_link_type.py
│   │       ├── attachment.py
│   │       ├── custom_fields.py
│   │       └── project.py
│   ├── confluence/                 # Confluence API
│   │   ├── __init__.py
│   │   ├── client.py              # ConfluenceClient (基础框架)
│   │   ├── models/                # TODO: 数据模型
│   │   └── resources/             # TODO: API资源类
│   └── tempo/                      # Tempo API (Jira 插件)
│       ├── __init__.py
│       ├── client.py              # TempoClient
│       ├── models/                # 数据模型
│       │   ├── __init__.py
│       │   ├── worklog.py
│       │   ├── account.py
│       │   ├── team.py
│       │   └── plan.py
│       └── resources/             # API资源类
│           ├── __init__.py
│           ├── worklog.py
│           ├── account.py
│           ├── team.py
│           └── plan.py
└── tests/
    ├── __init__.py
    └── test_login.py              # 登录测试
```

## Jira API 实现清单

| API 端点 | 状态 | 资源类 | 描述 |
|---------|------|--------|------|
| `auth/1/session` | [x] 已完成 | BaseHttpClient | Cookie-based 认证会话管理 |
| `api/2/myself` | [x] 已完成 | MyselfResource | 获取当前登录用户信息 |
| `api/2/issueLink` | [x] 已完成 | IssueLinkResource | Issue 链接管理 |
| `api/2/issueLinkType` | [x] 已完成 | IssueLinkTypeResource | Issue 链接类型管理 |
| `api/2/issue` | [x] 已完成 | IssueResource | Issue CRUD 操作 |
| `api/2/customFields` | [x] 已完成 | CustomFieldsResource | 自定义字段查询 |
| `api/2/attachment` | [x] 已完成 | AttachmentResource | 附件元数据和下载 |
| `api/2/issue/{key}/subtask` | [x] 已完成 | IssueResource | Issue 子任务操作 |
| `api/2/issue/{key}/attachments` | [x] 已完成 | IssueResource | Issue 附件上传 |
| `api/2/project` | [x] 已完成 | ProjectResource | 项目管理 |

## Confluence API 实现清单

| API 端点 | 状态 | 资源类 | 描述 |
|---------|------|--------|------|
| `auth/1/session` | [x] 已完成 | BaseHttpClient | 共享认证 |
| `rest/api/space` | [ ] 待实现 | SpaceResource | 空间管理 |
| `rest/api/content` | [ ] 待实现 | ContentResource | 页面/博客管理 |
| `rest/api/user` | [ ] 待实现 | UserResource | 用户管理 |

## Tempo API 实现清单

Tempo 是 Jira 的插件，使用与 Jira 相同的 URL 和认证

### Timesheets API (`/rest/tempo-timesheets/4/`)

| API 端点 | 状态 | 资源类 | 描述 |
|---------|------|--------|------|
| `worklogs` | [x] 已完成 | WorklogResource | 工时记录 CRUD |
| `worklogs/search` | [x] 已完成 | WorklogResource | 搜索工时记录 |
| `timesheet-approval` | [ ] 待实现 | - | 工时审批 |

### Accounts API (`/rest/tempo-accounts/1/`)

| API 端点 | 状态 | 资源类 | 描述 |
|---------|------|--------|------|
| `account` | [x] 已完成 | AccountResource | 账户 CRUD |
| `account/key/{key}` | [x] 已完成 | AccountResource | 按 Key 获取账户 |
| `account/project/{id}` | [x] 已完成 | AccountResource | 获取项目关联账户 |
| `link` | [x] 已完成 | AccountResource | 账户关联管理 |

### Teams API (`/rest/tempo-teams/2/`)

| API 端点 | 状态 | 资源类 | 描述 |
|---------|------|--------|------|
| `team` | [x] 已完成 | TeamResource | 团队 CRUD |
| `team/{id}/member` | [x] 已完成 | TeamResource | 团队成员管理 |

### Planning API (`/rest/tempo-planning/1/`)

| API 端点 | 状态 | 资源类 | 描述 |
|---------|------|--------|------|
| `allocation` | [x] 已完成 | PlanResource | 资源分配 CRUD |
| `allocation/{id}` | [x] 已完成 | PlanResource | 单个资源分配操作 |
| `plan/search` | [x] 已完成 | PlanResource | 搜索计划 |
| `plan` | [x] 已完成 | PlanResource | 计划 CRUD |

## 使用方式

```python
from atlassian.jira import JiraClient

# 异步方式
async with JiraClient() as jira:
    # 获取当前用户
    user = await jira.myself.get()

    # 获取所有项目
    projects = await jira.project.get_all()

    # 创建 Issue
    result = await jira.issue.create(
        project="DEMO",
        summary="Test Issue",
        issue_type="Bug",
    )

    # 获取 Issue
    issue = await jira.issue.get("DEMO-123")

# Tempo 使用示例
from atlassian.tempo import TempoClient

async with TempoClient() as tempo:
    # 搜索工时记录
    worklogs = await tempo.worklog.search(
        from_date="2024-01-01",
        to_date="2024-01-31",
    )

    # 获取所有团队
    teams = await tempo.team.get_all()

    # 获取所有账户
    accounts = await tempo.account.get_all()
```

## 环境变量

### Jira
- `JIRA_URL`: Jira 服务地址
- `JIRA_USERNAME`: 用户名
- `JIRA_PASSWORD`: 密码

### Confluence
- `CONFLUENCE_URL`: Confluence 服务地址
- `CONFLUENCE_USERNAME`: 用户名
- `CONFLUENCE_PASSWORD`: 密码

### Tempo (使用 Jira 的 URL)
- `TEMPO_URL`: Jira 服务地址 (可不设置，自动使用 JIRA_URL)
- `TEMPO_USERNAME`: 用户名 (可不设置，自动使用 JIRA_USERNAME)
- `TEMPO_PASSWORD`: 密码 (可不设置，自动使用 JIRA_PASSWORD)

### 通用 (可被产品特定变量覆盖)
- `ATLASSIAN_URL`: 服务地址
- `ATLASSIAN_USERNAME`: 用户名
- `ATLASSIAN_PASSWORD`: 密码

## 更新日志

### 2025-12-18
- 使用 UV 初始化项目
- 添加 httpx, pydantic 依赖
- 创建多产品支持的项目结构
- 实现 common 共享模块:
  - BaseHttpClient: 基础HTTP客户端，支持Session认证
  - BaseResource: 资源基类
  - 统一异常类
- 实现 Jira API:
  - JiraClient: 统一入口
  - 所有数据模型 (Pydantic)
  - 所有 API 资源类
- 创建 Confluence 基础框架 (待实现具体API)
- 添加双认证模式支持:
  - Session 模式 (Cookie-based)
  - Basic Auth 模式 (Jira/Confluence/Tempo 默认)
- 实现登录测试 (tests/test_login.py):
  - Jira Basic Auth 认证测试通过
  - Confluence Basic Auth 认证测试通过
- 实现 Tempo API:
  - TempoClient: 统一入口
  - WorklogResource: 工时记录管理
  - AccountResource: 账户管理
  - TeamResource: 团队管理
  - PlanResource: 资源计划管理 (allocation + plan)
  - 所有数据模型 (Pydantic)
