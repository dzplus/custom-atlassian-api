# Jira OAuth 1.0a demo

这个 demo 面向 Jira Server/Data Center 的 Application Links OAuth 1.0a，
使用 RSA-SHA1 签名。它不会使用或保存 Jira 用户密码。

Jira OAuth 2.0 Provider 从 Jira 8.22 开始提供。更早的 Jira 版本应使用本文
的 OAuth 1.0a 流程。

## 1. 生成 demo 密钥

已有 Confluence OAuth demo 密钥时可以复用同一对密钥；如果希望 Jira 和
Confluence 独立轮换，也可以生成 Jira 专用密钥：

```bash
mkdir -p ~/.config/custom-atlassian-api
openssl genrsa \
  -out ~/.config/custom-atlassian-api/jira-oauth1-private.pem 2048
openssl rsa \
  -in ~/.config/custom-atlassian-api/jira-oauth1-private.pem \
  -pubout \
  -out ~/.config/custom-atlassian-api/jira-oauth1-public.pem
chmod 600 ~/.config/custom-atlassian-api/jira-oauth1-private.pem
```

私钥只保存在客户端；管理员只需要公钥。

## 2. 创建 Jira Incoming Application Link

使用 Jira 管理员账号进入：

```text
右上角齿轮
→ Applications / 应用程序
→ Application links / 应用程序链接
```

直接地址通常是：

```text
https://<jira-host>/plugins/servlet/applinks/listApplicationLinks
```

在“输入要链接的应用程序 URL”中填写客户端服务地址。CLI demo 没有服务地址
时可以填写项目仓库 URL。页面提示无法从 URL 获取响应时继续即可。

第一步：

- Application Name：`custom-atlassian-api Jira OAuth demo`
- Application Type：`Generic Application`
- 勾选 `Create incoming link`
- 不创建双向链接

第二步：

- Consumer Key：`custom-atlassian-api-jira`
- Consumer Name：`custom-atlassian-api Jira OAuth demo`
- Public Key：粘贴 `jira-oauth1-public.pem` 的内容
- Callback URL：OOB 模式可以留空

不要启用 2-Legged OAuth、用户模拟、Trusted Applications 或 Basic Access。

## 3. 执行 Jira 三段授权

```bash
export JIRA_URL=https://jira.example.com
export JIRA_OAUTH_CONSUMER_KEY=custom-atlassian-api-jira
export JIRA_OAUTH_PRIVATE_KEY_FILE=\
"$HOME/.config/custom-atlassian-api/jira-oauth1-private.pem"

uv run python -m examples.jira_oauth1_demo authorize
```

程序会：

1. 从 Jira 获取短期 request token。
2. 打开 Jira 授权页面。
3. 用户登录 Jira 并点击允许。
4. 提示输入 Jira 显示的 verifier。
5. 换取 Jira access token。
6. 以 `0600` 权限保存到
   `~/.config/custom-atlassian-api/jira-oauth1.json`。
7. 使用 OAuth 签名调用 `/rest/api/2/myself`。

Demo 默认不读取代理环境变量。确实需要代理时传 `--trust-env`。

## 4. 复用 Jira token

```bash
uv run python -m examples.jira_oauth1_demo request
```

也可以调用其他 Jira REST API：

```bash
uv run python -m examples.jira_oauth1_demo request \
  --api-path '/rest/api/2/project'
```

请求继承授权用户在 Jira 中的权限。HTTP `403` 通常表示该用户无权访问目标
资源；HTTP `401` 通常表示 token 已撤销、过期或 Consumer Key 不匹配。

## 5. 同时连接 Jira 和 Confluence

两个产品必须分别创建 Incoming Application Link，并分别完成一次用户授权。
可以复用 Consumer Key 和 RSA 密钥，但 access token 不能复用。

Demo 默认使用不同文件，不会相互覆盖：

```text
Jira:       ~/.config/custom-atlassian-api/jira-oauth1.json
Confluence: ~/.config/custom-atlassian-api/confluence-oauth1.json
```

Token 文件记录了 Base URL 和 Consumer Key。Demo 在发请求前会校验这两个
字段，避免把 Jira token 发给 Confluence，或反向误用。如果显式指定了相同的
`--token-file`，保存逻辑也会拒绝覆盖属于另一个产品或 Consumer Key 的文件。
