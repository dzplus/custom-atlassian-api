"""
Atlassian Exceptions - 统一异常类

所有 Atlassian 产品 API 客户端共享的异常类
"""


class AtlassianError(Exception):
    """Atlassian API 基础异常"""
    pass


class AtlassianAuthError(AtlassianError):
    """认证异常"""
    pass


class AtlassianCaptchaError(AtlassianAuthError):
    """CAPTCHA 触发异常"""
    pass


class AtlassianSessionExpiredError(AtlassianAuthError):
    """会话过期异常"""
    pass


class AtlassianAPIError(AtlassianError):
    """API 调用异常"""

    def __init__(self, message: str, status_code: int | None = None, response: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class AtlassianNotFoundError(AtlassianAPIError):
    """资源未找到异常 (404)"""
    pass


class AtlassianPermissionError(AtlassianAPIError):
    """权限不足异常 (403)"""
    pass
