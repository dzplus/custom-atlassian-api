"""
Confluence API 接口测试

测试 Confluence 的各项 API 功能：
- 用户信息获取
- 空间列表和详情
- 内容搜索和获取
- 页面创建和更新（在个人空间）
- 附件上传
- 标签管理

使用前请设置环境变量:
- CONFLUENCE_URL: Confluence 服务地址
- CONFLUENCE_USERNAME: 用户名
- CONFLUENCE_PASSWORD: 密码

或使用通用变量:
- ATLASSIAN_URL, ATLASSIAN_USERNAME, ATLASSIAN_PASSWORD

运行测试:
    uv run python -m tests.test_confluence
    uv run python -m tests.test_confluence --read-only  # 仅读取测试
    uv run python -m tests.test_confluence --full       # 完整测试（包含写入）
"""

import asyncio
import argparse
import sys
from typing import Any, Optional
from datetime import datetime

from atlassian.confluence import ConfluenceClient
from atlassian.confluence.resources.content import ContentResource
from atlassian.common.exceptions import (
    AtlassianAuthError,
    AtlassianAPIError,
    AtlassianNotFoundError,
)


class ConfluenceAPITest:
    """Confluence API 测试类"""

    def __init__(self):
        self.client: Optional[ConfluenceClient] = None
        self.test_results: dict[str, dict] = {}
        self.personal_space_key: Optional[str] = None
        self.test_page_id: Optional[str] = None

    async def setup(
        self,
        url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """初始化客户端"""
        print("=" * 60)
        print("Confluence API Test Suite")
        print("=" * 60)

        self.client = ConfluenceClient(
            base_url=url,
            username=username,
            password=password,
        )

        print(f"URL: {self.client.base_url}")
        print(f"Username: {self.client._username}")
        print(f"Auth Mode: {self.client.auth_mode}")
        print()

    async def test_get_current_user(self) -> bool:
        """测试：获取当前用户信息"""
        test_name = "获取当前用户信息"
        print(f"[TEST] {test_name}")
        print("-" * 60)

        try:
            user_data = await self.client.user.get_current_raw()

            username = user_data.get("username", "N/A")
            display_name = user_data.get("displayName", "N/A")
            email = user_data.get("email", "N/A")
            user_key = user_data.get("userKey", "N/A")

            print(f"✓ 成功获取用户信息")
            print(f"  用户名: {username}")
            print(f"  显示名: {display_name}")
            print(f"  邮箱: {email}")
            print(f"  用户Key: {user_key}")

            # 个人空间 key 使用 ~username，而不是 ~userKey
            self.personal_space_key = f"~{username}" if username != "N/A" else None
            if self.personal_space_key:
                print(f"  个人空间Key: {self.personal_space_key}")

            self.test_results[test_name] = {"success": True, "user": display_name}
            return True

        except Exception as e:
            print(f"✗ 失败: {type(e).__name__}: {e}")
            self.test_results[test_name] = {"success": False, "error": str(e)}
            return False

    async def test_get_spaces(self) -> bool:
        """测试：获取空间列表"""
        test_name = "获取空间列表"
        print(f"\n[TEST] {test_name}")
        print("-" * 60)

        try:
            # 使用 Space Resource 获取空间列表
            space_list = await self.client.space.get_all(limit=5)

            spaces = space_list.results
            total = space_list.size

            print(f"✓ 成功获取空间列表")
            print(f"  总数: {total}")
            print(f"  显示前 {len(spaces)} 个空间:")

            for space in spaces:
                print(f"    - {space.name} (Key: {space.key}, Type: {space.type})")

            self.test_results[test_name] = {"success": True, "count": total}
            return True

        except Exception as e:
            print(f"✗ 失败: {type(e).__name__}: {e}")
            self.test_results[test_name] = {"success": False, "error": str(e)}
            return False

    async def test_get_personal_space(self) -> bool:
        """测试：获取个人空间详情"""
        test_name = "获取个人空间详情"
        print(f"\n[TEST] {test_name}")
        print("-" * 60)

        if not self.personal_space_key:
            print("⚠ 跳过: 未找到个人空间 key")
            self.test_results[test_name] = {"success": False, "error": "No personal space key"}
            return False

        try:
            space = await self.client.space.get(
                self.personal_space_key,
                expand="description,homepage"
            )

            print(f"✓ 成功获取个人空间")
            print(f"  名称: {space.name}")
            print(f"  Key: {space.key}")
            print(f"  类型: {space.type}")
            if space.description:
                desc_text = space.description.plain.value if space.description.plain else "N/A"
                print(f"  描述: {desc_text[:100]}...")

            # 获取个人空间的页面结构
            print(f"\n  获取空间页面结构...")
            try:
                # 获取空间中的所有页面（包括已删除和草稿）
                pages = await self.client.space.get_content_by_type(
                    self.personal_space_key,
                    content_type="page",
                    depth="all",
                    expand="ancestors",
                    limit=100
                )

                print(f"  API 返回页面总数: {pages.size}")

                # 统计不同状态的页面
                status_count = {}
                for page in pages.results:
                    status = page.status or 'unknown'
                    status_count[status] = status_count.get(status, 0) + 1

                if status_count:
                    status_str = ", ".join([f"{status}: {count}" for status, count in status_count.items()])
                    print(f"  页面状态分布: {status_str}")

                if pages.results:
                    print(f"\n  页面列表:")

                    # 构建页面层级结构
                    page_dict = {}
                    root_pages = []

                    for page in pages.results:
                        page_dict[page.id] = {
                            'id': page.id,
                            'title': page.title,
                            'status': page.status,
                            'ancestors': page.ancestors if page.ancestors else [],
                            'children': []
                        }

                    # 找出根页面和建立父子关系
                    for page_info in page_dict.values():
                        if not page_info['ancestors']:
                            root_pages.append(page_info)
                        else:
                            # 找到直接父页面（ancestors 是字典列表）
                            parent_id = page_info['ancestors'][-1].get('id') if page_info['ancestors'] else None
                            if parent_id and parent_id in page_dict:
                                page_dict[parent_id]['children'].append(page_info)

                    # 递归打印页面树
                    def print_page_tree(page_info, indent=0):
                        prefix = "    " + "  " * indent + "└─ "
                        status_marker = ""
                        if page_info.get('status'):
                            if page_info['status'] == 'trashed':
                                status_marker = " [已删除]"
                            elif page_info['status'] == 'draft':
                                status_marker = " [草稿]"
                        print(f"{prefix}{page_info['title']} (ID: {page_info['id']}){status_marker}")
                        for child in page_info['children']:
                            print_page_tree(child, indent + 1)

                    if root_pages:
                        for root in root_pages:
                            print_page_tree(root)
                    else:
                        # 如果没有根页面，可能所有页面都有父页面但父页面不在当前空间
                        for page in pages.results[:10]:  # 只显示前10个
                            ancestors_str = " > ".join([a.get('title', 'N/A') for a in page.ancestors]) if page.ancestors else "无"
                            print(f"    - {page.title} (ID: {page.id})")
                            if page.ancestors:
                                print(f"      父页面: {ancestors_str}")
                else:
                    print(f"    (空间中暂无页面)")

            except Exception as e:
                print(f"  ⚠ 获取页面结构失败: {e}")

            self.test_results[test_name] = {"success": True, "space_key": space.key}
            return True

        except AtlassianNotFoundError:
            print(f"⚠ 个人空间不存在: {self.personal_space_key}")
            print("  提示: 需要先在 Confluence 中创建个人空间")
            self.test_results[test_name] = {"success": False, "error": "Personal space not found"}
            return False

        except Exception as e:
            print(f"✗ 失败: {type(e).__name__}: {e}")
            self.test_results[test_name] = {"success": False, "error": str(e)}
            return False

    async def test_search_content(self) -> bool:
        """测试：搜索内容"""
        test_name = "搜索内容"
        print(f"\n[TEST] {test_name}")
        print("-" * 60)

        try:
            # 搜索所有页面
            cql = "type=page"
            results = await self.client.content.search(cql, limit=5)

            pages = results.results
            total = results.size

            print(f"✓ 成功搜索内容")
            print(f"  CQL: {cql}")
            print(f"  总数: {total}")
            print(f"  显示前 {len(pages)} 个结果:")

            for page in pages:
                space_key = page.space.key if page.space else "N/A"
                print(f"    - {page.title} (ID: {page.id}, Space: {space_key})")

            self.test_results[test_name] = {"success": True, "count": total}
            return True

        except Exception as e:
            print(f"✗ 失败: {type(e).__name__}: {e}")
            self.test_results[test_name] = {"success": False, "error": str(e)}
            return False

    async def test_get_notifications(self) -> bool:
        """测试：获取当前用户的所有通知"""
        test_name = "获取用户通知"
        print(f"\n[TEST] {test_name}")
        print("-" * 60)

        try:
            # 检查是否安装了 MyWork 插件
            print("  检查 MyWork 插件...")

            # 1. 获取未读通知数量
            try:
                status = await self.client.notification.get_unread_count()
                unread_count = status.get('count', 0)
                timeout = status.get('timeout', 60)

                print(f"✓ MyWork 插件已安装")
                print(f"  未读通知数量: {unread_count}")
                print(f"  建议轮询间隔: {timeout} 秒")

            except Exception as e:
                if "404" in str(e):
                    print(f"⚠ MyWork 插件未安装")
                    print(f"  提示: 需要安装 MyWork Confluence Host Plugin 插件才能使用通知 API")
                    self.test_results[test_name] = {
                        "success": False,
                        "error": "MyWork plugin not installed"
                    }
                    return False
                raise

            # 2. 获取通知列表
            print(f"\n  获取通知列表...")
            notifications = await self.client.notification.get_all(limit=20)

            print(f"✓ 成功获取通知列表")
            print(f"  通知总数: {len(notifications)}")

            if notifications:
                print(f"\n  最近的通知:")

                # 统计通知类型
                unread_notifications = []
                notification_types = {}

                for notif in notifications[:10]:  # 只显示前10条
                    notif_id = notif.get('id')
                    title = notif.get('title', 'N/A')
                    entity = notif.get('entity', 'unknown')
                    action = notif.get('action', 'unknown')
                    is_read = notif.get('read', False)
                    created = notif.get('created', 'N/A')

                    # 统计类型
                    notif_type = f"{entity}:{action}"
                    notification_types[notif_type] = notification_types.get(notif_type, 0) + 1

                    # 收集未读通知
                    if not is_read:
                        unread_notifications.append(notif)

                    # 显示通知信息
                    read_marker = "✓" if is_read else "📬"
                    print(f"    {read_marker} 通知 #{notif_id}")
                    print(f"       标题: {title}")
                    print(f"       类型: {entity} - {action}")
                    print(f"       时间: {created}")

                    # 显示关联项目信息
                    item = notif.get('item', {})
                    if item and item.get('title'):
                        print(f"       关联: {item.get('title')}")

                    print()

                # 显示统计信息
                print(f"  通知统计:")
                print(f"    未读: {len(unread_notifications)} 条")
                print(f"    已读: {len(notifications) - len(unread_notifications)} 条")

                print(f"\n  通知类型分布:")
                for notif_type, count in notification_types.items():
                    print(f"    {notif_type}: {count} 条")

                # 3. 测试获取嵌套（分组）通知
                print(f"\n  获取分组通知...")
                nested = await self.client.notification.get_nested(limit=10)

                print(f"✓ 成功获取分组通知")
                print(f"  分组数量: {len(nested)}")

                if nested:
                    print(f"\n  分组详情（前3组）:")
                    for i, group in enumerate(nested[:3], 1):
                        item = group.get('item', {})
                        notifs = group.get('notifications', [])

                        print(f"    [{i}] {item.get('title', 'N/A')}")
                        print(f"        通知数: {len(notifs)} 条")
                        if notifs:
                            unread_in_group = sum(1 for n in notifs if not n.get('read'))
                            print(f"        未读: {unread_in_group} 条")

            else:
                print(f"  (暂无通知)")

            self.test_results[test_name] = {
                "success": True,
                "total": len(notifications),
                "unread": unread_count
            }
            return True

        except Exception as e:
            print(f"✗ 失败: {type(e).__name__}: {e}")
            self.test_results[test_name] = {"success": False, "error": str(e)}
            return False

    async def test_create_page(self) -> bool:
        """测试：在个人空间创建页面"""
        test_name = "创建测试页面"
        print(f"\n[TEST] {test_name}")
        print("-" * 60)

        if not self.personal_space_key:
            print("⚠ 跳过: 未找到个人空间 key")
            self.test_results[test_name] = {"success": False, "error": "No personal space key"}
            return False

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            title = f"API Test Page - {timestamp}"
            body = f"""
            <h1>API 测试页面</h1>
            <p>这是一个由 Atlassian API 客户端库自动创建的测试页面。</p>
            <p>创建时间: {timestamp}</p>
            <h2>测试信息</h2>
            <ul>
                <li>客户端: Python Atlassian API</li>
                <li>产品: Confluence</li>
                <li>认证模式: Basic Auth</li>
            </ul>
            """

            page = await self.client.content.create(
                type="page",
                title=title,
                space_key=self.personal_space_key,
                body=body,
                body_format="storage",
            )

            self.test_page_id = page.id

            print(f"✓ 成功创建页面")
            print(f"  页面ID: {page.id}")
            print(f"  标题: {page.title}")
            print(f"  空间: {page.space.key if page.space else 'N/A'}")
            print(f"  链接: {self.client.base_url}/pages/viewpage.action?pageId={page.id}")

            self.test_results[test_name] = {"success": True, "page_id": page.id}
            return True

        except AtlassianNotFoundError:
            print(f"✗ 失败: 个人空间不存在 ({self.personal_space_key})")
            print("  提示: 请先在 Confluence 中创建个人空间")
            self.test_results[test_name] = {"success": False, "error": "Personal space not found"}
            return False

        except Exception as e:
            print(f"✗ 失败: {type(e).__name__}: {e}")
            self.test_results[test_name] = {"success": False, "error": str(e)}
            return False

    async def test_get_page(self) -> bool:
        """测试：获取页面详情"""
        test_name = "获取页面详情"
        print(f"\n[TEST] {test_name}")
        print("-" * 60)

        if not self.test_page_id:
            print("⚠ 跳过: 未创建测试页面")
            self.test_results[test_name] = {"success": False, "error": "No test page"}
            return False

        try:
            page = await self.client.content.get(
                self.test_page_id,
                expand="body.storage,version,space"
            )

            print(f"✓ 成功获取页面")
            print(f"  ID: {page.id}")
            print(f"  标题: {page.title}")
            print(f"  类型: {page.type}")
            print(f"  状态: {page.status}")
            if page.version:
                print(f"  版本: {page.version.number}")

            self.test_results[test_name] = {"success": True}
            return True

        except Exception as e:
            print(f"✗ 失败: {type(e).__name__}: {e}")
            self.test_results[test_name] = {"success": False, "error": str(e)}
            return False

    async def test_update_page(self) -> bool:
        """测试：更新页面"""
        test_name = "更新页面"
        print(f"\n[TEST] {test_name}")
        print("-" * 60)

        if not self.test_page_id:
            print("⚠ 跳过: 未创建测试页面")
            self.test_results[test_name] = {"success": False, "error": "No test page"}
            return False

        try:
            # 先获取当前页面获取版本号
            page = await self.client.content.get(self.test_page_id, expand="version")
            current_version = page.version.number if page.version else 1

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_body = f"""
            <h1>API 测试页面 (已更新)</h1>
            <p>这是一个由 Atlassian API 客户端库自动创建的测试页面。</p>
            <p>更新时间: {timestamp}</p>
            <h2>更新测试</h2>
            <p>这个页面已经被成功更新！</p>
            <ul>
                <li>更新版本: {current_version + 1}</li>
                <li>更新时间: {timestamp}</li>
            </ul>
            """

            updated_page = await self.client.content.update(
                content_id=self.test_page_id,
                title=f"{page.title} (Updated)",
                body=new_body,
                version_number=current_version + 1,
                version_message="API 测试更新",
            )

            print(f"✓ 成功更新页面")
            print(f"  页面ID: {updated_page.id}")
            print(f"  新标题: {updated_page.title}")
            if updated_page.version:
                print(f"  新版本: {updated_page.version.number}")

            self.test_results[test_name] = {"success": True}
            return True

        except Exception as e:
            print(f"✗ 失败: {type(e).__name__}: {e}")
            self.test_results[test_name] = {"success": False, "error": str(e)}
            return False

    async def test_add_labels(self) -> bool:
        """测试：添加标签"""
        test_name = "添加标签"
        print(f"\n[TEST] {test_name}")
        print("-" * 60)

        if not self.test_page_id:
            print("⚠ 跳过: 未创建测试页面")
            self.test_results[test_name] = {"success": False, "error": "No test page"}
            return False

        try:
            labels = ["api-test", "automation", "python"]
            result = await self.client.content.add_labels(
                self.test_page_id,
                labels=labels,
            )

            print(f"✓ 成功添加标签")
            print(f"  添加的标签: {', '.join(labels)}")
            print(f"  标签总数: {len(result.results)}")

            self.test_results[test_name] = {"success": True}
            return True

        except Exception as e:
            print(f"✗ 失败: {type(e).__name__}: {e}")
            self.test_results[test_name] = {"success": False, "error": str(e)}
            return False

    async def test_delete_page(self) -> bool:
        """测试：删除页面"""
        test_name = "删除测试页面"
        print(f"\n[TEST] {test_name}")
        print("-" * 60)

        if not self.test_page_id:
            print("⚠ 跳过: 未创建测试页面")
            self.test_results[test_name] = {"success": False, "error": "No test page"}
            return False

        try:
            await self.client.content.delete(self.test_page_id)

            print(f"✓ 成功删除页面")
            print(f"  页面ID: {self.test_page_id}")
            print(f"  提示: 页面已移至回收站")

            self.test_results[test_name] = {"success": True}
            return True

        except Exception as e:
            print(f"✗ 失败: {type(e).__name__}: {e}")
            self.test_results[test_name] = {"success": False, "error": str(e)}
            return False

    def print_summary(self):
        """打印测试结果摘要"""
        print("\n" + "=" * 60)
        print("测试结果摘要")
        print("=" * 60)

        for test_name, result in self.test_results.items():
            status = "✓ PASSED" if result.get("success") else "✗ FAILED"
            print(f"{status} - {test_name}")
            if not result.get("success") and result.get("error"):
                print(f"        错误: {result.get('error')}")

        # 统计
        passed = sum(1 for r in self.test_results.values() if r.get("success"))
        total = len(self.test_results)
        print(f"\n总计: {passed}/{total} 通过")


class _RecordingClient:
    """记录请求参数的最小 HTTP 客户端替身。"""

    def __init__(self) -> None:
        self.path: str | None = None
        self.payload: dict[str, Any] | None = None

    async def put_json(self, path: str, data: dict[str, Any]) -> dict[str, Any]:
        self.path = path
        self.payload = data
        return {"id": "456", **data}


def test_update_includes_ancestors_when_parent_id_is_provided() -> None:
    client = _RecordingClient()
    resource = ContentResource(client)

    asyncio.run(
        resource.update(
            content_id="456",
            title="Moved page",
            body="<p>content</p>",
            version_number=2,
            parent_id="789",
        )
    )

    assert client.path == "/rest/api/content/456"
    assert client.payload is not None
    assert client.payload["ancestors"] == [{"id": "789"}]


def test_update_omits_ancestors_when_parent_id_is_not_provided() -> None:
    client = _RecordingClient()
    resource = ContentResource(client)

    asyncio.run(
        resource.update(
            content_id="456",
            title="Unmoved page",
            body="<p>content</p>",
            version_number=2,
        )
    )

    assert client.payload is not None
    assert "ancestors" not in client.payload


async def main():
    parser = argparse.ArgumentParser(description="Test Confluence API")
    parser.add_argument("--read-only", action="store_true", help="仅执行读取测试（不创建/修改内容）")
    parser.add_argument("--full", action="store_true", help="执行完整测试（包含写入操作）")
    parser.add_argument("--url", help="Confluence URL")
    parser.add_argument("--username", "-u", help="用户名")
    parser.add_argument("--password", "-p", help="密码")

    args = parser.parse_args()

    tester = ConfluenceAPITest()

    try:
        await tester.setup(args.url, args.username, args.password)

        async with tester.client:
            # 基础测试（只读）
            await tester.test_get_current_user()
            await tester.test_get_spaces()
            await tester.test_get_personal_space()
            await tester.test_search_content()
            await tester.test_get_notifications()

            # 写入测试（需要明确指定）
            if args.full:
                print("\n" + "=" * 60)
                print("执行写入测试（将在个人空间创建测试页面）")
                print("=" * 60)

                await tester.test_create_page()
                await tester.test_get_page()
                await tester.test_update_page()
                await tester.test_add_labels()
                await tester.test_delete_page()
            elif not args.read_only:
                print("\n" + "=" * 60)
                print("提示: 使用 --full 参数执行完整测试（包含写入操作）")
                print("     使用 --read-only 参数仅执行只读测试")
                print("=" * 60)

        tester.print_summary()

    except AtlassianAuthError as e:
        print(f"\n✗ 认证失败: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n✗ 配置错误: {e}")
        print("\n请设置环境变量:")
        print("  CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD")
        print("或使用通用变量:")
        print("  ATLASSIAN_URL, ATLASSIAN_USERNAME, ATLASSIAN_PASSWORD")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 未预期的错误: {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
