"""
Confluence 7.x 新增API测试 - 测试 7.0+ 版本的新功能

测试内容：
1. Webhook API - 9个方法
2. AccessMode API - 1个方法
3. Audit API 路径兼容性测试

运行命令:
    uv run python -m tests.test_confluence_7x_apis
"""

import asyncio
import sys
from typing import Optional

from atlassian.confluence import ConfluenceClient
from atlassian.common.exceptions import AtlassianError


class Confluence7xAPIsTest:
    """Confluence 7.x 新增API测试类"""

    def __init__(self):
        self.client: Optional[ConfluenceClient] = None
        self.test_results: dict[str, bool] = {}
        self.passed_count = 0
        self.failed_count = 0
        self.test_webhook_id: Optional[str] = None

    def log_test(self, test_name: str, success: bool, message: str = ""):
        """记录测试结果"""
        self.test_results[test_name] = success
        if success:
            self.passed_count += 1
            print(f"  ✓ {test_name}")
            if message:
                print(f"    {message}")
        else:
            self.failed_count += 1
            print(f"  ✗ {test_name}")
            if message:
                print(f"    错误: {message}")

    async def setup(self):
        """初始化"""
        print("=" * 70)
        print("Confluence 7.x 新增API测试")
        print("=" * 70)
        print()

        self.client = ConfluenceClient()
        print(f"URL: {self.client.base_url}")
        print(f"用户: {self.client._username}")
        print()

    # ========== 1. AccessMode API 测试 ==========

    async def test_accessmode_api(self):
        """测试访问模式 API"""
        print("[阶段1] 访问模式(AccessMode) API 测试")
        print("-" * 70)

        # 1.1 获取访问模式
        try:
            access_mode = await self.client.accessmode.get()
            # AccessMode API 可能返回字符串或字典
            if isinstance(access_mode, str):
                self.log_test(
                    "accessmode.get()",
                    True,
                    f"访问模式: {access_mode}"
                )
            else:
                mode = access_mode.get("mode", "UNKNOWN")
                read_only = access_mode.get("readOnly", False)
                self.log_test(
                    "accessmode.get()",
                    True,
                    f"访问模式: {mode}, 只读: {read_only}"
                )
        except AtlassianError as e:
            if "404" in str(e):
                self.log_test("accessmode.get()", False, "API 不可用（需要 Confluence 7.0+）")
            else:
                self.log_test("accessmode.get()", False, str(e))
        except Exception as e:
            self.log_test("accessmode.get()", False, str(e))

        print()

    # ========== 2. Webhook API 测试 ==========

    async def test_webhook_api(self):
        """测试 Webhook API"""
        print("[阶段2] Webhook API 测试")
        print("-" * 70)

        # 2.1 获取所有 webhooks
        try:
            webhooks = await self.client.webhook.get_all(limit=10)
            webhook_count = webhooks.get("size", 0)
            self.log_test(
                "webhook.get_all()",
                True,
                f"当前有 {webhook_count} 个 webhooks"
            )

            # 保存第一个 webhook ID 用于后续测试
            if webhooks.get("results"):
                self.test_webhook_id = webhooks["results"][0].get("id")
        except AtlassianError as e:
            if "404" in str(e):
                self.log_test("webhook.get_all()", False, "API 不可用（需要 Confluence 7.0+）")
            elif "403" in str(e) or "401" in str(e):
                self.log_test("webhook.get_all()", False, "需要管理员权限")
            else:
                self.log_test("webhook.get_all()", False, str(e))
        except Exception as e:
            self.log_test("webhook.get_all()", False, str(e))

        # 2.2 获取指定 webhook
        if self.test_webhook_id:
            try:
                webhook = await self.client.webhook.get(self.test_webhook_id)
                self.log_test(
                    "webhook.get(webhook_id)",
                    True,
                    f"Webhook 名称: {webhook.get('name')}"
                )
            except Exception as e:
                self.log_test("webhook.get(webhook_id)", False, str(e))
        else:
            print("  ℹ webhook.get(webhook_id) 跳过（无可用 webhook ID）")

        # 2.3 获取 webhook 统计摘要
        if self.test_webhook_id:
            try:
                summary = await self.client.webhook.get_statistics_summary(
                    self.test_webhook_id
                )
                total = summary.get("totalInvocations", 0)
                self.log_test(
                    "webhook.get_statistics_summary()",
                    True,
                    f"总调用次数: {total}"
                )
            except Exception as e:
                self.log_test("webhook.get_statistics_summary()", False, str(e))
        else:
            print("  ℹ webhook.get_statistics_summary() 跳过（无可用 webhook ID）")

        # 2.4 获取最近调用记录
        if self.test_webhook_id:
            try:
                invocations = await self.client.webhook.get_latest_invocations(
                    self.test_webhook_id,
                    limit=5
                )
                count = invocations.get("size", 0)
                self.log_test(
                    "webhook.get_latest_invocations()",
                    True,
                    f"最近 {count} 次调用"
                )
            except Exception as e:
                self.log_test("webhook.get_latest_invocations()", False, str(e))
        else:
            print("  ℹ webhook.get_latest_invocations() 跳过（无可用 webhook ID）")

        # 2.5 获取 webhook 统计信息
        if self.test_webhook_id:
            try:
                statistics = await self.client.webhook.get_statistics(
                    self.test_webhook_id,
                    limit=5
                )
                count = statistics.get("size", 0)
                self.log_test(
                    "webhook.get_statistics()",
                    True,
                    f"统计信息: {count} 条记录"
                )
            except Exception as e:
                self.log_test("webhook.get_statistics()", False, str(e))
        else:
            print("  ℹ webhook.get_statistics() 跳过（无可用 webhook ID）")

        # 2.6 测试端点连接性
        try:
            test_result = await self.client.webhook.test("https://httpbin.org/post")
            status_code = test_result.get("statusCode", 0)
            self.log_test(
                "webhook.test()",
                True,
                f"测试连接成功，状态码: {status_code}"
            )
        except AtlassianError as e:
            if "404" in str(e):
                self.log_test("webhook.test()", False, "API 不可用（需要 Confluence 7.0+）")
            elif "403" in str(e) or "401" in str(e):
                self.log_test("webhook.test()", False, "需要管理员权限")
            else:
                self.log_test("webhook.test()", False, str(e))
        except Exception as e:
            self.log_test("webhook.test()", False, str(e))

        # 注意: create(), update(), delete() 这些写入操作不在测试中调用
        print("  ℹ webhook.create(), update(), delete() 跳过（写入操作）")
        print()

    # ========== 3. Audit API 路径测试 ==========

    async def test_audit_api_path(self):
        """测试 Audit API 路径（7.x 使用 /rest/api/audit）"""
        print("[阶段3] Audit API 路径测试")
        print("-" * 70)

        # 3.1 测试新路径 /rest/api/audit
        try:
            audit_records = await self.client.audit.get_all(limit=5)
            record_count = audit_records.get("size", 0)
            self.log_test(
                "audit.get_all() [/rest/api/audit]",
                True,
                f"获取到 {record_count} 条审计记录（使用 7.x 路径）"
            )
        except AtlassianError as e:
            if "404" in str(e):
                self.log_test(
                    "audit.get_all() [/rest/api/audit]",
                    False,
                    "路径不可用（可能是旧版本 Confluence 6.x，需要使用 /rest/audit）"
                )
            elif "403" in str(e) or "401" in str(e):
                self.log_test("audit.get_all() [/rest/api/audit]", False, "需要管理员权限")
            else:
                self.log_test("audit.get_all() [/rest/api/audit]", False, str(e))
        except Exception as e:
            self.log_test("audit.get_all() [/rest/api/audit]", False, str(e))

        print()

    # ========== 运行所有测试 ==========

    async def run_all_tests(self):
        """运行所有测试"""
        await self.setup()

        async with self.client:
            await self.test_accessmode_api()
            await self.test_webhook_api()
            await self.test_audit_api_path()

        # 输出测试总结
        print("=" * 70)
        print("测试总结")
        print("=" * 70)
        print(f"总计: {self.passed_count + self.failed_count} 个测试")
        print(f"✓ 成功: {self.passed_count}")
        print(f"✗ 失败: {self.failed_count}")

        if self.failed_count == 0:
            print("\n🎉 所有测试通过！")
            return 0
        else:
            print(f"\n⚠️  有 {self.failed_count} 个测试失败")
            print("\n失败的测试:")
            for test_name, success in self.test_results.items():
                if not success:
                    print(f"  - {test_name}")

            print("\n💡 注意:")
            print("  - Webhook 和 AccessMode API 需要 Confluence 7.0+ 版本")
            print("  - Audit API 在 7.0+ 使用路径 /rest/api/audit")
            print("  - 如果服务器是 6.x 版本，这些 API 可能不可用（404 错误）")
            return 1


async def main():
    """主函数"""
    test = Confluence7xAPIsTest()
    exit_code = await test.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    asyncio.run(main())
