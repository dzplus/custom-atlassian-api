"""
Base Resource - 资源基类

所有 API 资源类的基类
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from atlassian.common.client import BaseHttpClient


class BaseResource:
    """
    API 资源基类

    所有资源类继承此类，通过 client 访问 HTTP 方法
    """

    def __init__(self, client: "BaseHttpClient"):
        """
        初始化资源

        Args:
            client: BaseHttpClient 实例
        """
        self._client = client

    @property
    def client(self) -> "BaseHttpClient":
        """获取 HTTP 客户端"""
        return self._client
