"""
Confluence 新增API测试 - 测试新实现的资源和方法

测试内容：
1. Group（用户组）API - 3个方法
2. Audit（审计）API - 6个方法
3. LongTask（长期任务）API - 2个方法
4. Content 扩展 API - 7个方法
5. User 扩展 API - 1个方法

运行命令:
    uv run python -m tests.test_confluence_new_apis
"""

import asyncio
import sys
from typing import Optional

from atlassian.confluence import ConfluenceClient
from atlassian.common.exceptions import AtlassianError


class NewAPIsTest:
    """新增API测试类"""

    def __init__(self):
        self.client: Optional[ConfluenceClient] = None
        self.test_results: dict[str, bool] = {}
        self.passed_count = 0
        self.failed_count = 0
        self.test_content_id: Optional[str] = None

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
        print("Confluence 新增API测试")
        print("=" * 70)
        print()

        self.client = ConfluenceClient()
        print(f"URL: {self.client.base_url}")
        print(f"用户: {self.client._username}")
        print()

    # ========== 1. Group API 测试 ==========

    async def test_group_apis(self):
        """测试用户组 API"""
        print("[阶段1] 用户组(Group) API 测试")
        print("-" * 70)

        # 1.1 获取所有用户组
        try:
            groups = await self.client.group.get_all(limit=10)
            group_count = groups.get("size", 0)
            self.log_test(
                "group.get_all()",
                True,
                f"获取到 {group_count} 个用户组"
            )

            # 保存第一个组名用于后续测试
            if groups.get("results"):
                test_group_name = groups["results"][0]["name"]
            else:
                test_group_name = "confluence-users"  # fallback
        except Exception as e:
            self.log_test("group.get_all()", False, str(e))
            test_group_name = "confluence-users"

        # 1.2 获取指定用户组
        try:
            group_info = await self.client.group.get(test_group_name)
            self.log_test(
                "group.get(group_name)",
                True,
                f"组名: {group_info.get('name')}"
            )
        except Exception as e:
            self.log_test("group.get(group_name)", False, str(e))

        # 1.3 获取组成员
        try:
            members = await self.client.group.get_members(test_group_name, limit=10)
            member_count = members.get("size", 0)
            self.log_test(
                "group.get_members()",
                True,
                f"组 '{test_group_name}' 有 {member_count} 个成员"
            )
        except Exception as e:
            self.log_test("group.get_members()", False, str(e))

        print()

    # ========== 2. Audit API 测试 ==========

    async def test_audit_apis(self):
        """测试审计 API（需要管理员权限）"""
        print("[阶段2] 审计(Audit) API 测试")
        print("-" * 70)

        # 2.1 获取审计记录
        try:
            audit_records = await self.client.audit.get_all(limit=10)
            record_count = audit_records.get("size", 0)
            self.log_test(
                "audit.get_all()",
                True,
                f"获取到 {record_count} 条审计记录"
            )
        except AtlassianError as e:
            if "403" in str(e) or "401" in str(e):
                self.log_test("audit.get_all()", False, "需要管理员权限")
            else:
                self.log_test("audit.get_all()", False, str(e))
        except Exception as e:
            self.log_test("audit.get_all()", False, str(e))

        # 2.2 获取审计保留期设置
        try:
            retention = await self.client.audit.get_retention()
            self.log_test(
                "audit.get_retention()",
                True,
                f"保留期: {retention.get('number')} {retention.get('units')}"
            )
        except AtlassianError as e:
            if "403" in str(e) or "401" in str(e):
                self.log_test("audit.get_retention()", False, "需要管理员权限")
            else:
                self.log_test("audit.get_retention()", False, str(e))
        except Exception as e:
            self.log_test("audit.get_retention()", False, str(e))

        # 2.3 获取最近时间范围内的审计记录
        try:
            recent_records = await self.client.audit.get_since(
                number=7,
                units="DAYS",
                limit=5
            )
            record_count = recent_records.get("size", 0)
            self.log_test(
                "audit.get_since()",
                True,
                f"最近7天有 {record_count} 条记录"
            )
        except AtlassianError as e:
            if "403" in str(e) or "401" in str(e):
                self.log_test("audit.get_since()", False, "需要管理员权限")
            else:
                self.log_test("audit.get_since()", False, str(e))
        except Exception as e:
            self.log_test("audit.get_since()", False, str(e))

        # 注意: create(), set_retention(), export() 这些写入操作不在测试中调用
        print("  ℹ audit.create(), audit.set_retention(), audit.export() 跳过（写入操作）")
        print()

    # ========== 3. LongTask API 测试 ==========

    async def test_longtask_apis(self):
        """测试长期任务 API"""
        print("[阶段3] 长期任务(LongTask) API 测试")
        print("-" * 70)

        # 3.1 获取所有长期任务
        try:
            tasks = await self.client.longtask.get_all(limit=10)
            task_count = tasks.get("size", 0)
            self.log_test(
                "longtask.get_all()",
                True,
                f"当前有 {task_count} 个长期任务"
            )

            # 保存任务ID用于后续测试
            test_task_id = None
            if tasks.get("results"):
                test_task_id = tasks["results"][0].get("id")
        except Exception as e:
            self.log_test("longtask.get_all()", False, str(e))
            test_task_id = None

        # 3.2 获取指定任务详情
        if test_task_id:
            try:
                task = await self.client.longtask.get(test_task_id)
                self.log_test(
                    "longtask.get(task_id)",
                    True,
                    f"任务ID: {task.get('id')}, 完成度: {task.get('percentageComplete')}%"
                )
            except Exception as e:
                self.log_test("longtask.get(task_id)", False, str(e))
        else:
            print("  ℹ longtask.get(task_id) 跳过（无可用任务ID）")

        print()

    # ========== 4. Content 扩展 API 测试 ==========

    async def test_content_extended_apis(self):
        """测试 Content 扩展 API"""
        print("[阶段4] Content 扩展 API 测试")
        print("-" * 70)

        # 首先获取一个测试用的内容ID
        try:
            search_result = await self.client.search.search("type=page", limit=1)
            if search_result.results:
                self.test_content_id = search_result.results[0].content.id
        except Exception as e:
            print(f"  ℹ 无法获取测试内容: {e}")

        # 4.1 获取内容历史
        if self.test_content_id:
            try:
                history = await self.client.content.get_history(self.test_content_id)
                is_latest = history.get('latest', False)
                created_date = history.get('createdDate', 'N/A')
                self.log_test(
                    "content.get_history()",
                    True,
                    f"内容ID: {self.test_content_id}, 最新版本: {is_latest}, 创建时间: {created_date}"
                )
            except Exception as e:
                self.log_test("content.get_history()", False, str(e))
        else:
            print("  ℹ content.get_history() 跳过（无可用内容ID）")

        # 4.2 ContentBody Convert API
        try:
            converted = await self.client.content.convert_contentbody(
                value="<p>Test</p>",
                representation_from="storage",
                representation_to="view"
            )
            self.log_test(
                "content.convert_contentbody()",
                True,
                f"转换成功，结果长度: {len(converted.get('value', ''))}"
            )
        except Exception as e:
            self.log_test("content.convert_contentbody()", False, str(e))

        # 注意: update_attachment(), update_attachment_data(), publish_*_draft() 需要特定条件
        print("  ℹ content.update_attachment*(), publish_*_draft() 跳过（需要特定条件）")
        print()

    # ========== 5. User 扩展 API 测试 ==========

    async def test_user_extended_apis(self):
        """测试 User 扩展 API"""
        print("[阶段5] User 扩展 API 测试")
        print("-" * 70)

        # 获取当前用户名
        try:
            current_user = await self.client.user.get_current()
            username = current_user.username
        except Exception as e:
            print(f"  ℹ 无法获取当前用户: {e}")
            username = None

        # 5.1 获取用户所属组
        try:
            if username:
                groups = await self.client.user.get_member_of(username=username, limit=10)
            else:
                groups = await self.client.user.get_member_of(limit=10)
            group_count = groups.get("size", 0)
            self.log_test(
                "user.get_member_of()",
                True,
                f"当前用户属于 {group_count} 个用户组"
            )
            if groups.get("results"):
                group_names = [g.get("name") for g in groups["results"][:3]]
                print(f"    组: {', '.join(group_names)}")
        except Exception as e:
            self.log_test("user.get_member_of()", False, str(e))

        print()

    # ========== 运行所有测试 ==========

    async def run_all_tests(self):
        """运行所有测试"""
        await self.setup()

        async with self.client:
            await self.test_group_apis()
            await self.test_audit_apis()
            await self.test_longtask_apis()
            await self.test_content_extended_apis()
            await self.test_user_extended_apis()

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
            return 1


async def main():
    """主函数"""
    test = NewAPIsTest()
    exit_code = await test.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    asyncio.run(main())
