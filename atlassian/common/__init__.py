"""
Atlassian Common - 共享基础模块

提供所有 Atlassian 产品 API 客户端的公共基础设施:
- BaseHttpClient: 基础 HTTP 客户端
- BaseResource: API 资源基类
- 异常类
"""

from atlassian.common.exceptions import (
    AtlassianError,
    AtlassianAuthError,
    AtlassianCaptchaError,
    AtlassianSessionExpiredError,
    AtlassianOAuthError,
    AtlassianAPIError,
    AtlassianNotFoundError,
    AtlassianPermissionError,
)
from atlassian.common.client import BaseHttpClient, SessionInfo
from atlassian.common.base import BaseResource
from atlassian.common.auth import AtlassianOAuth1Flow, OAuth1Config, OAuth1Token

__all__ = [
    # Exceptions
    "AtlassianError",
    "AtlassianAuthError",
    "AtlassianCaptchaError",
    "AtlassianSessionExpiredError",
    "AtlassianOAuthError",
    "AtlassianAPIError",
    "AtlassianNotFoundError",
    "AtlassianPermissionError",
    # Client
    "BaseHttpClient",
    "SessionInfo",
    "AtlassianOAuth1Flow",
    "OAuth1Config",
    "OAuth1Token",
    # Resource
    "BaseResource",
]
