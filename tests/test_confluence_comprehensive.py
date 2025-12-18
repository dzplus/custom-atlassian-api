"""
Confluence 综合测试 - 完整工作流测试

测试流程：
1. 用户信息查询
2. 空间查询和属性管理
3. 创建测试页面和子页面
4. 内容查询和属性管理
5. 标签管理
6. 附件管理
7. 评论和子内容查询
8. 监视功能
9. 权限查询
10. 搜索功能
11. 清理测试数据

所有写入操作在个人空间进行

运行命令:
    uv run python -m tests.test_confluence_comprehensive
"""

import asyncio
import sys
from datetime import datetime
from typing import Optional

from atlassian.confluence import ConfluenceClient
from atlassian.common.exceptions import AtlassianError


class ComprehensiveTest:
    """综合测试类"""

    def __init__(self):
        self.client: Optional[ConfluenceClient] = None
        self.test_results: dict[str, bool] = {}
        self.personal_space_key: Optional[str] = None
        self.test_page_id: Optional[str] = None
        self.child_page_id: Optional[str] = None
        self.test_property_key = "test-property"
        self.test_labels = ["comprehensive-test", "api-test", "auto-cleanup"]
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
        print("Confluence 综合API测试")
        print("=" * 70)
        print()

        self.client = ConfluenceClient()
        print(f"URL: {self.client.base_url}")
        print(f"用户: {self.client._username}")
        print()

    # ========== 1. 用户信息查询 ==========

    async def test_user_apis(self):
        """测试用户相关 API"""
        print("[阶段1] 用户信息查询")
        print("-" * 70)

        try:
            # 1.1 get_current() - Pydantic 模型
            try:
                user = await self.client.user.get_current(expand="operations")
                self.log_test(
                    "user.get_current()",
                    True,
                    f"用户: {user.display_name} ({user.username})"
                )
                username = user.username
                self.personal_space_key = f"~{username}"
            except Exception as e:
                self.log_test("user.get_current()", False, str(e))
                username = None

            # 1.2 get() - 获取指定用户
            if username:
                try:
                    user_info = await self.client.user.get(username=username)
                    self.log_test(
                        "user.get(username)",
                        True,
                        f"类型: {user_info.type}"
                    )
                except Exception as e:
                    self.log_test("user.get(username)", False, str(e))

            # 1.3 get_anonymous() - 获取匿名用户
            try:
                anon = await self.client.user.get_anonymous()
                self.log_test(
                    "user.get_anonymous()",
                    True,
                    f"匿名用户: {anon.display_name}"
                )
            except Exception as e:
                self.log_test("user.get_anonymous()", False, str(e))

        except Exception as e:
            print(f"  ✗ 用户测试阶段失败: {e}")

        print()

    # ========== 2. 空间查询和属性管理 ==========

    async def test_space_apis(self):
        """测试空间相关 API"""
        print("[阶段2] 空间查询和属性管理")
        print("-" * 70)

        if not self.personal_space_key:
            print("  ⚠ 跳过: 未获取到个人空间key")
            return

        try:
            # 2.1 space.get_raw() - 原始JSON
            try:
                space_data = await self.client.space.get_raw(
                    self.personal_space_key,
                    expand="description,homepage"
                )
                self.log_test(
                    "space.get_raw()",
                    True,
                    f"空间: {space_data.get('name')}"
                )
            except Exception as e:
                self.log_test("space.get_raw()", False, str(e))

            # 2.2 space.get_content() - 获取空间内容
            try:
                content_data = await self.client.space.get_content(
                    self.personal_space_key,
                    depth="all",
                    limit=5
                )
                # content_data 是 ContentList，但 API 返回的 extra 字段(如 page)是 dict
                page_data = getattr(content_data, 'page', None)
                if page_data and isinstance(page_data, dict):
                    page_count = len(page_data.get('results', []))
                else:
                    page_count = len(content_data.results) if content_data.results else 0
                self.log_test(
                    "space.get_content()",
                    True,
                    f"页面数: {page_count}"
                )
            except Exception as e:
                self.log_test("space.get_content()", False, str(e))

            # 2.3 创建空间属性
            try:
                prop = await self.client.space.create_property(
                    self.personal_space_key,
                    key="test-space-prop",
                    value={"test": "value", "created": datetime.now().isoformat()}
                )
                self.log_test(
                    "space.create_property()",
                    True,
                    f"属性ID: {prop.id}"
                )
            except Exception as e:
                self.log_test("space.create_property()", False, str(e))

            # 2.4 获取空间属性列表
            try:
                props = await self.client.space.get_properties(
                    self.personal_space_key
                )
                self.log_test(
                    "space.get_properties()",
                    True,
                    f"属性数: {len(props.results)}"
                )
            except Exception as e:
                self.log_test("space.get_properties()", False, str(e))

            # 2.5 获取单个空间属性
            try:
                prop = await self.client.space.get_property(
                    self.personal_space_key,
                    key="test-space-prop"
                )
                self.log_test(
                    "space.get_property()",
                    True,
                    f"属性值: {prop.value}"
                )
                # version 是 dict, 不是对象
                current_version = prop.version.get('number', 1) if prop.version else 1
            except Exception as e:
                self.log_test("space.get_property()", False, str(e))
                current_version = 1

            # 2.6 更新空间属性
            try:
                updated_prop = await self.client.space.update_property(
                    self.personal_space_key,
                    key="test-space-prop",
                    value={"test": "updated", "updated": datetime.now().isoformat()},
                    version_number=current_version + 1
                )
                # version 是 dict, 不是对象
                new_version = updated_prop.version.get('number', 'N/A') if updated_prop.version else 'N/A'
                self.log_test(
                    "space.update_property()",
                    True,
                    f"新版本: {new_version}"
                )
            except Exception as e:
                self.log_test("space.update_property()", False, str(e))

            # 2.7 删除空间属性
            try:
                await self.client.space.delete_property(
                    self.personal_space_key,
                    key="test-space-prop"
                )
                self.log_test("space.delete_property()", True)
            except Exception as e:
                self.log_test("space.delete_property()", False, str(e))

        except Exception as e:
            print(f"  ✗ 空间测试阶段失败: {e}")

        print()

    # ========== 3. 创建测试页面 ==========

    async def test_create_pages(self):
        """创建测试页面和子页面"""
        print("[阶段3] 创建测试页面")
        print("-" * 70)

        if not self.personal_space_key:
            print("  ⚠ 跳过: 未获取到个人空间key")
            return

        try:
            # 3.1 创建主测试页面
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            title = f"[综合测试] API Test Page - {timestamp}"
            body = f"""
            <h1>Confluence API 综合测试页面</h1>
            <p>创建时间: {datetime.now().isoformat()}</p>
            <p>此页面由自动化测试创建，用于测试各种 Confluence API。</p>
            <p>测试完成后会自动清理。</p>
            """

            page = await self.client.content.create(
                type="page",
                title=title,
                space_key=self.personal_space_key,
                body=body
            )
            self.test_page_id = page.id
            self.log_test(
                "content.create() [主页面]",
                True,
                f"页面ID: {page.id}"
            )

            # 3.2 创建子页面
            child_title = f"[子页面] Child Page - {timestamp}"
            child_body = "<p>这是一个子页面，用于测试子内容查询功能。</p>"

            child_page = await self.client.content.create(
                type="page",
                title=child_title,
                space_key=self.personal_space_key,
                body=child_body,
                parent_id=self.test_page_id
            )
            self.child_page_id = child_page.id
            self.log_test(
                "content.create() [子页面]",
                True,
                f"子页面ID: {child_page.id}"
            )

        except Exception as e:
            print(f"  ✗ 页面创建失败: {e}")
            self.test_page_id = None
            self.child_page_id = None

        print()

    # ========== 4. 内容查询 ==========

    async def test_content_query_apis(self):
        """测试内容查询 API"""
        print("[阶段4] 内容查询")
        print("-" * 70)

        if not self.test_page_id:
            print("  ⚠ 跳过: 未创建测试页面")
            return

        try:
            # 4.1 content.get_all() - 获取内容列表
            try:
                contents = await self.client.content.get_all(
                    space_key=self.personal_space_key,
                    limit=10
                )
                self.log_test(
                    "content.get_all()",
                    True,
                    f"内容数: {contents.size}"
                )
            except Exception as e:
                self.log_test("content.get_all()", False, str(e))

            # 4.2 content.get_raw() - 原始JSON
            try:
                page_data = await self.client.content.get_raw(
                    self.test_page_id,
                    expand="body.storage,version"
                )
                self.log_test(
                    "content.get_raw()",
                    True,
                    f"版本: {page_data.get('version', {}).get('number')}"
                )
            except Exception as e:
                self.log_test("content.get_raw()", False, str(e))

            # 4.3 content.get_children() - 获取子内容
            try:
                children = await self.client.content.get_children(
                    self.test_page_id,
                    expand="page"
                )
                self.log_test(
                    "content.get_children()",
                    True,
                    f"子内容: {children}"
                )
            except Exception as e:
                self.log_test("content.get_children()", False, str(e))

            # 4.4 content.get_children_by_type() - 获取指定类型子内容
            try:
                page_children = await self.client.content.get_children_by_type(
                    self.test_page_id,
                    child_type="page"
                )
                self.log_test(
                    "content.get_children_by_type()",
                    True,
                    f"子页面数: {page_children.size}"
                )
            except Exception as e:
                self.log_test("content.get_children_by_type()", False, str(e))

            # 4.5 content.get_descendants() - 获取后代内容
            try:
                descendants = await self.client.content.get_descendants(
                    self.test_page_id
                )
                self.log_test(
                    "content.get_descendants()",
                    True,
                    f"后代内容: {descendants}"
                )
            except Exception as e:
                self.log_test("content.get_descendants()", False, str(e))

            # 4.6 content.get_descendants_by_type() - 获取指定类型后代
            try:
                page_descendants = await self.client.content.get_descendants_by_type(
                    self.test_page_id,
                    descendant_type="page"
                )
                self.log_test(
                    "content.get_descendants_by_type()",
                    True,
                    f"后代页面数: {page_descendants.size}"
                )
            except Exception as e:
                # 服务器返回 501 (未实现) 是预期行为
                if "501" in str(e):
                    self.log_test("content.get_descendants_by_type()", False, "501 服务器未实现此端点")
                else:
                    self.log_test("content.get_descendants_by_type()", False, str(e))

        except Exception as e:
            print(f"  ✗ 内容查询阶段失败: {e}")

        print()

    # ========== 5. 属性管理 ==========

    async def test_content_properties(self):
        """测试内容属性管理"""
        print("[阶段5] 内容属性管理")
        print("-" * 70)

        if not self.test_page_id:
            print("  ⚠ 跳过: 未创建测试页面")
            return

        try:
            # 5.1 create_property() - 创建属性
            try:
                prop = await self.client.content.create_property(
                    self.test_page_id,
                    key=self.test_property_key,
                    value={
                        "test": "comprehensive",
                        "timestamp": datetime.now().isoformat(),
                        "type": "integration-test"
                    }
                )
                self.log_test(
                    "content.create_property()",
                    True,
                    f"属性: {self.test_property_key}"
                )
            except Exception as e:
                self.log_test("content.create_property()", False, str(e))

            # 5.2 get_properties() - 获取属性列表
            try:
                props = await self.client.content.get_properties(
                    self.test_page_id
                )
                self.log_test(
                    "content.get_properties()",
                    True,
                    f"属性数: {len(props.results)}"
                )
            except Exception as e:
                self.log_test("content.get_properties()", False, str(e))

            # 5.3 get_property() - 获取单个属性
            try:
                prop = await self.client.content.get_property(
                    self.test_page_id,
                    key=self.test_property_key
                )
                # version 是 dict, 不是对象
                version_num = prop.version.get('number', 'N/A') if prop.version else 'N/A'
                self.log_test(
                    "content.get_property()",
                    True,
                    f"版本: {version_num}"
                )
                current_version = prop.version.get('number', 1) if prop.version else 1
            except Exception as e:
                self.log_test("content.get_property()", False, str(e))
                current_version = 1

            # 5.4 update_property() - 更新属性
            try:
                updated_prop = await self.client.content.update_property(
                    self.test_page_id,
                    key=self.test_property_key,
                    value={
                        "test": "updated",
                        "timestamp": datetime.now().isoformat(),
                        "version": current_version + 1
                    },
                    version_number=current_version + 1
                )
                # version 是 dict, 不是对象
                new_version = updated_prop.version.get('number', 'N/A') if updated_prop.version else 'N/A'
                self.log_test(
                    "content.update_property()",
                    True,
                    f"新版本: {new_version}"
                )
            except Exception as e:
                self.log_test("content.update_property()", False, str(e))

            # 5.5 delete_property() - 删除属性
            try:
                await self.client.content.delete_property(
                    self.test_page_id,
                    key=self.test_property_key
                )
                self.log_test("content.delete_property()", True)
            except Exception as e:
                self.log_test("content.delete_property()", False, str(e))

        except Exception as e:
            print(f"  ✗ 属性管理阶段失败: {e}")

        print()

    # ========== 6. 标签管理 ==========

    async def test_label_management(self):
        """测试标签管理"""
        print("[阶段6] 标签管理")
        print("-" * 70)

        if not self.test_page_id:
            print("  ⚠ 跳过: 未创建测试页面")
            return

        try:
            # 6.1 add_labels() - 添加标签（已测试，但再次验证）
            try:
                labels_result = await self.client.content.add_labels(
                    self.test_page_id,
                    labels=self.test_labels
                )
                self.log_test(
                    "content.add_labels()",
                    True,
                    f"添加标签: {', '.join(self.test_labels)}"
                )
            except Exception as e:
                self.log_test("content.add_labels()", False, str(e))

            # 6.2 get_labels() - 获取标签列表
            try:
                labels = await self.client.content.get_labels(
                    self.test_page_id
                )
                label_names = [l.name for l in labels.results]
                self.log_test(
                    "content.get_labels()",
                    True,
                    f"标签数: {len(labels.results)}, 标签: {', '.join(label_names)}"
                )
            except Exception as e:
                self.log_test("content.get_labels()", False, str(e))

            # 6.3 delete_label() - 删除标签
            try:
                await self.client.content.delete_label(
                    self.test_page_id,
                    label=self.test_labels[0]
                )
                self.log_test(
                    "content.delete_label()",
                    True,
                    f"删除标签: {self.test_labels[0]}"
                )
            except Exception as e:
                self.log_test("content.delete_label()", False, str(e))

        except Exception as e:
            print(f"  ✗ 标签管理阶段失败: {e}")

        print()

    # ========== 7. 附件管理 ==========

    async def test_attachment_management(self):
        """测试附件管理"""
        print("[阶段7] 附件管理")
        print("-" * 70)

        if not self.test_page_id:
            print("  ⚠ 跳过: 未创建测试页面")
            return

        try:
            # 7.1 add_attachment_bytes() - 上传附件（字节）
            try:
                test_content = b"This is a test file for Confluence API testing.\nCreated by comprehensive test."
                filename = f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"

                attachments = await self.client.content.add_attachment_bytes(
                    self.test_page_id,
                    content=test_content,
                    filename=filename,
                    comment="Uploaded by comprehensive API test"
                )
                self.log_test(
                    "content.add_attachment_bytes()",
                    True,
                    f"文件: {filename}, 大小: {len(test_content)} bytes"
                )
            except Exception as e:
                self.log_test("content.add_attachment_bytes()", False, str(e))

            # 7.2 get_attachments() - 获取附件列表
            try:
                attachments = await self.client.content.get_attachments(
                    self.test_page_id
                )
                self.log_test(
                    "content.get_attachments()",
                    True,
                    f"附件数: {len(attachments.results)}"
                )
            except Exception as e:
                self.log_test("content.get_attachments()", False, str(e))

        except Exception as e:
            print(f"  ✗ 附件管理阶段失败: {e}")

        print()

    # ========== 8. 评论管理 ==========

    async def test_comment_apis(self):
        """测试评论相关 API"""
        print("[阶段8] 评论管理")
        print("-" * 70)

        if not self.test_page_id:
            print("  ⚠ 跳过: 未创建测试页面")
            return

        try:
            # 8.1 get_comments() - 获取评论列表
            try:
                comments = await self.client.content.get_comments(
                    self.test_page_id
                )
                self.log_test(
                    "content.get_comments()",
                    True,
                    f"评论数: {len(comments.results)}"
                )
            except Exception as e:
                self.log_test("content.get_comments()", False, str(e))

        except Exception as e:
            print(f"  ✗ 评论管理阶段失败: {e}")

        print()

    # ========== 9. 监视功能 ==========

    async def test_watch_apis(self):
        """测试监视功能"""
        print("[阶段9] 监视功能")
        print("-" * 70)

        if not self.test_page_id or not self.personal_space_key:
            print("  ⚠ 跳过: 未创建测试页面或未获取空间key")
            return

        try:
            # 9.1 watch_content() - 监视内容
            try:
                await self.client.user.watch_content(self.test_page_id)
                self.log_test("user.watch_content()", True)
            except Exception as e:
                self.log_test("user.watch_content()", False, str(e))

            # 9.2 is_watching_content() - 检查监视状态
            try:
                watch_status = await self.client.user.is_watching_content(self.test_page_id)
                self.log_test(
                    "user.is_watching_content()",
                    True,
                    f"监视状态: {'是' if watch_status.watching else '否'}"
                )
            except Exception as e:
                self.log_test("user.is_watching_content()", False, str(e))

            # 9.3 unwatch_content() - 取消监视
            try:
                await self.client.user.unwatch_content(self.test_page_id)
                self.log_test("user.unwatch_content()", True)
            except Exception as e:
                self.log_test("user.unwatch_content()", False, str(e))

            # 9.4 watch_space() - 监视空间
            try:
                await self.client.user.watch_space(self.personal_space_key)
                self.log_test("user.watch_space()", True)
            except Exception as e:
                self.log_test("user.watch_space()", False, str(e))

            # 9.5 is_watching_space() - 检查空间监视状态
            try:
                space_watch_status = await self.client.user.is_watching_space(self.personal_space_key)
                self.log_test(
                    "user.is_watching_space()",
                    True,
                    f"监视状态: {'是' if space_watch_status.watching else '否'}"
                )
            except Exception as e:
                self.log_test("user.is_watching_space()", False, str(e))

            # 9.6 unwatch_space() - 取消监视空间
            try:
                await self.client.user.unwatch_space(self.personal_space_key)
                self.log_test("user.unwatch_space()", True)
            except Exception as e:
                self.log_test("user.unwatch_space()", False, str(e))

        except Exception as e:
            print(f"  ✗ 监视功能阶段失败: {e}")

        print()

    # ========== 10. 权限查询 ==========

    async def test_restriction_apis(self):
        """测试权限限制查询"""
        print("[阶段10] 权限查询")
        print("-" * 70)

        if not self.test_page_id:
            print("  ⚠ 跳过: 未创建测试页面")
            return

        try:
            # 10.1 get_restrictions() - 获取所有限制
            try:
                restrictions = await self.client.content.get_restrictions(
                    self.test_page_id
                )
                self.log_test(
                    "content.get_restrictions()",
                    True,
                    f"限制: {restrictions}"
                )
            except Exception as e:
                self.log_test("content.get_restrictions()", False, str(e))

            # 10.2 get_restrictions_for_operation() - 获取指定操作限制
            try:
                read_restrictions = await self.client.content.get_restrictions_for_operation(
                    self.test_page_id,
                    operation_key="read"
                )
                self.log_test(
                    "content.get_restrictions_for_operation()",
                    True,
                    f"读取限制: {read_restrictions}"
                )
            except Exception as e:
                self.log_test("content.get_restrictions_for_operation()", False, str(e))

        except Exception as e:
            print(f"  ✗ 权限查询阶段失败: {e}")

        print()

    # ========== 11. 搜索功能 ==========

    async def test_search_apis(self):
        """测试搜索功能"""
        print("[阶段11] 搜索功能")
        print("-" * 70)

        try:
            # 11.1 search.search() - 独立搜索资源
            try:
                # 个人空间的 key 在 CQL 中需要使用引号
                cql = f'space="{self.personal_space_key}" AND type=page'
                results = await self.client.search.search(cql, limit=5)
                self.log_test(
                    "search.search()",
                    True,
                    f"搜索结果: {results.size}"
                )
            except Exception as e:
                self.log_test("search.search()", False, str(e))

            # 11.2 search.search_raw() - 原始JSON搜索
            try:
                # 使用相同的 CQL 语法
                cql = f'space="{self.personal_space_key}" AND type=page'
                results_raw = await self.client.search.search_raw(cql, limit=5)
                self.log_test(
                    "search.search_raw()",
                    True,
                    f"结果数: {results_raw.get('size', 0)}"
                )
            except Exception as e:
                self.log_test("search.search_raw()", False, str(e))

        except Exception as e:
            print(f"  ✗ 搜索功能阶段失败: {e}")

        print()

    # ========== 12. 清理测试数据 ==========

    async def test_cleanup(self):
        """清理测试数据"""
        print("[阶段12] 清理测试数据")
        print("-" * 70)

        try:
            # 12.1 删除子页面
            if self.child_page_id:
                try:
                    await self.client.content.delete(self.child_page_id)
                    self.log_test("content.delete() [子页面]", True)
                except Exception as e:
                    self.log_test("content.delete() [子页面]", False, str(e))

            # 12.2 删除主页面
            if self.test_page_id:
                try:
                    await self.client.content.delete(self.test_page_id)
                    self.log_test("content.delete() [主页面]", True)
                except Exception as e:
                    self.log_test("content.delete() [主页面]", False, str(e))

        except Exception as e:
            print(f"  ✗ 清理阶段失败: {e}")

        print()

    async def run_all_tests(self):
        """运行所有测试"""
        try:
            await self.setup()

            async with self.client:
                await self.test_user_apis()
                await self.test_space_apis()
                await self.test_create_pages()
                await self.test_content_query_apis()
                await self.test_content_properties()
                await self.test_label_management()
                await self.test_attachment_management()
                await self.test_comment_apis()
                await self.test_watch_apis()
                await self.test_restriction_apis()
                await self.test_search_apis()
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
        print(f"成功率: {self.passed_count / (self.passed_count + self.failed_count) * 100:.1f}%")
        print()


async def main():
    """主函数"""
    tester = ComprehensiveTest()

    try:
        await tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
