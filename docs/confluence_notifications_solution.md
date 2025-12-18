# Confluence 监视和通知完整解决方案

## 问题回答

### Q: 监视页面后，如何获取最新消息？

**答案**：使用 **MyWork Confluence Host Plugin** 提供的通知 API。

---

## 完整解决方案

### 1. 监视功能（Watch API）

监视功能用于**订阅**页面或空间的更新，触发 Confluence 系统发送通知。

```python
from atlassian.confluence import ConfluenceClient

async with ConfluenceClient() as confluence:
    # 监视页面
    await confluence.user.watch_content(content_id="123456")

    # 监视空间
    await confluence.user.watch_space(space_key="DEV")
```

**作用**：
- ✅ 在 Confluence 系统中标记用户订阅该内容
- ✅ 内容更新时自动生成通知
- ✅ 触发邮件通知（取决于用户设置）

---

### 2. 通知 API（Notification API）

**前提**：需要安装 **MyWork Confluence Host Plugin** 插件

#### 核心功能

| 功能 | API 方法 | 说明 |
|------|---------|------|
| 获取通知列表 | `notification.get_all()` | 获取所有通知 |
| 获取分组通知 | `notification.get_nested()` | 按项目分组的通知 |
| 未读数量 | `notification.get_unread_count()` | 获取未读通知数量 |
| 标记已读 | `notification.mark_as_read()` | 标记通知为已读 |
| 获取单个通知 | `notification.get()` | 获取特定通知详情 |

---

## 使用示例

### 示例1：获取未读通知

```python
async with ConfluenceClient() as confluence:
    # 获取未读数量
    status = await confluence.notification.get_unread_count()
    print(f"未读通知: {status['count']} 条")

    # 获取通知列表
    notifications = await confluence.notification.get_all(limit=20)

    for notif in notifications:
        if not notif.get('read'):
            print(f"📬 {notif['title']}")
            print(f"   时间: {notif['created']}")
            print(f"   描述: {notif.get('description', 'N/A')}")
```

### 示例2：获取监视页面的更新

```python
async def get_watched_page_updates():
    """获取监视页面的最新更新通知"""
    async with ConfluenceClient() as confluence:
        # 获取所有通知
        notifications = await confluence.notification.get_all(limit=50)

        # 筛选页面更新通知
        page_updates = [
            n for n in notifications
            if n.get('entity') == 'page' and not n.get('read')
        ]

        print(f"监视页面有 {len(page_updates)} 条新更新：")

        for notif in page_updates:
            item = notif.get('item', {})
            print(f"  📄 {item.get('title')}")
            print(f"     {notif['title']}")
            print(f"     链接: {item.get('url')}")
            print()

        return page_updates

# 使用
updates = await get_watched_page_updates()
```

### 示例3：监控新通知（轮询）

```python
import asyncio

async def monitor_notifications():
    """实时监控新通知"""
    async with ConfluenceClient() as confluence:
        # 获取轮询间隔
        status = await confluence.notification.get_status()
        poll_interval = status.get('timeout', 60)  # 默认60秒
        last_count = status.get('count', 0)

        print(f"开始监控通知（间隔 {poll_interval} 秒）...")

        while True:
            await asyncio.sleep(poll_interval)

            # 检查新通知
            current = await confluence.notification.get_unread_count()
            current_count = current.get('count', 0)

            if current_count > last_count:
                new_count = current_count - last_count
                print(f"🔔 收到 {new_count} 条新通知！")

                # 获取最新通知
                latest = await confluence.notification.get_all(limit=new_count)
                for notif in latest[:new_count]:
                    print(f"  - {notif['title']}")

                last_count = current_count

# 使用
await monitor_notifications()
```

### 示例4：分页获取所有通知

```python
async def get_all_notifications():
    """分页获取所有通知"""
    async with ConfluenceClient() as confluence:
        all_notifications = []
        last_id = None
        page_size = 50

        while True:
            # 使用 after 参数分页
            notifications = await confluence.notification.get_all(
                limit=page_size,
                after=last_id
            )

            if not notifications:
                break

            all_notifications.extend(notifications)
            last_id = notifications[-1]['id']

            print(f"已获取 {len(all_notifications)} 条通知...")

        return all_notifications

# 使用
all_notifs = await get_all_notifications()
```

### 示例5：标记通知为已读

```python
async def mark_page_notifications_read(page_id: str):
    """标记特定页面的所有通知为已读"""
    async with ConfluenceClient() as confluence:
        # 获取通知列表
        notifications = await confluence.notification.get_all(limit=100)

        marked_count = 0
        for notif in notifications:
            # 检查是否是该页面的通知
            item = notif.get('item', {})
            if page_id in item.get('url', ''):
                if not notif.get('read'):
                    # 标记为已读
                    await confluence.notification.mark_as_read(notif['id'])
                    marked_count += 1
                    print(f"✓ 已读: {notif['title']}")

        print(f"总计标记 {marked_count} 条通知为已读")

# 使用
await mark_page_notifications_read("123456")
```

---

## 完整工作流程

### 场景：团队协作 - 监控项目文档更新

```python
async def team_collaboration_workflow():
    """团队协作工作流：监控项目文档"""
    async with ConfluenceClient() as confluence:
        # 步骤1：监视项目空间
        project_space = "PROJECT"
        await confluence.user.watch_space(space_key=project_space)
        print(f"✓ 已监视空间: {project_space}")

        # 步骤2：监视重要页面
        important_pages = ["123456", "789012", "345678"]
        for page_id in important_pages:
            await confluence.user.watch_content(content_id=page_id)
            print(f"✓ 已监视页面: {page_id}")

        # 步骤3：定期检查更新（例如每小时）
        while True:
            # 获取未读通知
            status = await confluence.notification.get_unread_count()
            unread_count = status.get('count', 0)

            if unread_count > 0:
                print(f"\n🔔 您有 {unread_count} 条未读通知")

                # 获取通知详情
                notifications = await confluence.notification.get_all(limit=unread_count)

                # 筛选项目相关的通知
                project_updates = []
                for notif in notifications:
                    if not notif.get('read'):
                        item = notif.get('item', {})
                        # 检查是否是项目空间的内容
                        if project_space in item.get('url', ''):
                            project_updates.append(notif)

                if project_updates:
                    print(f"项目空间有 {len(project_updates)} 条更新：")
                    for notif in project_updates:
                        item = notif.get('item', {})
                        print(f"  📄 {item.get('title')}")
                        print(f"     {notif['title']}")
                        print(f"     {notif.get('description', 'N/A')[:100]}")
                        print()

                        # 标记为已读
                        await confluence.notification.mark_as_read(notif['id'])

            # 等待1小时
            await asyncio.sleep(3600)

# 运行
await team_collaboration_workflow()
```

---

## API 参考

### NotificationResource 方法

#### 获取通知

```python
# 获取通知列表（平面）
notifications = await confluence.notification.get_all(
    limit=20,        # 可选：返回数量
    after=12345,     # 可选：获取指定ID之后的通知（分页）
    before=67890     # 可选：获取指定ID之前的通知
)

# 获取分组通知（按项目聚合）
nested = await confluence.notification.get_nested(
    limit=20,
    after=12345
)

# 获取单个通知
notif = await confluence.notification.get(notification_id=123)
```

#### 未读统计

```python
# 获取未读数量（包含轮询配置）
status = await confluence.notification.get_unread_count()
# 返回: {"count": 7, "timeout": 60, "maxTimeout": 300}

# 仅获取新通知数量
new_count = await confluence.notification.get_new_count()

# 获取完整状态
status = await confluence.notification.get_status()
```

#### 标记已读

```python
# 标记单个通知为已读
await confluence.notification.mark_as_read(notification_id=123)

# 设置最后查看的通知ID（之后的通知视为未读）
await confluence.notification.set_last_read_id(notification_id=456)
```

#### 管理通知

```python
# 更新通知状态
await confluence.notification.update_status(
    notification_id=123,
    status="DONE"  # 或 "TODO"
)

# 删除通知
await confluence.notification.delete(notification_id=123)
```

---

## 通知对象结构

```json
{
  "id": 12345,
  "title": "John Doe 评论了页面",
  "description": "评论内容...",
  "application": "confluence",
  "entity": "page",
  "action": "commented",
  "created": "2025-12-18T10:30:00.000Z",
  "updated": "2025-12-18T10:30:00.000Z",
  "status": "NEW",
  "read": false,
  "pinned": false,
  "item": {
    "title": "项目设计文档",
    "url": "https://confluence.example.com/pages/viewpage.action?pageId=123456",
    "iconUrl": "https://confluence.example.com/...",
    "applicationLinkId": "..."
  },
  "metadata": {}
}
```

---

## 最佳实践

### 1. 轮询频率

遵守服务器返回的 `timeout` 值（通常是60秒）：

```python
status = await confluence.notification.get_status()
poll_interval = status.get('timeout', 60)
await asyncio.sleep(poll_interval)
```

### 2. 分页获取

使用 `after` 参数而不是 `offset`，更高效：

```python
last_id = None
while True:
    notifications = await confluence.notification.get_all(
        limit=50,
        after=last_id
    )
    if not notifications:
        break
    last_id = notifications[-1]['id']
```

### 3. 过滤通知

根据 `entity`、`action` 等字段筛选：

```python
page_comments = [
    n for n in notifications
    if n.get('entity') == 'page' and n.get('action') == 'commented'
]
```

### 4. 错误处理

```python
try:
    notifications = await confluence.notification.get_all()
except Exception as e:
    if "404" in str(e):
        print("MyWork 插件未安装")
    else:
        print(f"获取通知失败: {e}")
```

---

## 注意事项

1. **插件依赖**
   - 需要安装 **MyWork Confluence Host Plugin**
   - 如果未安装，API 调用会返回 404 错误

2. **权限要求**
   - 用户只能看到自己的通知
   - 管理员可以使用 `bypass` 参数查看其他用户的通知

3. **通知来源**
   - 监视的页面/空间更新
   - @提及
   - 分配的任务
   - 评论回复
   - 页面权限变更

4. **性能考虑**
   - 避免过于频繁的轮询
   - 使用 `after` 参数减少数据传输
   - 批量操作时添加延迟

---

## 总结

**监视（Watch）+ 通知（Notification）= 完整解决方案**

| 步骤 | API | 作用 |
|------|-----|------|
| 1. 订阅内容 | `user.watch_content/space()` | 开始监视 |
| 2. 获取更新 | `notification.get_all()` | 查看通知 |
| 3. 检查未读 | `notification.get_unread_count()` | 未读数量 |
| 4. 标记已读 | `notification.mark_as_read()` | 清除提醒 |

通过这套 API，您可以实现：
- ✅ 自动监控文档更新
- ✅ 及时获取团队协作信息
- ✅ 构建自定义的通知系统
- ✅ 集成到工作流程工具中

完整示例代码请查看：`examples/confluence_notifications.py`
