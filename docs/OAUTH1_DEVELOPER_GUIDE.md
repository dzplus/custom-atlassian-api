# OAuth 1.0a 开发者接入指南

本文面向需要通过 `custom-atlassian-api` 访问 Jira、Confluence 或 Tempo
Server/Data Center REST API 的开发者。

SDK 支持 Atlassian Application Links 的三方 OAuth 1.0a（3LO）流程，并使用
RSA-SHA1 对每个 REST 请求签名。完成首次用户授权后，业务代码不再需要保存
Atlassian 用户名和密码。

> Confluence 7.16.x 和 Jira 8.13.x 使用本文的 OAuth 1.0a 流程。
> Confluence OAuth 2.0 Provider 从 7.17 开始提供，Jira OAuth 2.0 Provider
> 从 8.22 开始提供，它们不是本文描述的协议。

## 1. 安装 OAuth 支持

OAuth 是可选依赖。Basic 和 Session 用户不需要安装 RSA 加密依赖。

```bash
uv add "custom-atlassian-api[oauth]"
```

从 Git 仓库安装时：

```bash
uv add \
  "custom-atlassian-api[oauth] @ git+https://github.com/dzplus/custom-atlassian-api.git"
```

## 2. 生成 RSA 密钥

每个 OAuth consumer 应使用独立密钥。私钥只保存在客户端环境，管理员只需要
公钥。同一个内部客户端同时连接 Jira 和 Confluence 时，可以在两个产品中
登记相同的 Consumer Key 和公钥；如果希望独立轮换和缩小泄露影响面，也可以
为两个产品分别生成密钥。

```bash
mkdir -p ~/.config/custom-atlassian-api

openssl genrsa \
  -out ~/.config/custom-atlassian-api/atlassian-oauth1-private.pem 2048

openssl rsa \
  -in ~/.config/custom-atlassian-api/atlassian-oauth1-private.pem \
  -pubout \
  -out ~/.config/custom-atlassian-api/atlassian-oauth1-public.pem

chmod 600 ~/.config/custom-atlassian-api/atlassian-oauth1-private.pem
```

## 3. 请管理员创建 Incoming Application Link

Confluence 的入口是：

```text
右上角齿轮
→ General Configuration / 常规配置
→ Application links / 应用程序链接
```

直接地址通常是：

```text
https://<confluence-host>/plugins/servlet/applinks/listApplicationLinks
```

Jira 的入口是：

```text
右上角齿轮
→ Applications / 应用程序
→ Application links / 应用程序链接
```

直接地址通常是：

```text
https://<jira-host>/plugins/servlet/applinks/listApplicationLinks
```

在“输入要链接的应用程序 URL”中填写客户端服务地址。如果只是 CLI 或 SDK
demo，没有独立服务，可以填写项目仓库 URL。页面提示无法从 URL 获取响应时
可以继续。

第一步：

- Application Name：客户端名称，例如 `my-atlassian-client`
- Application Type：`Generic Application`
- 勾选 `Create incoming link`
- 不创建双向链接

第二步：

- Consumer Key：开发者和管理员约定的稳定唯一值
- Consumer Name：便于用户识别的名称
- Public Key：上一步生成的 PEM 公钥
- Callback URL：OOB 模式可以留空

不要为普通 3LO 客户端启用：

- 2-Legged OAuth
- Allow user impersonation
- Trusted Applications
- Basic Access

配置完成后，管理员只需把最终 Consumer Key 告诉开发者，不需要传递私钥或
用户密码。

## 4. 首次三段授权

以下代码获取 request token，生成用户授权 URL，再用页面显示的 verifier
换取 access token。把 `base_url` 指向 Jira 或 Confluence 即可：

```python
import asyncio
from pathlib import Path

from atlassian import AtlassianOAuth1Flow


async def authorize() -> None:
    private_key = Path(
        "~/.config/custom-atlassian-api/atlassian-oauth1-private.pem"
    ).expanduser().read_text()

    flow = AtlassianOAuth1Flow(
        base_url="https://jira.example.com",
        consumer_key="my-atlassian-client",
        private_key=private_key,
        callback_uri="oob",
    )

    request_token = await flow.fetch_request_token()
    print(flow.build_authorization_url(request_token))

    verifier = input("Verifier: ").strip()
    access_token = await flow.exchange_access_token(
        request_token=request_token,
        verifier=verifier,
    )

    # 交给调用方的密钥管理系统保存，不要打印或提交到 Git。
    token_payload = access_token.as_dict()
    # persist_to_secret_store(token_payload)


asyncio.run(authorize())
```

Jira 和 Confluence 使用相同的三段 OAuth 端点：

```text
POST /plugins/servlet/oauth/request-token
GET  /plugins/servlet/oauth/authorize?oauth_token=...
POST /plugins/servlet/oauth/access-token
```

`request_token` 是短期临时凭据。真正需要长期保存的是
`exchange_access_token()` 返回的 access token。

## 5. 使用 access token 调用 REST API

### 5.1 Confluence

```python
import asyncio
from pathlib import Path

from atlassian import ConfluenceClient, OAuth1Config, OAuth1Token


async def main() -> None:
    private_key = Path(
        "~/.config/custom-atlassian-api/atlassian-oauth1-private.pem"
    ).expanduser().read_text()

    stored_token = OAuth1Token(
        oauth_token="从安全存储读取",
        oauth_token_secret="从安全存储读取",
    )
    oauth1 = OAuth1Config.from_access_token(
        consumer_key="my-confluence-client",
        private_key=private_key,
        token=stored_token,
    )

    async with ConfluenceClient(
        base_url="https://confluence.example.com",
        auth_mode="oauth1",
        oauth1=oauth1,
    ) as confluence:
        page = await confluence.content.get("123456")
        print(page.title)


asyncio.run(main())
```

`OAuth1Config` 也可以直接构造：

```python
oauth1 = OAuth1Config(
    consumer_key="my-confluence-client",
    private_key=private_key,
    access_token=stored_access_token,
    access_token_secret=stored_access_token_secret,
)
```

相同配置也可以传给 `JiraClient` 和 `TempoClient`。

### 5.2 Jira

Jira 必须使用从 Jira 自己换取的 access token，不能使用 Confluence
返回的 token：

```python
import asyncio
from pathlib import Path

from atlassian import JiraClient, OAuth1Config, OAuth1Token


async def main() -> None:
    private_key = Path(
        "~/.config/custom-atlassian-api/atlassian-oauth1-private.pem"
    ).expanduser().read_text()
    stored_token = OAuth1Token(
        oauth_token="从 Jira token 存储读取",
        oauth_token_secret="从 Jira token 存储读取",
    )
    oauth1 = OAuth1Config.from_access_token(
        consumer_key="my-atlassian-client",
        private_key=private_key,
        token=stored_token,
    )

    async with JiraClient(
        base_url="https://jira.example.com",
        auth_mode="oauth1",
        oauth1=oauth1,
    ) as jira:
        myself = await jira.get_json("/rest/api/2/myself")
        print(myself["name"])


asyncio.run(main())
```

Tempo 是 Jira 插件时，通常使用 Jira Base URL 和 Jira OAuth token，不需要
第三次授权。

## 6. 回调模式

CLI 和人工测试推荐 `callback_uri="oob"`。用户允许访问后，Atlassian 页面会
直接显示 verifier。

Web 服务可以把 `callback_uri` 设置成自己的 HTTPS 回调地址。收到回调里的
verifier 后，仍然调用 `exchange_access_token()`。回调路由、CSRF state、
用户会话关联和 token 数据库存储属于应用层，SDK 不会替业务框架做决定。

## 7. Token 存储和撤销

至少需要保存：

```json
{
  "oauth_token": "...",
  "oauth_token_secret": "..."
}
```

同时保留对应的 Base URL、Consumer Key 和 RSA 私钥引用。生产系统建议使用
以下联合键保存 token：

```text
(业务用户 ID, Atlassian Base URL, Consumer Key)
```

Jira 和 Confluence 必须是两条独立记录。建议：

- 生产环境使用 Secrets Manager、Vault 或加密数据库字段。
- 本地文件权限设为 `0600`。
- 不记录完整 token、私钥或 OAuth Authorization Header。
- 不把 token 或私钥提交到 Git。

用户可以在 Jira 或 Confluence 的个人 OAuth Access Tokens 页面撤销对应
授权。撤销后，SDK 请求会收到 `401`，需要对该产品重新执行三段授权。

## 8. 异常处理

授权流程的统一异常是 `AtlassianOAuthError`：

```python
from atlassian import AtlassianOAuthError

try:
    request_token = await flow.fetch_request_token()
except AtlassianOAuthError as exc:
    logger.error("OAuth authorization failed: %s", exc)
```

常见错误：

| 错误 | 原因 |
|---|---|
| `oauth_problem=consumer_key_unknown` | Application Link 尚未创建，或 Consumer Key 不一致 |
| `oauth_problem=signature_invalid` | 公钥与本地私钥不匹配，或签名 URL 与实际访问 URL 不一致 |
| HTTP 401 | access token 已撤销、过期或不属于当前 consumer |
| HTTP 403 | 授权用户本身没有目标资源权限 |
| SOCKS proxy 依赖错误 | 本机代理环境变量被 HTTPX 读取；内网直连时传 `trust_env=False` |

反向代理环境必须保证 SDK 使用的 `base_url` 与 Jira 或 Confluence 对外公布的
Base URL 一致，并保证客户端和服务器时钟同步。

## 9. 可运行 demo

仓库为 Confluence 和 Jira 分别提供 CLI。它们共享同一套 OAuth 实现，但使用
独立的环境变量和 token 文件。

Confluence：

```bash
export CONFLUENCE_URL=https://confluence.example.com
export CONFLUENCE_OAUTH_CONSUMER_KEY=my-confluence-client
export CONFLUENCE_OAUTH_PRIVATE_KEY_FILE=\
"$HOME/.config/custom-atlassian-api/atlassian-oauth1-private.pem"

uv run python -m examples.confluence_oauth1_demo authorize
```

后续复用已保存的 token：

```bash
uv run python -m examples.confluence_oauth1_demo request \
  --api-path '/rest/api/space?limit=1'
```

Demo 负责终端交互和本地 token 文件；OAuth 协议、RSA 签名和 REST 客户端认证
全部使用 SDK 的公共实现。

Jira：

```bash
export JIRA_URL=https://jira.example.com
export JIRA_OAUTH_CONSUMER_KEY=my-jira-client
export JIRA_OAUTH_PRIVATE_KEY_FILE=\
"$HOME/.config/custom-atlassian-api/atlassian-oauth1-private.pem"

uv run python -m examples.jira_oauth1_demo authorize
```

后续复用 Jira token：

```bash
uv run python -m examples.jira_oauth1_demo request \
  --api-path '/rest/api/2/project'
```

两个 Demo 的默认文件不会互相覆盖：

```text
~/.config/custom-atlassian-api/confluence-oauth1.json
~/.config/custom-atlassian-api/jira-oauth1.json
```

读取 token 时，Demo 还会校验文件中的 Base URL 和 Consumer Key；即使误传了
另一个产品的 token 文件，也会在发送请求前报错。授权时如果目标文件已经属于
另一个 Base URL 或 Consumer Key，Demo 会拒绝覆盖。
