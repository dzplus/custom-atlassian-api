"""
Jira API Client - Jira Server/Data Center REST API

基于 Jira REST API 8.13.5 文档实现

用法:
    from atlassian.jira import JiraClient

    async with JiraClient() as jira:
        # 获取当前用户
        user = await jira.myself.get()

        # 获取 Issue
        issue = await jira.issue.get("DEMO-123")

        # 获取所有项目
        projects = await jira.project.get_all()
"""

from atlassian.jira.client import JiraClient

__all__ = ["JiraClient"]
