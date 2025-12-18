"""
Login Test - 测试 Jira, Confluence, Tempo 的登录功能

使用前请设置环境变量:
- JIRA_URL, JIRA_USERNAME, JIRA_PASSWORD
- CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD
- TEMPO_URL (或使用 JIRA_URL), TEMPO_USERNAME, TEMPO_PASSWORD

或使用通用变量:
- ATLASSIAN_URL, ATLASSIAN_USERNAME, ATLASSIAN_PASSWORD

运行测试:
    uv run python -m tests.test_login
    uv run python -m tests.test_login --jira
    uv run python -m tests.test_login --confluence
    uv run python -m tests.test_login --tempo
    uv run python -m tests.test_login --all
"""

import asyncio
import argparse
import os
import sys
from typing import Optional

from atlassian.jira import JiraClient
from atlassian.confluence import ConfluenceClient
from atlassian.tempo import TempoClient
from atlassian.common.exceptions import (
    AtlassianAuthError,
    AtlassianCaptchaError,
)


class LoginTest:
    """登录测试类"""

    def __init__(self):
        self.results: dict[str, dict] = {}

    async def test_jira_login(
        self,
        url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> bool:
        """
        测试 Jira 登录 (Basic Auth)

        Args:
            url: Jira URL (可选，默认从环境变量读取)
            username: 用户名 (可选)
            password: 密码 (可选)

        Returns:
            bool: 登录是否成功
        """
        print("\n" + "=" * 50)
        print("Testing Jira Login (Basic Auth)")
        print("=" * 50)

        try:
            client = JiraClient(
                base_url=url,
                username=username,
                password=password,
            )

            print(f"URL: {client.base_url}")
            print(f"Username: {client._username}")
            print(f"Auth Mode: {client.auth_mode}")
            print("Verifying credentials...")

            # 使用上下文管理器
            async with client:
                # 获取当前用户信息验证
                user_data = await client.get_json("/rest/api/2/myself")
                display_name = user_data.get("displayName", user_data.get("name", "Unknown"))
                email = user_data.get("emailAddress", "")
                print(f"✓ Authentication successful!")
                print(f"  Current user: {display_name} ({email})")

            self.results["jira"] = {
                "success": True,
                "url": client.base_url,
                "user": display_name,
                "auth_mode": client.auth_mode,
            }
            return True

        except AtlassianCaptchaError as e:
            print(f"✗ CAPTCHA triggered: {e}")
            print("  Please login via browser to resolve CAPTCHA first.")
            self.results["jira"] = {"success": False, "error": "CAPTCHA"}
            return False

        except AtlassianAuthError as e:
            print(f"✗ Authentication failed: {e}")
            self.results["jira"] = {"success": False, "error": str(e)}
            return False

        except ValueError as e:
            print(f"✗ Configuration error: {e}")
            self.results["jira"] = {"success": False, "error": str(e)}
            return False

        except Exception as e:
            print(f"✗ Unexpected error: {type(e).__name__}: {e}")
            self.results["jira"] = {"success": False, "error": str(e)}
            return False

    async def test_confluence_login(
        self,
        url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> bool:
        """
        测试 Confluence 登录 (Basic Auth)

        Args:
            url: Confluence URL (可选，默认从环境变量读取)
            username: 用户名 (可选)
            password: 密码 (可选)

        Returns:
            bool: 登录是否成功
        """
        print("\n" + "=" * 50)
        print("Testing Confluence Login (Basic Auth)")
        print("=" * 50)

        try:
            # Confluence 默认使用 Basic Auth
            client = ConfluenceClient(
                base_url=url,
                username=username,
                password=password,
            )

            print(f"URL: {client.base_url}")
            print(f"Username: {client._username}")
            print(f"Auth Mode: {client.auth_mode}")
            print("Verifying credentials...")

            # 使用上下文管理器
            async with client:
                # 获取当前用户信息验证
                user_data = await client.get_current_user()
                display_name = user_data.get("displayName", user_data.get("username", "Unknown"))
                print(f"✓ Authentication successful!")
                print(f"  Current user: {display_name}")

                # 获取空间列表
                spaces = await client.get_spaces(limit=3)
                space_count = spaces.get("size", 0)
                print(f"  Spaces accessible: {space_count}+")

            self.results["confluence"] = {
                "success": True,
                "url": client.base_url,
                "user": display_name,
                "auth_mode": client.auth_mode,
            }
            return True

        except AtlassianAuthError as e:
            print(f"✗ Authentication failed: {e}")
            self.results["confluence"] = {"success": False, "error": str(e)}
            return False

        except ValueError as e:
            print(f"✗ Configuration error: {e}")
            self.results["confluence"] = {"success": False, "error": str(e)}
            return False

        except Exception as e:
            print(f"✗ Unexpected error: {type(e).__name__}: {e}")
            self.results["confluence"] = {"success": False, "error": str(e)}
            return False

    async def test_tempo_login(
        self,
        url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> bool:
        """
        测试 Tempo 登录 (Basic Auth)

        Tempo 是 Jira 插件，使用与 Jira 相同的认证

        Args:
            url: Jira URL (可选，默认从环境变量读取)
            username: 用户名 (可选)
            password: 密码 (可选)

        Returns:
            bool: 登录是否成功
        """
        print("\n" + "=" * 50)
        print("Testing Tempo Login (Basic Auth)")
        print("=" * 50)

        try:
            client = TempoClient(
                base_url=url,
                username=username,
                password=password,
            )

            print(f"URL: {client.base_url}")
            print(f"Username: {client._username}")
            print(f"Auth Mode: {client.auth_mode}")
            print("Verifying credentials...")

            # 使用上下文管理器
            async with client:
                # 获取团队列表验证 Tempo API 可用
                teams = await client.team.get_all_raw()
                team_count = len(teams) if isinstance(teams, list) else 0
                print(f"✓ Authentication successful!")
                print(f"  Teams accessible: {team_count}")

                # 尝试获取账户列表
                accounts = await client.account.get_all_raw()
                account_count = len(accounts) if isinstance(accounts, list) else 0
                print(f"  Accounts accessible: {account_count}")

            self.results["tempo"] = {
                "success": True,
                "url": client.base_url,
                "teams": team_count,
                "accounts": account_count,
                "auth_mode": client.auth_mode,
            }
            return True

        except AtlassianAuthError as e:
            print(f"✗ Authentication failed: {e}")
            self.results["tempo"] = {"success": False, "error": str(e)}
            return False

        except ValueError as e:
            print(f"✗ Configuration error: {e}")
            self.results["tempo"] = {"success": False, "error": str(e)}
            return False

        except Exception as e:
            print(f"✗ Unexpected error: {type(e).__name__}: {e}")
            self.results["tempo"] = {"success": False, "error": str(e)}
            return False

    async def run_all(self) -> dict[str, dict]:
        """运行所有登录测试"""
        await self.test_jira_login()
        await self.test_confluence_login()
        await self.test_tempo_login()
        return self.results

    def print_summary(self):
        """打印测试结果摘要"""
        print("\n" + "=" * 50)
        print("Test Summary")
        print("=" * 50)

        for product, result in self.results.items():
            status = "✓ PASSED" if result.get("success") else "✗ FAILED"
            print(f"{product.upper()}: {status}")
            if result.get("success"):
                print(f"  URL: {result.get('url')}")
                print(f"  User: {result.get('user')}")
            else:
                print(f"  Error: {result.get('error')}")

        # 总结
        passed = sum(1 for r in self.results.values() if r.get("success"))
        total = len(self.results)
        print(f"\nTotal: {passed}/{total} passed")


async def main():
    parser = argparse.ArgumentParser(description="Test Atlassian login")
    parser.add_argument("--jira", action="store_true", help="Test Jira login only")
    parser.add_argument("--confluence", action="store_true", help="Test Confluence login only")
    parser.add_argument("--tempo", action="store_true", help="Test Tempo login only")
    parser.add_argument("--all", action="store_true", help="Test all products")
    parser.add_argument("--url", help="Override URL")
    parser.add_argument("--username", "-u", help="Override username")
    parser.add_argument("--password", "-p", help="Override password")

    args = parser.parse_args()

    tester = LoginTest()

    # 默认行为：如果没有指定任何选项，提示用户
    if not args.jira and not args.confluence and not args.tempo and not args.all:
        print("Usage: python -m tests.test_login [--jira] [--confluence] [--tempo] [--all]")
        print("\nEnvironment variables needed:")
        print("  JIRA_URL, JIRA_USERNAME, JIRA_PASSWORD")
        print("  CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD")
        print("  TEMPO_URL (or JIRA_URL), TEMPO_USERNAME, TEMPO_PASSWORD")
        print("\nOr use common variables:")
        print("  ATLASSIAN_URL, ATLASSIAN_USERNAME, ATLASSIAN_PASSWORD")

        # 检查可用的环境变量
        print("\nDetected environment variables:")
        for var in ["JIRA_URL", "JIRA_USERNAME", "CONFLUENCE_URL", "CONFLUENCE_USERNAME",
                    "TEMPO_URL", "TEMPO_USERNAME", "ATLASSIAN_URL", "ATLASSIAN_USERNAME"]:
            value = os.getenv(var)
            if value:
                print(f"  {var}: {'*' * 8 if 'PASSWORD' in var else value}")

        return

    try:
        if args.all:
            await tester.run_all()
        else:
            if args.jira:
                await tester.test_jira_login(args.url, args.username, args.password)
            if args.confluence:
                await tester.test_confluence_login(args.url, args.username, args.password)
            if args.tempo:
                await tester.test_tempo_login(args.url, args.username, args.password)

        tester.print_summary()

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
