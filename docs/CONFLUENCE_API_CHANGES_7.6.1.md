# Confluence REST API 变化分析：6.6.0 → 7.6.1

> 对比我们当前实现的 6.6.0 版本与最新的 7.6.1 版本

## 🆕 新增资源 (7.6.1 新增)

### 1. Webhooks API - **全新功能** ⭐

| HTTP 方法 | 端点 | 功能描述 | 是否已实现 |
|----------|------|---------|-----------|
| POST | `/rest/api/webhooks` | 创建 webhook | ❌ |
| GET | `/rest/api/webhooks` | 查找 webhooks（支持事件/统计过滤） | ❌ |
| GET | `/rest/api/webhooks/{webhookId}` | 获取指定 webhook | ❌ |
| PUT | `/rest/api/webhooks/{webhookId}` | 更新 webhook | ❌ |
| DELETE | `/rest/api/webhooks/{webhookId}` | 删除 webhook | ❌ |
| GET | `/rest/api/webhooks/{webhookId}/latest` | 获取最近调用记录 | ❌ |
| GET | `/rest/api/webhooks/{webhookId}/statistics` | 获取 webhook 统计信息 | ❌ |
| GET | `/rest/api/webhooks/{webhookId}/statistics/summary` | 获取统计摘要 | ❌ |
| POST | `/rest/api/webhooks/test` | 测试端点连接性 | ❌ |

**功能说明**：
- Webhooks 允许在 Confluence 事件发生时向外部系统发送通知
- 支持事件过滤、调用统计和连接测试
- 这是企业集成的重要功能

**实现优先级**: 🔴 高 - 对于 CI/CD 集成和自动化工作流很重要

---

### 2. Access Mode API - **全新功能**

| HTTP 方法 | 端点 | 功能描述 | 是否已实现 |
|----------|------|---------|-----------|
| GET | `/rest/api/accessmode` | 获取 Confluence 访问模式状态 | ❌ |

**功能说明**：
- 返回 Confluence 当前的访问模式（只读、读写等）
- 用于检查系统维护状态

**实现优先级**: 🟡 中 - 对于系统状态监控有用

---

## 🔄 现有资源的变化

### 1. Content Macro API - **部分弃用**

#### 新增端点：
| HTTP 方法 | 端点 | 功能描述 | 是否已实现 |
|----------|------|---------|-----------|
| GET | `/rest/api/content/{id}/history/{version}/macro/id/{macroId}` | 通过 ID 获取宏体（推荐） | ❌ |

#### 弃用端点：
| HTTP 方法 | 端点 | 状态 |
|----------|------|------|
| GET | `/rest/api/content/{id}/history/{version}/macro/hash/{hash}` | ⚠️ **已弃用** - 建议迁移到使用 macro ID |

**变化说明**：
- 7.6.1 推荐使用 macro ID 替代 hash 来获取宏内容
- 旧的 hash 方式已标记为 deprecated

**实现优先级**: 🟢 低 - 这是高级功能，大多数用户不需要

---

### 2. Audit API - **路径确认**

在 7.6.1 中，Audit API 的路径是 `/rest/api/audit`，而不是 `/rest/audit`。

**当前实现状态**: ✅ 已实现（使用 `/rest/audit` 路径）

**建议**:
- 检查我们当前的实现是否需要同时支持两种路径
- 或者根据 Confluence 版本自动选择路径

---

## 📊 完整资源对比表

| 资源名称 | 6.6.0 | 7.6.1 | 实现状态 | 变化说明 |
|---------|-------|-------|---------|---------|
| Access Mode | ❌ | ✅ | ❌ 未实现 | **7.6.1 新增** |
| Audit | ✅ | ✅ | ✅ 已实现 | 路径可能需要调整 |
| Content | ✅ | ✅ | ✅ 已实现 | 完全实现 |
| Content Blueprint | ✅ | ✅ | ✅ 已实现 | 无变化 |
| Content History | ✅ | ✅ | ✅ 已实现 | 新增 macro ID 端点 |
| Content Body Convert | ✅ | ✅ | ✅ 已实现 | 无变化 |
| Group | ✅ | ✅ | ✅ 已实现 | 无变化 |
| Long Task | ✅ | ✅ | ✅ 已实现 | 无变化 |
| Search | ✅ | ✅ | ✅ 已实现 | 无变化 |
| Space | ✅ | ✅ | ✅ 已实现 | 无变化 |
| User | ✅ | ✅ | ✅ 已实现 | 无变化 |
| User Watch | ✅ | ✅ | ✅ 已实现 | 无变化 |
| **Webhooks** | ❌ | ✅ | ❌ 未实现 | **7.6.1 新增** |

---

## 🎯 实现建议

### 高优先级 (建议实现)

#### 1. Webhooks API (9个端点)
```python
# 建议的资源类结构
class WebhookResource(BaseResource):
    """
    Webhook 资源
    API: /rest/api/webhooks
    """

    async def create(self, webhook_data: dict) -> dict:
        """创建 webhook"""

    async def get_all(self, event: Optional[str] = None) -> dict:
        """获取所有 webhooks"""

    async def get(self, webhook_id: str) -> dict:
        """获取指定 webhook"""

    async def update(self, webhook_id: str, webhook_data: dict) -> dict:
        """更新 webhook"""

    async def delete(self, webhook_id: str) -> None:
        """删除 webhook"""

    async def get_latest_invocations(self, webhook_id: str) -> dict:
        """获取最近调用记录"""

    async def get_statistics(self, webhook_id: str) -> dict:
        """获取统计信息"""

    async def get_statistics_summary(self, webhook_id: str) -> dict:
        """获取统计摘要"""

    async def test(self, url: str) -> dict:
        """测试端点连接性"""
```

**使用场景**：
- CI/CD 集成：页面更新时触发构建
- 团队协作：内容变更通知到 Slack/Teams
- 自动化工作流：监控关键页面变化

---

### 中优先级

#### 2. Access Mode API (1个端点)
```python
class AccessModeResource(BaseResource):
    """
    访问模式资源
    API: /rest/api/accessmode
    """

    async def get(self) -> dict:
        """获取 Confluence 访问模式状态"""
```

**使用场景**：
- 系统健康检查
- 维护模式检测
- 自动化脚本的前置检查

---

### 低优先级

#### 3. Content Macro ID API (1个端点)
```python
# 在 ContentResource 中添加
async def get_macro_by_id(
    self,
    content_id: str,
    version: int,
    macro_id: str,
) -> dict:
    """
    通过 ID 获取宏体

    GET /rest/api/content/{id}/history/{version}/macro/id/{macroId}
    """
```

---

## 📈 版本兼容性建议

### 1. 动态 API 路径检测

建议实现版本检测机制：

```python
class ConfluenceClient(BaseHttpClient):
    def __init__(self, ...):
        super().__init__(...)
        self._api_version: Optional[str] = None

    async def detect_version(self) -> str:
        """检测 Confluence 版本"""
        # 通过 /rest/api/serverInfo 检测版本
        pass

    def get_audit_base_path(self) -> str:
        """根据版本返回正确的 Audit API 路径"""
        if self._api_version and self._api_version >= "7.0":
            return "/rest/api/audit"
        return "/rest/audit"
```

### 2. 功能可用性检查

```python
async def is_feature_available(self, feature: str) -> bool:
    """检查特定功能是否可用"""
    features = {
        "webhooks": lambda: self._api_version >= "7.0",
        "accessmode": lambda: self._api_version >= "7.0",
        "macro_id": lambda: self._api_version >= "7.0",
    }
    return features.get(feature, lambda: True)()
```

---

## 📝 总结

### 新增功能统计

| 类别 | 新增端点数 | 实现状态 | 优先级 |
|------|-----------|---------|--------|
| Webhooks API | 9 | ❌ 未实现 | 🔴 高 |
| Access Mode API | 1 | ❌ 未实现 | 🟡 中 |
| Content Macro ID | 1 | ❌ 未实现 | 🟢 低 |
| **总计** | **11** | **0/11** | - |

### 兼容性分析

**好消息**：
- ✅ 我们已实现的所有 API 在 7.6.1 中都保持兼容
- ✅ 没有破坏性变更
- ✅ 只有一个端点被标记为 deprecated（macro hash）

**建议行动**：
1. **立即实施**: 实现 Webhooks API（对企业用户很重要）
2. **近期实施**: 实现 Access Mode API（简单但有用）
3. **按需实施**: Macro ID API（高级功能，使用较少）
4. **版本检测**: 添加 Confluence 版本检测机制
5. **路径兼容**: 确保 Audit API 路径在不同版本下都能工作

---

## 🔗 参考资源

- **6.6.0 文档**: https://docs.atlassian.com/atlassian-confluence/REST/6.6.0/
- **7.6.1 文档**: https://docs.atlassian.com/ConfluenceServer/rest/7.6.1/
- **当前实现**: docs/CONFLUENCE_API_REGISTRY.md
