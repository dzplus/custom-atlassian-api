# Confluence 监视（Watch）功能详解

## 功能概述

Confluence 的监视功能允许用户订阅页面或空间的更新通知。当被监视的内容发生变化时，用户会收到邮件通知或在 Confluence 中看到更新提醒。

## 使用场景

### 1. **团队协作场景**
监视团队成员正在编辑的文档，及时了解文档更新情况。

**示例**：
- 产品经理监视需求文档，当开发人员更新实现细节时收到通知
- 技术 Leader 监视团队的设计文档空间，了解团队的设计进展

### 2. **项目跟踪场景**
监视项目相关的空间或页面，掌握项目进度。

**示例**：
- 监视项目空间，随时了解项目文档的更新
- 监视项目周报页面，不错过任何项目进展

### 3. **知识管理场景**
监视感兴趣的技术文档或知识库。

**示例**：
- 监视公司技术规范文档，当规范更新时第一时间知道
- 监视培训资料空间，了解新的培训内容

### 4. **自动化集成场景**
通过 API 实现自动化的内容订阅管理。

**示例**：
- 自动为新加入的团队成员订阅团队空间
- 根据用户角色自动订阅相关文档
- 批量管理用户的订阅关系

---

## API 使用方法

### 内容监视（Content Watch）

#### 1. 检查是否监视某个页面

```python
from atlassian.confluence import ConfluenceClient

async with ConfluenceClient() as confluence:
    # 检查当前用户是否监视页面
    watch_status = await confluence.user.is_watching_content(
        content_id="123456"
    )

    if watch_status.watching:
        print("已监视该页面")
    else:
        print("未监视该页面")
```

#### 2. 监视页面

```python
async with ConfluenceClient() as confluence:
    # 监视指定页面
    await confluence.user.watch_content(
        content_id="123456"
    )
    print("已开始监视该页面")
```

#### 3. 取消监视页面

```python
async with ConfluenceClient() as confluence:
    # 取消监视
    await confluence.user.unwatch_content(
        content_id="123456"
    )
    print("已取消监视该页面")
```

---

### 空间监视（Space Watch）

#### 1. 检查是否监视某个空间

```python
async with ConfluenceClient() as confluence:
    # 检查当前用户是否监视空间
    watch_status = await confluence.user.is_watching_space(
        space_key="DEV"
    )

    if watch_status.watching:
        print("已监视该空间")
    else:
        print("未监视该空间")
```

#### 2. 监视空间

```python
async with ConfluenceClient() as confluence:
    # 监视指定空间
    await confluence.user.watch_space(
        space_key="DEV"
    )
    print("已开始监视该空间")
```

#### 3. 取消监视空间

```python
async with ConfluenceClient() as confluence:
    # 取消监视
    await confluence.user.unwatch_space(
        space_key="DEV"
    )
    print("已取消监视该空间")
```

---

## 实际应用示例

### 示例1：自动订阅团队空间

当新员工加入时，自动为其订阅团队相关的空间。

```python
from atlassian.confluence import ConfluenceClient

async def subscribe_new_employee(username: str, team_spaces: list[str]):
    """为新员工订阅团队空间"""
    async with ConfluenceClient() as confluence:
        for space_key in team_spaces:
            try:
                # 检查是否已监视
                status = await confluence.user.is_watching_space(
                    space_key=space_key,
                    username=username
                )

                if not status.watching:
                    # 订阅空间
                    await confluence.user.watch_space(
                        space_key=space_key,
                        username=username
                    )
                    print(f"✓ 已为 {username} 订阅空间: {space_key}")
                else:
                    print(f"- {username} 已订阅空间: {space_key}")

            except Exception as e:
                print(f"✗ 订阅空间 {space_key} 失败: {e}")

# 使用示例
await subscribe_new_employee(
    username="newuser",
    team_spaces=["DEV", "PRODUCT", "DESIGN"]
)
```

### 示例2：批量管理订阅

管理整个团队对重要文档的订阅。

```python
async def manage_team_subscriptions(
    team_members: list[str],
    important_pages: list[str]
):
    """为团队成员批量订阅重要页面"""
    async with ConfluenceClient() as confluence:
        for member in team_members:
            subscribed_count = 0
            for page_id in important_pages:
                try:
                    await confluence.user.watch_content(
                        content_id=page_id,
                        username=member
                    )
                    subscribed_count += 1
                except Exception as e:
                    print(f"✗ {member} 订阅页面 {page_id} 失败: {e}")

            print(f"✓ {member}: 订阅了 {subscribed_count}/{len(important_pages)} 个页面")

# 使用示例
await manage_team_subscriptions(
    team_members=["user1", "user2", "user3"],
    important_pages=["123456", "789012", "345678"]
)
```

### 示例3：根据页面标签自动订阅

自动订阅带有特定标签的页面。

```python
async def watch_pages_by_label(label: str):
    """监视所有带有指定标签的页面"""
    async with ConfluenceClient() as confluence:
        # 使用 CQL 搜索带有指定标签的页面
        cql = f"type=page AND label={label}"
        results = await confluence.content.search(cql, limit=100)

        watched_count = 0
        for page in results.results:
            try:
                # 检查是否已监视
                status = await confluence.user.is_watching_content(
                    content_id=page.id
                )

                if not status.watching:
                    await confluence.user.watch_content(
                        content_id=page.id
                    )
                    watched_count += 1
                    print(f"✓ 已监视: {page.title}")

            except Exception as e:
                print(f"✗ 监视页面 {page.title} 失败: {e}")

        print(f"\n总计: 新监视了 {watched_count} 个页面")

# 使用示例：监视所有标签为 "important" 的页面
await watch_pages_by_label("important")
```

### 示例4：导出用户的订阅列表

获取用户订阅的所有内容（需要遍历检查）。

```python
async def export_user_subscriptions(space_keys: list[str]):
    """导出用户在指定空间中的订阅"""
    async with ConfluenceClient() as confluence:
        subscriptions = {
            "spaces": [],
            "pages": []
        }

        # 检查空间订阅
        for space_key in space_keys:
            try:
                status = await confluence.user.is_watching_space(
                    space_key=space_key
                )
                if status.watching:
                    subscriptions["spaces"].append(space_key)
            except Exception as e:
                print(f"检查空间 {space_key} 失败: {e}")

        # 获取并检查页面订阅
        for space_key in space_keys:
            try:
                pages = await confluence.space.get_content_by_type(
                    space_key=space_key,
                    content_type="page",
                    limit=100
                )

                for page in pages.results:
                    try:
                        status = await confluence.user.is_watching_content(
                            content_id=page.id
                        )
                        if status.watching:
                            subscriptions["pages"].append({
                                "id": page.id,
                                "title": page.title,
                                "space": space_key
                            })
                    except:
                        pass

            except Exception as e:
                print(f"获取空间 {space_key} 页面失败: {e}")

        return subscriptions

# 使用示例
subscriptions = await export_user_subscriptions(["DEV", "PRODUCT"])
print(f"监视的空间: {subscriptions['spaces']}")
print(f"监视的页面: {len(subscriptions['pages'])} 个")
```

---

## 监视 vs 收藏

### 监视（Watch）
- **目的**: 接收更新通知
- **效果**: 当内容更新时收到邮件或系统通知
- **使用场景**: 需要及时了解内容变化

### 收藏（Favorite）
- **目的**: 快速访问常用内容
- **效果**: 内容出现在收藏夹中，方便查找
- **使用场景**: 经常访问的文档

**两者可以组合使用**：既收藏又监视重要文档。

---

## 注意事项

### 1. 权限要求
- 需要有读取内容的权限才能监视
- 管理员可以为其他用户设置监视（使用 `username` 参数）

### 2. 通知设置
监视后是否收到通知取决于用户的 Confluence 通知设置：
- 用户配置 → 通知设置
- 可以选择立即通知、每日摘要等

### 3. API 限制
- 检查监视状态不会触发通知
- 频繁的监视/取消监视操作可能受到速率限制

### 4. 性能考虑
- 批量操作时建议加入延迟，避免触发速率限制
- 大量订阅可能影响用户的通知体验

---

## 返回值说明

### UserWatch 模型

```python
class UserWatch(BaseModel):
    watching: bool = False  # True: 正在监视, False: 未监视
```

**示例响应**：
```python
UserWatch(watching=True)   # 已监视
UserWatch(watching=False)  # 未监视
```

---

## 总结

监视功能是 Confluence 中重要的协作特性，通过 API 可以：

✅ **自动化订阅管理** - 新员工入职、角色变更时自动订阅相关内容
✅ **批量操作** - 为团队成员批量订阅重要文档
✅ **智能订阅** - 根据标签、空间等条件自动订阅
✅ **订阅审计** - 导出和分析用户的订阅情况

合理使用监视功能可以提高团队协作效率，确保重要信息及时传达。
