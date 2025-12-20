# Atlassian API Client

> 🚀 一个现代化的 Python 异步 Atlassian API 客户端库，支持 Confluence、Jira、Tempo 等产品

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 📑 目录

- [特性](#-特性)
- [API 支持情况](#-api-支持情况)
- [快速开始](#-快速开始)
  - [安装](#安装)
  - [配置](#配置)
  - [第一个程序](#第一个程序)
- [在其他项目中使用](#-在其他项目中使用)
- [使用示例](#-使用示例)
- [高级功能](#-高级功能)
- [Web 框架集成](#-web-框架集成)
- [最佳实践](#-最佳实践)
- [项目结构](#-项目结构)
- [测试](#-测试)
- [常见问题](#-常见问题)
- [环境要求](#-环境要求)
- [路线图](#️-路线图)
- [文档](#-文档)

---

## ✨ 特性

- 🔄 **完全异步** - 基于 `httpx` 的异步 HTTP 客户端
- 📦 **类型安全** - 使用 Pydantic 进行数据验证和类型提示
- 🎯 **API 覆盖率高** - 支持 96% 的 Confluence REST API (94/98)
- 🔌 **多产品支持** - Confluence、Jira、Tempo 统一客户端
- 🔐 **灵活认证** - 支持 Session 和 Basic Auth 两种认证方式
- 🛠️ **易于使用** - 简洁的 API 设计，开箱即用
- 📚 **文档完善** - 详细的使用指南和示例代码

---

## 📊 API 支持情况

### Confluence API

| 资源 | 支持度 | 测试覆盖率 |
|------|--------|-----------|
| Content（内容） | 35/35 (100%) | 85.7% ⭐ |
| Space（空间） | 15/15 (100%) | 100% ⭐ |
| User（用户） | 10/10 (100%) | 100% ⭐ |
| Search（搜索） | 2/2 (100%) | 100% ⭐ |
| Group（用户组） | 3/3 (100%) | 100% ⭐ |
| LongTask（长期任务） | 2/2 (100%) | 100% ⭐ |
| Webhook（7.0+） | 9/9 (100%) | - 🆕 |
| AccessMode（7.0+） | 1/1 (100%) | 100% 🆕 |
| Audit（审计） | 6/6 (100%) | - |
| Notification（插件） | 11/11 (100%) | 27% |

**总计**: 94/98 API 已实现 (96%)，测试覆盖率 70%

详见 [API 登记表](docs/CONFLUENCE_API_REGISTRY.md)

### Jira API

| API 端点 | 状态 | 资源类 | 描述 |
|---------|------|--------|------|
| `auth/1/session` | ✅ 已完成 | BaseHttpClient | Cookie-based 认证会话管理 |
| `api/2/myself` | ✅ 已完成 | MyselfResource | 获取当前登录用户信息 |
| `api/2/issueLink` | ✅ 已完成 | IssueLinkResource | Issue 链接管理 |
| `api/2/issueLinkType` | ✅ 已完成 | IssueLinkTypeResource | Issue 链接类型管理 |
| `api/2/issue` | ✅ 已完成 | IssueResource | Issue CRUD 操作 |
| `api/2/customFields` | ✅ 已完成 | CustomFieldsResource | 自定义字段查询 |
| `api/2/attachment` | ✅ 已完成 | AttachmentResource | 附件元数据和下载 |
| `api/2/issue/{key}/subtask` | ✅ 已完成 | IssueResource | Issue 子任务操作 |
| `api/2/issue/{key}/attachments` | ✅ 已完成 | IssueResource | Issue 附件上传 |
| `api/2/project` | ✅ 已完成 | ProjectResource | 项目管理 |

### Tempo API

Tempo 是 Jira 的插件，使用与 Jira 相同的 URL 和认证

#### Timesheets API (`/rest/tempo-timesheets/4/`)

| API 端点 | 状态 | 资源类 | 描述 |
|---------|------|--------|------|
| `worklogs` | ✅ 已完成 | WorklogResource | 工时记录 CRUD |
| `worklogs/search` | ✅ 已完成 | WorklogResource | 搜索工时记录 |
| `timesheet-approval` | ⏳ 待实现 | - | 工时审批 |

#### Accounts API (`/rest/tempo-accounts/1/`)

| API 端点 | 状态 | 资源类 | 描述 |
|---------|------|--------|------|
| `account` | ✅ 已完成 | AccountResource | 账户 CRUD |
| `account/key/{key}` | ✅ 已完成 | AccountResource | 按 Key 获取账户 |
| `account/project/{id}` | ✅ 已完成 | AccountResource | 获取项目关联账户 |
| `link` | ✅ 已完成 | AccountResource | 账户关联管理 |

#### Teams API (`/rest/tempo-teams/2/`)

| API 端点 | 状态 | 资源类 | 描述 |
|---------|------|--------|------|
| `team` | ✅ 已完成 | TeamResource | 团队 CRUD |
| `team/{id}/member` | ✅ 已完成 | TeamResource | 团队成员管理 |

#### Planning API (`/rest/tempo-planning/1/`)

| API 端点 | 状态 | 资源类 | 描述 |
|---------|------|--------|------|
| `allocation` | ✅ 已完成 | PlanResource | 资源分配 CRUD |
| `allocation/{id}` | ✅ 已完成 | PlanResource | 单个资源分配操作 |
| `plan/search` | ✅ 已完成 | PlanResource | 搜索计划 |
| `plan` | ✅ 已完成 | PlanResource | 计划 CRUD |

---

## 🚀 快速开始

### 安装

#### 方法 1: 本地开发模式（推荐用于开发阶段）

在你的项目目录中执行：

```bash
# 使用 pip
pip install -e /Users/seal/PythonProject/custom-atlassian-api

# 或使用 uv (推荐，更快)
uv add --editable /Users/seal/PythonProject/custom-atlassian-api
```

**验证安装**:

```bash
python -c "from atlassian.confluence import ConfluenceClient; print('✓ 安装成功')"
```

#### 方法 2: Git 仓库安装（推荐用于团队协作）

```bash
# 安装最新版本
pip install git+https://github.com/yourusername/custom-atlassian-api.git

# 指定分支
pip install git+https://github.com/yourusername/custom-atlassian-api.git@develop

# 使用 uv
uv add git+https://github.com/yourusername/custom-atlassian-api.git
```

在 `requirements.txt` 中使用：

```txt
git+https://github.com/yourusername/custom-atlassian-api.git@main
```

在 `pyproject.toml` 中使用：

```toml
[project]
dependencies = [
    "custom-atlassian-api @ git+https://github.com/yourusername/custom-atlassian-api.git@main"
]
```

#### 方法 3: PyPI 发布（推荐用于生产环境）

```bash
# 从 PyPI 安装（发布后）
pip install custom-atlassian-api

# 使用 uv
uv add custom-atlassian-api
```

### 配置

#### 方法 1: 环境变量（推荐）

在项目根目录创建 `.env` 文件：

```env
# Confluence 配置
CONFLUENCE_URL=https://your-confluence.com
CONFLUENCE_USERNAME=your-username
CONFLUENCE_PASSWORD=your-api-token

# Jira 配置
JIRA_URL=https://your-jira.com
JIRA_USERNAME=your-username
JIRA_PASSWORD=your-password

# Tempo 配置（可选，默认使用 Jira 配置）
TEMPO_URL=https://your-jira.com
TEMPO_USERNAME=your-username
TEMPO_PASSWORD=your-password

# 通用配置（可被产品特定变量覆盖）
ATLASSIAN_URL=https://your-atlassian.com
ATLASSIAN_USERNAME=your-username
ATLASSIAN_PASSWORD=your-password
```

**获取 API Token**:
- **Confluence Cloud**: https://id.atlassian.com/manage-profile/security/api-tokens
- **Confluence Server**: 使用你的登录密码即可

代码中使用：

```python
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件

from atlassian.confluence import ConfluenceClient

# 会自动从环境变量读取配置
async with ConfluenceClient() as confluence:
    pass
```

#### 方法 2: 直接传参

```python
from atlassian.confluence import ConfluenceClient

async with ConfluenceClient(
    base_url="https://your-confluence.com",
    username="your-username",
    password="your-api-token"
) as confluence:
    # 使用客户端
    pass
```

#### 方法 3: 配置文件

创建 `config.py`:

```python
import os

CONFLUENCE_CONFIG = {
    "base_url": os.getenv("CONFLUENCE_URL", "https://default-url.com"),
    "username": os.getenv("CONFLUENCE_USERNAME"),
    "password": os.getenv("CONFLUENCE_PASSWORD"),
}
```

使用配置：

```python
from config import CONFLUENCE_CONFIG
from atlassian.confluence import ConfluenceClient

async with ConfluenceClient(**CONFLUENCE_CONFIG) as confluence:
    pass
```

### 第一个程序

创建 `my_confluence_app.py`:

```python
import asyncio
from atlassian.confluence import ConfluenceClient

async def main():
    # 自动从 .env 读取配置
    async with ConfluenceClient() as confluence:
        # 获取当前用户
        user = await confluence.user.get_current()
        print(f"👋 你好, {user.display_name}!")

        # 搜索页面
        results = await confluence.search.search("type=page", limit=5)
        print(f"\n📄 找到 {results.total_size} 个页面:")

        for item in results.results[:5]:
            print(f"  - {item.content.title}")

if __name__ == "__main__":
    asyncio.run(main())
```

**运行程序**:

```bash
python my_confluence_app.py
```

**期望输出**:

```
👋 你好, 断章!

📄 找到 142 个页面:
  - API 文档
  - 开发指南
  - 项目规划
  - 会议纪要
  - 技术方案
```

### 运行示例程序

我们提供了一个完整的示例程序：

```bash
# 运行所有示例
python example_usage.py

# 或使用 uv
uv run python example_usage.py
```

这个示例演示了：
- ✅ 基础使用
- ✅ 空间管理
- ✅ 内容搜索
- ✅ 用户和组管理
- ✅ 监视和通知
- ✅ 系统信息
- ✅ 错误处理
- ✅ 批量操作

---

## 📦 在其他项目中使用

### Django 项目

```python
# myapp/confluence_client.py
from django.conf import settings
from atlassian.confluence import ConfluenceClient

def get_confluence_client():
    """获取 Confluence 客户端"""
    return ConfluenceClient(
        base_url=settings.CONFLUENCE_URL,
        username=settings.CONFLUENCE_USERNAME,
        password=settings.CONFLUENCE_PASSWORD
    )

# myapp/views.py
from django.http import JsonResponse
from .confluence_client import get_confluence_client

async def get_pages(request):
    async with get_confluence_client() as confluence:
        results = await confluence.search.search("type=page", limit=10)
        pages = [{"title": p.content.title} for p in results.results]
        return JsonResponse({"pages": pages})
```

### FastAPI 项目

```python
# app/dependencies.py
from atlassian.confluence import ConfluenceClient
from app.config import settings

async def get_confluence():
    """FastAPI 依赖注入"""
    async with ConfluenceClient(
        base_url=settings.CONFLUENCE_URL,
        username=settings.CONFLUENCE_USERNAME,
        password=settings.CONFLUENCE_PASSWORD
    ) as confluence:
        yield confluence

# app/routers/confluence.py
from fastapi import APIRouter, Depends
from app.dependencies import get_confluence

router = APIRouter()

@router.get("/pages")
async def get_pages(confluence = Depends(get_confluence)):
    results = await confluence.search.search("type=page")
    return {"total": results.total_size}
```

### Flask 项目

```python
# app.py
from flask import Flask, jsonify
from atlassian.confluence import ConfluenceClient
import asyncio

app = Flask(__name__)

@app.route('/confluence/pages')
def get_pages():
    async def fetch_pages():
        async with ConfluenceClient() as confluence:
            results = await confluence.search.search("type=page", limit=10)
            return [{"title": p.content.title} for p in results.results]

    pages = asyncio.run(fetch_pages())
    return jsonify({"pages": pages})
```

### 命令行工具

```python
#!/usr/bin/env python3
# confluence_cli.py
"""Confluence 命令行工具"""

import asyncio
import click
from atlassian.confluence import ConfluenceClient

@click.group()
def cli():
    """Confluence CLI"""
    pass

@cli.command()
@click.option('--space', required=True, help='空间 key')
def list_pages(space):
    """列出空间的所有页面"""
    async def _list():
        async with ConfluenceClient() as confluence:
            content = await confluence.space.get_content(space)
            for page in content.page.results:
                click.echo(f"{page.id}: {page.title}")

    asyncio.run(_list())

@cli.command()
@click.argument('page_id')
def show_page(page_id):
    """显示页面详情"""
    async def _show():
        async with ConfluenceClient() as confluence:
            page = await confluence.content.get(page_id)
            click.echo(f"标题: {page.title}")
            click.echo(f"版本: {page.version.number}")

    asyncio.run(_show())

if __name__ == '__main__':
    cli()
```

使用：

```bash
python confluence_cli.py list-pages --space DEV
python confluence_cli.py show-page 12345
```

### 完整项目示例

#### 项目结构

```
my-confluence-app/
├── .env                    # 环境变量
├── requirements.txt        # 依赖列表
├── config.py              # 配置文件
└── app.py                 # 主应用
```

#### requirements.txt

```txt
# 方法 1: 本地开发
-e /Users/seal/PythonProject/custom-atlassian-api

# 方法 2: Git 仓库
# git+https://github.com/yourusername/custom-atlassian-api.git

# 方法 3: PyPI（发布后）
# custom-atlassian-api>=0.1.0

# 其他依赖
python-dotenv>=1.0.0
```

#### .env

```env
CONFLUENCE_URL=https://your-confluence.com
CONFLUENCE_USERNAME=your-username
CONFLUENCE_PASSWORD=your-api-token
```

#### config.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME")
CONFLUENCE_PASSWORD = os.getenv("CONFLUENCE_PASSWORD")
```

#### app.py

```python
import asyncio
from atlassian.confluence import ConfluenceClient
from config import CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD

async def main():
    async with ConfluenceClient(
        base_url=CONFLUENCE_URL,
        username=CONFLUENCE_USERNAME,
        password=CONFLUENCE_PASSWORD
    ) as confluence:

        # 你的业务逻辑
        user = await confluence.user.get_current()
        print(f"当前用户: {user.display_name}")

        spaces = await confluence.space.get_all(limit=5)
        print(f"\n空间列表:")
        for space in spaces.results:
            print(f"  - {space.key}: {space.name}")

if __name__ == "__main__":
    asyncio.run(main())
```

#### 运行

```bash
cd my-confluence-app
pip install -r requirements.txt
python app.py
```

---

## 💡 使用示例

### Confluence 示例

#### 内容管理

```python
# 获取页面
page = await confluence.content.get("12345", expand="body.storage")
print(f"标题: {page.title}, 版本: {page.version.number}")

# 更新页面
updated = await confluence.content.update(
    content_id="12345",
    title="新标题",
    body="<p>更新后的内容</p>",
    version=page.version.number + 1
)

# 创建页面
page = await confluence.content.create(
    type="page",
    title="我的第一个页面",
    space_key="DEV",
    body="<p>Hello World!</p>"
)
print(f"✓ 创建成功! 页面 ID: {page.id}")

# 添加附件
attachment = await confluence.content.add_attachment(
    content_id="12345",
    file_path="/path/to/file.pdf"
)
```

#### 空间管理

```python
# 获取空间列表
spaces = await confluence.space.get_all()
for space in spaces.results:
    print(f"{space.key}: {space.name}")

# 创建空间
new_space = await confluence.space.create(
    key="PROJ",
    name="项目空间",
    description="项目文档"
)

# 获取空间内容
content = await confluence.space.get_content("DEV")
print(f"空间 'DEV' 有 {content.page.size} 个页面")
```

#### 搜索功能

```python
# CQL 搜索
results = await confluence.search.search(
    "type=page AND space=DEV AND title~'API'"
)

# 搜索最近 7 天修改的页面
results = await confluence.search.search(
    "type=page AND lastModified >= now('-7d')"
)

# 遍历结果
for item in results.results:
    page = item.content
    print(f"{page.title} - {item.url}")
```

#### Webhook（Confluence 7.0+）

```python
# 创建 Webhook（需要管理员权限）
webhook = await confluence.webhook.create({
    "name": "CI/CD Webhook",
    "url": "https://ci.example.com/webhook",
    "events": ["page_created", "page_updated"]
})

# 测试 Webhook
result = await confluence.webhook.test("https://example.com/webhook")
print(f"测试状态: {result['statusCode']}")

# 获取所有 Webhook
webhooks = await confluence.webhook.get_all()
for webhook in webhooks:
    print(f"{webhook['name']}: {webhook['url']}")
```

### Jira 示例

```python
from atlassian.jira import JiraClient

async with JiraClient() as jira:
    # 获取当前用户
    user = await jira.myself.get()
    print(f"当前用户: {user.display_name}")

    # 获取所有项目
    projects = await jira.project.get_all()
    for project in projects:
        print(f"{project.key}: {project.name}")

    # 创建 Issue
    result = await jira.issue.create(
        project="DEMO",
        summary="Test Issue",
        issue_type="Bug",
    )
    print(f"创建 Issue: {result.key}")

    # 获取 Issue
    issue = await jira.issue.get("DEMO-123")
    print(f"Issue 标题: {issue.fields.summary}")

    # 添加附件
    attachment = await jira.issue.add_attachment(
        issue_key="DEMO-123",
        file_path="/path/to/file.pdf"
    )
```

### Tempo 示例

```python
from atlassian.tempo import TempoClient

async with TempoClient() as tempo:
    # 搜索工时记录
    worklogs = await tempo.worklog.search(
        from_date="2024-01-01",
        to_date="2024-01-31",
    )
    print(f"找到 {len(worklogs)} 条工时记录")

    # 获取所有团队
    teams = await tempo.team.get_all()
    for team in teams:
        print(f"团队: {team.name}")

    # 获取所有账户
    accounts = await tempo.account.get_all()
    for account in accounts:
        print(f"账户: {account.name}")

    # 创建资源分配
    allocation = await tempo.plan.create_allocation({
        "planItem": {"id": 123},
        "assignee": {"accountId": "user-id"},
        "plannedSecondsPerDay": 28800,
        "startDate": "2024-01-01",
        "endDate": "2024-01-31"
    })
```

---

## 🔧 高级功能

### 批量操作

```python
import asyncio

# 并发获取多个页面
page_ids = ["123", "456", "789"]
tasks = [confluence.content.get(pid) for pid in page_ids]
pages = await asyncio.gather(*tasks)

# 使用 asyncio.gather 并发执行
tasks = [confluence.content.get(id) for id in page_ids]
pages = await asyncio.gather(*tasks)
```

### 分页处理

```python
async def get_all_pages(space_key):
    all_pages = []
    start = 0
    limit = 25

    while True:
        results = await confluence.content.get_all(
            space_key=space_key,
            start=start,
            limit=limit
        )
        all_pages.extend(results.results)

        if len(results.results) < limit:
            break

        start += limit

    return all_pages
```

### 错误处理

```python
from atlassian.common.exceptions import AtlassianError

try:
    page = await confluence.content.get("invalid-id")
except AtlassianError as e:
    if "404" in str(e):
        print("页面不存在")
    elif "403" in str(e):
        print("权限不足")
    else:
        print(f"错误: {e}")
```

---

## 🌐 Web 框架集成

### FastAPI

```python
from fastapi import FastAPI
from atlassian.confluence import ConfluenceClient

app = FastAPI()

@app.get("/pages/{space_key}")
async def get_pages(space_key: str):
    async with ConfluenceClient() as confluence:
        content = await confluence.space.get_content(space_key)
        return {"pages": [p.title for p in content.page.results]}
```

### Django

```python
from django.http import JsonResponse
from atlassian.confluence import ConfluenceClient

async def confluence_pages(request):
    async with ConfluenceClient() as confluence:
        results = await confluence.search.search("type=page")
        pages = [{"title": p.content.title} for p in results.results]
        return JsonResponse({"pages": pages})
```

---

## 💡 最佳实践

### 1. 使用异步上下文管理器

✅ 推荐：

```python
async with ConfluenceClient() as confluence:
    # 使用客户端
    pass
# 自动关闭连接
```

❌ 不推荐：

```python
confluence = ConfluenceClient()
# 可能忘记关闭连接
```

### 2. 环境变量管理

✅ 推荐：

```python
from dotenv import load_dotenv
load_dotenv()

async with ConfluenceClient() as confluence:
    # 自动从环境变量读取
    pass
```

❌ 不推荐：

```python
# 硬编码凭据
async with ConfluenceClient(
    username="admin",
    password="password123"  # 不安全！
) as confluence:
    pass
```

### 3. 错误处理

✅ 推荐：

```python
from atlassian.common.exceptions import AtlassianError

try:
    page = await confluence.content.get("123")
except AtlassianError as e:
    if "404" in str(e):
        print("页面不存在")
    else:
        print(f"错误: {e}")
```

### 4. 批量操作

✅ 推荐：

```python
# 使用 asyncio.gather 并发执行
tasks = [confluence.content.get(id) for id in page_ids]
pages = await asyncio.gather(*tasks)
```

❌ 不推荐：

```python
# 顺序执行，慢
pages = []
for page_id in page_ids:
    page = await confluence.content.get(page_id)
    pages.append(page)
```

### 5. 使用类型提示

```python
from atlassian.confluence import ConfluenceClient
from atlassian.confluence.models.content import Content

async with ConfluenceClient() as confluence:
    page: Content = await confluence.content.get("12345")
    # 现在 IDE 会提供智能提示
    print(page.title)
```

---

## 📂 项目结构

```
custom-atlassian-api/
├── README.md                       # 项目说明
├── pyproject.toml                  # UV 项目配置
├── example_usage.py                # 使用示例
├── check_admin_permissions.py      # 权限检查工具
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
│   │   ├── client.py              # ConfluenceClient
│   │   ├── models/                # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── content.py
│   │   │   ├── space.py
│   │   │   ├── user.py
│   │   │   └── search.py
│   │   └── resources/             # API资源类
│   │       ├── __init__.py
│   │       ├── content.py
│   │       ├── space.py
│   │       ├── user.py
│   │       ├── search.py
│   │       ├── group.py
│   │       ├── audit.py
│   │       ├── longtask.py
│   │       ├── webhook.py
│   │       ├── accessmode.py
│   │       └── notification.py
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
├── tests/
│   ├── __init__.py
│   ├── test_login.py
│   ├── test_confluence_comprehensive.py
│   ├── test_confluence_7x_apis.py
│   └── test_confluence_new_apis.py
└── docs/
    ├── CONFLUENCE_API_REGISTRY.md
    ├── CONFLUENCE_API_CHANGES_7.6.1.md
    ├── USAGE_GUIDE.md
    ├── WEBHOOK_USAGE_GUIDE.md
    └── confluence_notifications_solution.md
```

---

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
uv run python -m pytest

# 运行 Confluence 测试
uv run python -m tests.test_confluence_comprehensive

# 运行 7.x 新功能测试
uv run python -m tests.test_confluence_7x_apis

# 检查权限
uv run python check_admin_permissions.py
```

### 检查配置

运行配置检查脚本：

```bash
python check_admin_permissions.py
```

输出示例：

```
✓ 用户名: duanzhang
✓ 显示名: 断章
✓ 用户类型: known
✓ 用户所属组 (4 个):
  - confluence-users
  - jira-administrators
  - jira-software-users
  - 开发
🎉 检测到管理员组！
```

---

## ❓ 常见问题

### Q: 如何更新库到最新版本？

**本地开发模式**：

```bash
# 拉取最新代码
cd /Users/seal/PythonProject/custom-atlassian-api
git pull

# 不需要重新安装，因为是 editable 模式
```

**Git 仓库模式**：

```bash
pip install --upgrade git+https://github.com/yourusername/custom-atlassian-api.git
```

**PyPI 模式**：

```bash
pip install --upgrade custom-atlassian-api
```

### Q: 如何在虚拟环境中使用？

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装库
pip install -e /Users/seal/PythonProject/custom-atlassian-api

# 使用
python your_app.py
```

### Q: 支持同步调用吗？

不支持。这个库完全基于异步设计。如果你的项目是同步的，可以这样使用：

```python
import asyncio
from atlassian.confluence import ConfluenceClient

def get_current_user():
    """同步包装器"""
    async def _get():
        async with ConfluenceClient() as confluence:
            return await confluence.user.get_current()

    return asyncio.run(_get())

# 同步调用
user = get_current_user()
print(user.display_name)
```

### Q: 常见错误如何处理？

**1. 403 权限错误**

```
✗ Client error '403' for url '...'
```

解决方法：
- 检查用户名和密码是否正确
- 某些 API 需要管理员权限（如 Webhook、Audit）
- 运行 `python check_admin_permissions.py` 检查权限

**2. 404 API 不存在**

```
✗ Client error '404' for url '...'
```

解决方法：
- 检查 Confluence 版本（部分 API 需要 7.0+）
- Audit API 在旧版本可能不可用

**3. 连接超时**

```
ConnectTimeout: ...
```

解决方法：

```python
# 增加超时时间
async with ConfluenceClient(timeout=60.0) as confluence:
    pass
```

---

## 📋 环境要求

- Python 3.12+
- httpx >= 0.28.1
- pydantic >= 2.12.5

---

## 🗺️ 路线图

- [x] Confluence API 完整支持
- [x] Confluence 7.x 新功能（Webhook、AccessMode）
- [x] Jira API 基础支持
- [x] Tempo API 基础支持
- [ ] Jira API 完整支持
- [ ] Tempo API 完整支持
- [ ] 发布到 PyPI
- [ ] 添加更多测试用例
- [ ] 支持速率限制
- [ ] 支持重试机制

---

## 📖 文档

### 核心文档

- **[完整使用指南](docs/USAGE_GUIDE.md)** - 详细的 API 使用教程
- **[API 登记表](docs/CONFLUENCE_API_REGISTRY.md)** - 所有 API 的实现状态
- **[版本升级指南](docs/CONFLUENCE_API_CHANGES_7.6.1.md)** - 6.6.0 → 7.6.1 变化

### 专题文档

- **[Webhook 使用指南](docs/WEBHOOK_USAGE_GUIDE.md)** - Webhook 详细教程
- **[监视和通知](docs/confluence_notifications_solution.md)** - Watch + Notification 完整方案

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 开源协议

MIT License

---

## 📞 支持

- 📖 [使用文档](docs/USAGE_GUIDE.md)
- 📊 [API 参考](docs/CONFLUENCE_API_REGISTRY.md)
- 🐛 [问题反馈](https://github.com/yourusername/custom-atlassian-api/issues)

---

**🎉 现在你已经准备好使用这个库了！开始构建你的应用吧！**
