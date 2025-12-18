"""
Confluence 剩余方法测试 - 测试未覆盖的 API

测试内容：
1. user.get_raw() - 获取用户信息（原始JSON）
2. space.create() - 创建空间
3. space.create_raw() - 使用原始payload创建空间
4. content.create_raw() - 使用原始payload创建内容
5. content.update_raw() - 使用原始payload更新内容
6. content.add_attachment() - 上传附件（文件路径）
7. space.update() - 更新空间
8. space.update_raw() - 使用原始payload更新空间
9. space.delete() - 删除空间

注意：所有创建的测试空间都会在测试结束后清理

运行命令:
    uv run python -m tests.test_confluence_remaining
"""

import asyncio
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

from atlassian.confluence import ConfluenceClient
from atlassian.common.exceptions import AtlassianError


class RemainingMethodsTest:
    """剩余方法测试类"""

    def __init__(self):
        self.client: Optional[ConfluenceClient] = None
        self.test_results: dict[str, bool] = {}
        self.username: Optional[str] = None
        self.personal_space_key: Optional[str] = None

        # 测试空间 keys
        self.test_space_key: Optional[str] = None  # 通过 create() 创建
        self.test_space_raw_key: Optional[str] = None  # 通过 create_raw() 创建

        # 测试页面 IDs
        self.test_page_raw_id: Optional[str] = None

        self.passed_count = 0
        self.failed_count = 0

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
        print("Confluence 剩余方法测试")
        print("=" * 70)
        print()

        self.client = ConfluenceClient()
        print(f"URL: {self.client.base_url}")
        print(f"用户: {self.client._username}")

        # 获取当前用户信息
        user = await self.client.user.get_current()
        self.username = user.username
        self.personal_space_key = f"~{self.username}"
        print(f"个人空间: {self.personal_space_key}")
        print()

    # ========== 1. 用户方法测试 ==========

    async def test_user_methods(self):
        """测试用户相关方法"""
        print("[阶段1] 用户方法测试")
        print("-" * 70)

        # 1.1 user.get_raw() - 获取用户信息（原始JSON）
        try:
            user_data = await self.client.user.get_raw(username=self.username)
            self.log_test(
                "user.get_raw()",
                True,
                f"用户: {user_data.get('displayName')} (type: {user_data.get('type')})"
            )
        except Exception as e:
            self.log_test("user.get_raw()", False, str(e))

        print()

    # ========== 2. 空间创建测试 ==========

    async def test_space_creation(self):
        """测试空间创建方法"""
        print("[阶段2] 空间创建测试")
        print("-" * 70)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # 2.1 space.create() - 创建空间（标准方法）
        try:
            self.test_space_key = f"TEST{timestamp}"
            space = await self.client.space.create(
                key=self.test_space_key,
                name=f"测试空间 {timestamp}",
                description="通过 space.create() 创建的测试空间，测试完成后会自动删除"
            )
            self.log_test(
                "space.create()",
                True,
                f"空间key: {space.key}, 名称: {space.name}"
            )
        except Exception as e:
            self.log_test("space.create()", False, str(e))
            self.test_space_key = None

        # 2.2 space.create_raw() - 使用原始payload创建空间
        try:
            self.test_space_raw_key = f"RAW{timestamp}"
            payload = {
                "key": self.test_space_raw_key,
                "name": f"Raw测试空间 {timestamp}",
                "description": {
                    "plain": {
                        "value": "通过 space.create_raw() 创建的测试空间，测试完成后会自动删除",
                        "representation": "plain"
                    }
                }
            }
            space_data = await self.client.space.create_raw(payload)
            self.log_test(
                "space.create_raw()",
                True,
                f"空间key: {space_data.get('key')}, ID: {space_data.get('id')}"
            )
        except Exception as e:
            self.log_test("space.create_raw()", False, str(e))
            self.test_space_raw_key = None

        print()

    # ========== 3. 内容方法测试 ==========

    async def test_content_methods(self):
        """测试内容相关方法"""
        print("[阶段3] 内容方法测试")
        print("-" * 70)

        if not self.test_space_raw_key:
            print("  ⚠ 跳过: 未创建测试空间")
            return

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        # 3.1 content.create_raw() - 使用原始payload创建内容
        try:
            payload = {
                "type": "page",
                "title": f"[Raw方式] 测试页面 - {timestamp}",
                "space": {"key": self.test_space_raw_key},
                "body": {
                    "storage": {
                        "value": "<p>这是通过 <strong>content.create_raw()</strong> 创建的测试页面。</p>",
                        "representation": "storage"
                    }
                }
            }
            page_data = await self.client.content.create_raw(payload)
            self.test_page_raw_id = page_data.get('id')
            self.log_test(
                "content.create_raw()",
                True,
                f"页面ID: {self.test_page_raw_id}, 标题: {page_data.get('title')}"
            )
        except Exception as e:
            self.log_test("content.create_raw()", False, str(e))
            self.test_page_raw_id = None

        # 3.2 content.update_raw() - 使用原始payload更新内容
        if self.test_page_raw_id:
            try:
                # 先获取当前版本号
                page = await self.client.content.get(self.test_page_raw_id, expand="version")
                current_version = page.version.number if page.version else 1

                payload = {
                    "version": {"number": current_version + 1},
                    "type": "page",
                    "title": f"[Raw方式更新] 测试页面 - {timestamp}",
                    "body": {
                        "storage": {
                            "value": "<p>这个页面通过 <strong>content.update_raw()</strong> 更新了。</p><p>更新时间: " + datetime.now().isoformat() + "</p>",
                            "representation": "storage"
                        }
                    }
                }
                updated_data = await self.client.content.update_raw(self.test_page_raw_id, payload)
                self.log_test(
                    "content.update_raw()",
                    True,
                    f"新版本: {updated_data.get('version', {}).get('number')}"
                )
            except Exception as e:
                self.log_test("content.update_raw()", False, str(e))

        # 3.3 content.add_attachment() - 上传附件（从文件路径）
        if self.test_page_raw_id:
            try:
                # 创建临时测试文件
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                    f.write(f"测试附件内容\n创建时间: {datetime.now().isoformat()}\n")
                    f.write("这是通过 content.add_attachment() 上传的测试附件。\n")
                    temp_file_path = f.name

                # 上传附件
                attachments = await self.client.content.add_attachment(
                    self.test_page_raw_id,
                    file_path=temp_file_path,
                    comment="测试附件上传"
                )

                # 清理临时文件
                Path(temp_file_path).unlink()

                if attachments and attachments.results:
                    att = attachments.results[0]
                    self.log_test(
                        "content.add_attachment()",
                        True,
                        f"文件: {att.title}, 大小: {att.extensions.get('fileSize') if att.extensions else 'N/A'} bytes"
                    )
                else:
                    self.log_test("content.add_attachment()", True, "上传成功")
            except Exception as e:
                self.log_test("content.add_attachment()", False, str(e))

        print()

    # ========== 4. 空间更新测试 ==========

    async def test_space_update(self):
        """测试空间更新方法"""
        print("[阶段4] 空间更新测试")
        print("-" * 70)

        # 4.1 space.update() - 更新空间（标准方法）
        if self.test_space_key:
            try:
                updated_space = await self.client.space.update(
                    self.test_space_key,
                    name=f"更新后的测试空间",
                    description="通过 space.update() 更新的空间描述"
                )
                self.log_test(
                    "space.update()",
                    True,
                    f"新名称: {updated_space.name}"
                )
            except Exception as e:
                self.log_test("space.update()", False, str(e))

        # 4.2 space.update_raw() - 使用原始payload更新空间
        if self.test_space_raw_key:
            try:
                # 先获取空间信息获取版本号
                space_data = await self.client.space.get_raw(self.test_space_raw_key)
                current_version = space_data.get('version', {}).get('number', 1)

                payload = {
                    "name": f"Raw方式更新的空间",
                    "description": {
                        "plain": {
                            "value": f"通过 space.update_raw() 更新，时间: {datetime.now().isoformat()}",
                            "representation": "plain"
                        }
                    },
                    "version": {"number": current_version + 1}
                }
                updated_data = await self.client.space.update_raw(self.test_space_raw_key, payload)
                self.log_test(
                    "space.update_raw()",
                    True,
                    f"新版本: {updated_data.get('version', {}).get('number')}"
                )
            except Exception as e:
                self.log_test("space.update_raw()", False, str(e))

        print()

    # ========== 5. 清理测试数据 ==========

    async def test_cleanup(self):
        """清理测试数据"""
        print("[阶段5] 清理测试数据")
        print("-" * 70)

        # 5.1 删除标准方式创建的空间
        if self.test_space_key:
            try:
                result = await self.client.space.delete(self.test_space_key)
                self.log_test(
                    "space.delete() [标准空间]",
                    True,
                    f"空间key: {self.test_space_key}"
                )
            except Exception as e:
                self.log_test("space.delete() [标准空间]", False, str(e))

        # 5.2 删除raw方式创建的空间
        if self.test_space_raw_key:
            try:
                result = await self.client.space.delete(self.test_space_raw_key)
                self.log_test(
                    "space.delete() [Raw空间]",
                    True,
                    f"空间key: {self.test_space_raw_key}"
                )
            except Exception as e:
                self.log_test("space.delete() [Raw空间]", False, str(e))

        print()

    # ========== 主测试流程 ==========

    async def run_all_tests(self):
        """运行所有测试"""
        try:
            await self.setup()

            async with self.client:
                await self.test_user_methods()
                await self.test_space_creation()
                await self.test_content_methods()
                await self.test_space_update()
                await self.test_cleanup()

            # 打印总结
            self.print_summary()

        except Exception as e:
            print(f"\n测试执行失败: {e}")
            sys.exit(1)

    def print_summary(self):
        """打印测试总结"""
        print("=" * 70)
        print("测试总结")
        print("=" * 70)
        print(f"✓ 通过: {self.passed_count}")
        print(f"✗ 失败: {self.failed_count}")
        print(f"总计: {self.passed_count + self.failed_count}")
        if self.passed_count + self.failed_count > 0:
            print(f"成功率: {self.passed_count / (self.passed_count + self.failed_count) * 100:.1f}%")
        print()


async def main():
    """主函数"""
    tester = RemainingMethodsTest()

    try:
        await tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n测试异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
