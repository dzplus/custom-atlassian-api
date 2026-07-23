"""
Atlassian API - 统一的 Atlassian 产品 API 客户端

支持的产品:
- Jira Server/Data Center
- Confluence Server/Data Center
"""

__version__ = "0.1.0"

from atlassian.jira import JiraClient
from atlassian.confluence import ConfluenceClient
from atlassian.common.auth import AtlassianOAuth1Flow, OAuth1Config, OAuth1Token
from atlassian.common.exceptions import AtlassianOAuthError

__all__ = [
    "JiraClient",
    "ConfluenceClient",
    "AtlassianOAuth1Flow",
    "OAuth1Config",
    "OAuth1Token",
    "AtlassianOAuthError",
]
