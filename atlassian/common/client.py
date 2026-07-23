"""
Base HTTP Client - 基础 HTTP 客户端

提供所有 Atlassian 产品 API 客户端的公共 HTTP 功能:
- Session 认证 (Cookie-based)
- Basic Auth 认证 (备选)
- 自动重登录
- 通用 HTTP 方法
"""

import os
import logging
import base64
from typing import Any, Literal, Optional
from dataclasses import dataclass
import httpx

from atlassian.common.auth import OAuth1Config
from atlassian.common.exceptions import (
    AtlassianAuthError,
    AtlassianCaptchaError,
    AtlassianSessionExpiredError,
    AtlassianAPIError,
    AtlassianNotFoundError,
    AtlassianPermissionError,
)

logger = logging.getLogger(__name__)

# 认证模式类型
AuthMode = Literal["session", "basic", "oauth1"]


@dataclass
class SessionInfo:
    """会话信息"""
    session_name: str  # Cookie 名称，通常为 JSESSIONID
    session_value: str  # Cookie 值
    login_count: int = 0
    failed_login_count: int = 0
    last_failed_login_time: Optional[str] = None
    previous_login_time: Optional[str] = None


@dataclass
class BasicAuthInfo:
    """Basic Auth 信息"""
    username: str
    auth_header: str  # Base64 编码的认证头


class BaseHttpClient:
    """
    基础 HTTP 客户端

    支持三种认证模式:
    - session: 使用 /rest/auth/1/session 接口进行登录，获取 JSESSIONID cookie
    - basic: 使用 HTTP Basic Auth 认证
    - oauth1: 使用 Atlassian Application Links OAuth 1.0a RSA-SHA1 签名

    用法:
        # Session 认证 (默认)
        async with BaseHttpClient(base_url, username, password) as client:
            result = await client.get_json("/rest/api/2/myself")

        # Basic Auth 认证
        async with BaseHttpClient(base_url, username, password, auth_mode="basic") as client:
            result = await client.get_json("/rest/api/2/myself")

        # OAuth 1.0a 认证
        async with BaseHttpClient(
            base_url,
            auth_mode="oauth1",
            oauth1=oauth1_config,
        ) as client:
            result = await client.get_json("/rest/api/content")
    """

    AUTH_SESSION_PATH = "/rest/auth/1/session"

    def __init__(
        self,
        base_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: float = 30.0,
        auto_login: bool = True,
        auto_relogin: bool = True,
        env_prefix: str = "",
        auth_mode: AuthMode = "session",
        oauth1: Optional[OAuth1Config] = None,
        trust_env: bool = True,
    ):
        """
        初始化 HTTP 客户端

        Args:
            base_url: 服务地址，默认从 {env_prefix}_URL 环境变量读取
            username: 用户名，默认从 {env_prefix}_USERNAME 环境变量读取
            password: 密码，默认从 {env_prefix}_PASSWORD 环境变量读取
            timeout: 请求超时时间（秒）
            auto_login: 是否在首次请求时自动登录 (仅 session 模式)
            auto_relogin: 会话过期时是否自动重新登录 (仅 session 模式)
            env_prefix: 环境变量前缀（如 "JIRA", "CONFLUENCE"）
            auth_mode: 认证模式，"session"、"basic" 或 "oauth1"
            oauth1: OAuth 1.0a RSA-SHA1 认证配置
            trust_env: 是否读取系统代理等 HTTPX 环境变量
        """
        # 环境变量优先级: 参数 > 带前缀环境变量 > 通用环境变量
        self.base_url = (
            base_url
            or os.getenv(f"{env_prefix}_URL", "")
            or os.getenv("ATLASSIAN_URL", "")
        ).rstrip("/")

        self._username = (
            username
            or os.getenv(f"{env_prefix}_USERNAME")
            or os.getenv("ATLASSIAN_USERNAME")
        )
        self._password = (
            password
            or os.getenv(f"{env_prefix}_PASSWORD")
            or os.getenv("ATLASSIAN_PASSWORD")
        )

        self.timeout = timeout
        self.auto_login = auto_login
        self.auto_relogin = auto_relogin
        self.auth_mode = auth_mode
        self._oauth1_config = oauth1
        self.trust_env = trust_env

        # 验证必要参数
        if not self.base_url:
            raise ValueError(f"{env_prefix}_URL or ATLASSIAN_URL is required")
        if self.auth_mode not in ("session", "basic", "oauth1"):
            raise ValueError(f"Unsupported auth_mode: {self.auth_mode}")
        if self.auth_mode in ("session", "basic") and (
            not self._username or not self._password
        ):
            raise ValueError(
                f"{env_prefix}_USERNAME/{env_prefix}_PASSWORD or "
                "ATLASSIAN_USERNAME/ATLASSIAN_PASSWORD are required"
            )
        if self.auth_mode == "oauth1" and self._oauth1_config is None:
            raise ValueError("oauth1 configuration is required for auth_mode='oauth1'")

        # 会话状态
        self._session_info: Optional[SessionInfo] = None
        self._basic_auth_info: Optional[BasicAuthInfo] = None
        self._client: Optional[httpx.AsyncClient] = None
        self._logged_in: bool = False

        # Basic Auth 模式下，预先生成认证头
        if self.auth_mode == "basic":
            credentials = f"{self._username}:{self._password}"
            encoded = base64.b64encode(credentials.encode()).decode()
            self._basic_auth_info = BasicAuthInfo(
                username=self._username,
                auth_header=f"Basic {encoded}",
            )
            self._logged_in = True  # Basic Auth 不需要登录步骤
        elif self.auth_mode == "oauth1":
            self._logged_in = True  # OAuth access token 不需要登录步骤

    @property
    def is_logged_in(self) -> bool:
        """是否已登录"""
        if self.auth_mode == "session":
            return self._logged_in and self._session_info is not None
        return self._logged_in

    @property
    def session_info(self) -> Optional[SessionInfo]:
        """获取当前会话信息"""
        return self._session_info

    async def __aenter__(self) -> "BaseHttpClient":
        """异步上下文管理器入口"""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            follow_redirects=True,
            auth=self._get_httpx_auth(),
            trust_env=self.trust_env,
        )
        # Basic Auth 模式不需要登录
        if self.auth_mode == "session" and self.auto_login:
            await self.login()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """异步上下文管理器出口"""
        try:
            # Basic Auth 模式不需要注销
            if self.auth_mode == "session" and self._logged_in:
                await self.logout()
        finally:
            if self._client:
                await self._client.aclose()
                self._client = None

    def _get_client(self) -> httpx.AsyncClient:
        """获取 HTTP 客户端实例"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                follow_redirects=True,
                auth=self._get_httpx_auth(),
                trust_env=self.trust_env,
            )
        return self._client

    def _get_httpx_auth(self) -> Any:
        """获取需要参与完整请求签名的 HTTPX 认证对象。"""

        if self.auth_mode == "oauth1" and self._oauth1_config:
            return self._oauth1_config.create_httpx_auth()
        return None

    def _get_auth_headers(self) -> dict:
        """获取认证请求头"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.auth_mode == "basic" and self._basic_auth_info:
            headers["Authorization"] = self._basic_auth_info.auth_header
        elif self._session_info:
            headers["Cookie"] = f"{self._session_info.session_name}={self._session_info.session_value}"
        return headers

    async def login(self) -> SessionInfo | BasicAuthInfo | OAuth1Config:
        """
        登录并获取会话

        Session 模式: POST /rest/auth/1/session
        Basic Auth / OAuth 1.0a 模式: 返回当前认证配置

        Returns:
            SessionInfo | BasicAuthInfo | OAuth1Config: 认证信息

        Raises:
            AtlassianCaptchaError: 触发了 CAPTCHA 验证
            AtlassianAuthError: 认证失败
        """
        # Basic Auth 模式直接返回
        if self.auth_mode == "basic":
            if self._basic_auth_info:
                logger.info(f"Using Basic Auth for {self.base_url} as {self._username}")
                return self._basic_auth_info
            raise AtlassianAuthError("Basic Auth info not initialized")
        if self.auth_mode == "oauth1":
            if self._oauth1_config:
                logger.info(
                    "Using OAuth 1.0a for %s with consumer %s",
                    self.base_url,
                    self._oauth1_config.consumer_key,
                )
                return self._oauth1_config
            raise AtlassianAuthError("OAuth 1.0a config not initialized")

        client = self._get_client()

        payload = {
            "username": self._username,
            "password": self._password,
        }

        logger.info(f"Attempting login to {self.base_url} as {self._username}")

        response = await client.post(
            self.AUTH_SESSION_PATH,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

        # 检查 CAPTCHA
        login_reason = response.headers.get("X-Seraph-LoginReason", "")
        if login_reason in ("AUTHENTICATION_DENIED", "AUTHENTICATED_FAILED"):
            raise AtlassianCaptchaError(
                f"Login denied (possibly CAPTCHA triggered): {login_reason}. "
                "Please login via browser to resolve CAPTCHA."
            )

        if response.status_code == 401:
            error_msg = "Authentication failed"
            try:
                error_data = response.json()
                if "errorMessages" in error_data:
                    error_msg = "; ".join(error_data["errorMessages"])
            except Exception:
                pass
            raise AtlassianAuthError(f"Login failed: {error_msg}")

        response.raise_for_status()

        data = response.json()
        session_data = data.get("session", {})
        login_info = data.get("loginInfo", {})

        self._session_info = SessionInfo(
            session_name=session_data.get("name", "JSESSIONID"),
            session_value=session_data.get("value", ""),
            login_count=login_info.get("loginCount", 0),
            failed_login_count=login_info.get("failedLoginCount", 0),
            last_failed_login_time=login_info.get("lastFailedLoginTime"),
            previous_login_time=login_info.get("previousLoginTime"),
        )
        self._logged_in = True

        logger.info(f"Login successful. Login count: {self._session_info.login_count}")
        return self._session_info

    async def get_current_session(self) -> dict:
        """
        获取当前会话信息

        GET /rest/auth/1/session

        Returns:
            dict: 当前会话详情
        """
        if not self._session_info:
            raise AtlassianAuthError("Not logged in")

        client = self._get_client()
        response = await client.get(
            self.AUTH_SESSION_PATH,
            headers=self._get_auth_headers(),
        )

        if response.status_code == 401:
            self._logged_in = False
            raise AtlassianSessionExpiredError("Session expired")

        response.raise_for_status()
        return response.json()

    async def logout(self) -> bool:
        """
        注销当前会话

        DELETE /rest/auth/1/session

        Returns:
            bool: 是否成功注销
        """
        if not self._session_info:
            logger.warning("Logout called but not logged in")
            return False

        client = self._get_client()

        try:
            response = await client.delete(
                self.AUTH_SESSION_PATH,
                headers=self._get_auth_headers(),
            )
            response.raise_for_status()
            logger.info("Logout successful")
            return True
        except Exception as e:
            logger.warning(f"Logout failed: {e}")
            return False
        finally:
            self._session_info = None
            self._logged_in = False

    async def _ensure_logged_in(self) -> None:
        """确保已登录，必要时自动登录"""
        # Basic Auth 和 OAuth access token 不需要登录步骤
        if self.auth_mode in ("basic", "oauth1"):
            return

        if not self._logged_in and self.auto_login:
            await self.login()
        elif not self._logged_in:
            raise AtlassianAuthError("Not logged in and auto_login is disabled")

    def _handle_error_response(self, response: httpx.Response) -> None:
        """处理错误响应"""
        if response.status_code == 404:
            raise AtlassianNotFoundError(
                f"Resource not found: {response.url}",
                status_code=404,
            )
        elif response.status_code == 403:
            raise AtlassianPermissionError(
                f"Permission denied: {response.url}",
                status_code=403,
            )
        elif response.status_code >= 400:
            error_msg = f"API error: {response.status_code}"
            try:
                error_data = response.json()
                if "errorMessages" in error_data:
                    error_msg = "; ".join(error_data["errorMessages"])
                elif "message" in error_data:
                    error_msg = error_data["message"]
            except Exception:
                pass
            raise AtlassianAPIError(error_msg, status_code=response.status_code)

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs,
    ) -> httpx.Response:
        """
        发送 HTTP 请求，自动处理会话认证

        Args:
            method: HTTP 方法
            path: API 路径
            **kwargs: 传递给 httpx 的其他参数

        Returns:
            httpx.Response: 响应对象
        """
        await self._ensure_logged_in()

        client = self._get_client()

        # 合并请求头
        headers = self._get_auth_headers()
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))

        response = await client.request(
            method,
            path,
            headers=headers,
            **kwargs,
        )

        # 检查会话过期，尝试重新登录
        if (
            response.status_code == 401
            and self.auth_mode == "session"
            and self.auto_relogin
        ):
            logger.warning("Session expired, attempting re-login...")
            self._logged_in = False
            self._session_info = None
            await self.login()

            # 重新发送请求
            headers = self._get_auth_headers()
            if "headers" in kwargs:
                headers.update(kwargs.get("headers", {}))

            response = await client.request(
                method,
                path,
                headers=headers,
                **kwargs,
            )

        return response

    async def get(self, path: str, **kwargs) -> httpx.Response:
        """发送 GET 请求"""
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs) -> httpx.Response:
        """发送 POST 请求"""
        return await self._request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs) -> httpx.Response:
        """发送 PUT 请求"""
        return await self._request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs) -> httpx.Response:
        """发送 DELETE 请求"""
        return await self._request("DELETE", path, **kwargs)

    async def get_json(self, path: str, **kwargs) -> Any:
        """发送 GET 请求并返回 JSON"""
        response = await self.get(path, **kwargs)
        response.raise_for_status()
        return response.json()

    async def post_json(self, path: str, data: Any = None, **kwargs) -> Any:
        """发送 POST 请求并返回 JSON"""
        response = await self.post(path, json=data, **kwargs)
        response.raise_for_status()
        if response.status_code == 204:
            return None
        return response.json()

    async def put_json(self, path: str, data: Any = None, **kwargs) -> Any:
        """发送 PUT 请求并返回 JSON"""
        response = await self.put(path, json=data, **kwargs)
        response.raise_for_status()
        if response.status_code == 204:
            return None
        return response.json()

    async def delete_json(self, path: str, **kwargs) -> Any:
        """发送 DELETE 请求并返回 JSON（如有）"""
        response = await self.delete(path, **kwargs)
        response.raise_for_status()
        if response.status_code == 204:
            return None
        try:
            return response.json()
        except Exception:
            return None

    async def close(self) -> None:
        """关闭客户端（不注销会话）"""
        if self._client:
            await self._client.aclose()
            self._client = None
