"""
Custom Atlassian API - 使用示例

使用前请设置环境变量:
- JIRA_URL: Jira 服务地址
- JIRA_USERNAME: 用户名
- JIRA_PASSWORD: 密码

或使用通用变量:
- ATLASSIAN_URL, ATLASSIAN_USERNAME, ATLASSIAN_PASSWORD
"""

import asyncio
from atlassian.jira import JiraClient


async def main():
    """示例：使用 JiraClient"""
    async with JiraClient() as jira:
        # 获取当前用户
        user = await jira.myself.get()
        print(f"当前用户: {user.display_name} ({user.email_address})")

        # 获取所有项目
        projects = await jira.project.get_all()
        print(f"项目数量: {len(projects)}")
        for p in projects[:5]:
            print(f"  - {p.key}: {p.name}")

        # 获取 Issue 链接类型
        link_types = await jira.issue_link_type.get_all()
        print(f"链接类型: {len(link_types)}")
        for lt in link_types:
            print(f"  - {lt.name}: {lt.inward} / {lt.outward}")

        # 获取附件配置
        meta = await jira.attachment.get_meta()
        print(f"附件功能: {'启用' if meta.enabled else '禁用'}, 上传限制: {meta.upload_limit} bytes")

        # 创建 Issue 示例 (注释掉避免实际创建)
        # result = await jira.issue.create(
        #     project="DEMO",
        #     summary="Test Issue",
        #     issue_type="Bug",
        #     description="This is a test issue",
        # )
        # print(f"创建 Issue: {result.key}")


if __name__ == "__main__":
    asyncio.run(main())
