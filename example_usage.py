#!/usr/bin/env python3
"""
Atlassian API 客户端使用示例

演示如何在你的项目中使用这个库

运行命令:
    python example_usage.py
    # 或
    uv run python example_usage.py
"""

import asyncio
from atlassian.confluence import ConfluenceClient


async def example_basic_usage():
    """基础使用示例"""
    print("=" * 70)
    print("示例 1: 基础使用")
    print("=" * 70)

    async with ConfluenceClient() as confluence:
        # 获取当前用户
        user = await confluence.user.get_current()
        print(f"✓ 当前用户: {user.display_name} ({user.username})")

        # 搜索页面
        results = await confluence.search.search("type=page", limit=5)
        print(f"✓ 找到 {results.total_size} 个页面")

        # 显示前 5 个页面
        for item in results.results[:5]:
            page = item.content
            print(f"  - {page.title}")

    print()


async def example_space_management():
    """空间管理示例"""
    print("=" * 70)
    print("示例 2: 空间管理")
    print("=" * 70)

    async with ConfluenceClient() as confluence:
        # 获取所有空间
        spaces = await confluence.space.get_all(limit=10)
        print(f"✓ 获取到 {spaces.size} 个空间:")

        for space in spaces.results[:5]:
            print(f"  - {space.key}: {space.name}")

        # 获取第一个空间的内容
        if spaces.results:
            first_space = spaces.results[0]
            content = await confluence.space.get_content(first_space.key)
            print(f"✓ 空间 '{first_space.key}' 有 {content.page.size} 个页面")

    print()


async def example_content_search():
    """内容搜索示例"""
    print("=" * 70)
    print("示例 3: 高级搜索")
    print("=" * 70)

    async with ConfluenceClient() as confluence:
        # 使用 CQL 搜索
        cql = "type=page AND lastModified >= now('-7d')"
        results = await confluence.search.search(cql)

        print(f"✓ 最近 7 天修改的页面数: {results.total_size}")

        # 显示最近更新的页面
        for item in results.results[:3]:
            page = item.content
            print(f"  - {page.title}")
            print(f"    ID: {page.id}")
            if hasattr(item, 'last_modified'):
                print(f"    修改时间: {item.last_modified}")

    print()


async def example_user_and_groups():
    """用户和组管理示例"""
    print("=" * 70)
    print("示例 4: 用户和组管理")
    print("=" * 70)

    async with ConfluenceClient() as confluence:
        # 获取当前用户所属组
        user = await confluence.user.get_current()
        groups = await confluence.user.get_member_of(username=user.username)

        print(f"✓ 用户 '{user.display_name}' 属于 {groups['size']} 个组:")
        for group in groups['results'][:5]:
            print(f"  - {group['name']}")

        # 获取所有用户组
        all_groups = await confluence.group.get_all(limit=10)
        print(f"✓ 系统共有 {all_groups['size']} 个用户组")

    print()


async def example_watch_and_notification():
    """监视和通知示例"""
    print("=" * 70)
    print("示例 5: 监视和通知")
    print("=" * 70)

    async with ConfluenceClient() as confluence:
        # 获取一个页面用于测试
        results = await confluence.search.search("type=page", limit=1)

        if results.results:
            page_id = results.results[0].content.id

            # 检查是否正在监视
            watching = await confluence.user.is_watching_content(page_id)
            print(f"✓ 是否监视页面 {page_id}: {watching.watching}")

            # 获取通知（需要 MyWork 插件）
            try:
                notifications = await confluence.notification.get_all(limit=5)
                print(f"✓ 获取到 {notifications.get('size', 0)} 条通知")
            except Exception as e:
                print(f"⚠️  获取通知失败: {e}")
                print("   (可能需要安装 MyWork Confluence Host Plugin)")

    print()


async def example_system_info():
    """系统信息示例（Confluence 7.0+）"""
    print("=" * 70)
    print("示例 6: 系统信息（Confluence 7.0+）")
    print("=" * 70)

    async with ConfluenceClient() as confluence:
        # 获取访问模式
        try:
            access_mode = await confluence.accessmode.get()
            print(f"✓ 系统访问模式: {access_mode}")
        except Exception as e:
            print(f"⚠️  获取访问模式失败: {e}")
            print("   (需要 Confluence 7.0+ 版本)")

        # 获取长期任务
        try:
            tasks = await confluence.longtask.get_all(limit=5)
            print(f"✓ 当前有 {tasks['size']} 个长期任务")

            for task in tasks['results'][:3]:
                print(f"  - 任务 {task['id']}: {task.get('percentageComplete', 0)}%")
        except Exception as e:
            print(f"⚠️  获取长期任务失败: {e}")

    print()


async def example_error_handling():
    """错误处理示例"""
    print("=" * 70)
    print("示例 7: 错误处理")
    print("=" * 70)

    from atlassian.common.exceptions import AtlassianError

    async with ConfluenceClient() as confluence:
        # 尝试获取不存在的页面
        try:
            page = await confluence.content.get("invalid-page-id")
        except AtlassianError as e:
            error_msg = str(e)
            if "404" in error_msg:
                print("✓ 正确捕获 404 错误: 页面不存在")
            elif "403" in error_msg:
                print("✓ 正确捕获 403 错误: 权限不足")
            else:
                print(f"✓ 捕获到错误: {e}")

        # 尝试访问需要管理员权限的 API
        try:
            webhooks = await confluence.webhook.get_all(limit=1)
            print("✓ Webhook API 访问成功")
        except AtlassianError as e:
            if "403" in str(e):
                print("✓ 正确捕获 403 错误: 需要管理员权限")
            elif "404" in str(e):
                print("✓ Webhook API 不可用（服务器版本可能过旧）")

    print()


async def example_batch_operations():
    """批量操作示例"""
    print("=" * 70)
    print("示例 8: 批量操作")
    print("=" * 70)

    async with ConfluenceClient() as confluence:
        # 并发获取多个空间的信息
        space_keys = []
        spaces = await confluence.space.get_all(limit=3)

        for space in spaces.results[:3]:
            space_keys.append(space.key)

        if space_keys:
            # 使用 asyncio.gather 并发请求
            tasks = [
                confluence.space.get(key)
                for key in space_keys
            ]
            space_details = await asyncio.gather(*tasks)

            print(f"✓ 并发获取了 {len(space_details)} 个空间的详情:")
            for space in space_details:
                print(f"  - {space.key}: {space.name}")

    print()


async def main():
    """运行所有示例"""
    print()
    print("🚀 Atlassian API 客户端使用示例")
    print()

    try:
        # 运行所有示例
        await example_basic_usage()
        await example_space_management()
        await example_content_search()
        await example_user_and_groups()
        await example_watch_and_notification()
        await example_system_info()
        await example_error_handling()
        await example_batch_operations()

        print("=" * 70)
        print("✅ 所有示例运行完成！")
        print("=" * 70)
        print()
        print("📖 更多信息:")
        print("  - 完整使用指南: docs/USAGE_GUIDE.md")
        print("  - API 登记表: docs/CONFLUENCE_API_REGISTRY.md")
        print("  - Webhook 指南: docs/WEBHOOK_USAGE_GUIDE.md")
        print()

    except Exception as e:
        print(f"❌ 运行失败: {e}")
        print()
        print("请检查:")
        print("  1. 环境变量是否正确配置 (CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD)")
        print("  2. Confluence 服务是否可访问")
        print("  3. 用户名和密码是否正确")


if __name__ == "__main__":
    asyncio.run(main())
