# Confluence OAuth 1.0a demo

这个 demo 面向 Confluence Data Center 7.16.x 的 Application Links OAuth
1.0a，使用 RSA-SHA1 签名。它不会使用或保存 Confluence 用户密码。

## 1. 生成 demo 密钥

```bash
mkdir -p ~/.config/custom-atlassian-api
openssl genrsa \
  -out ~/.config/custom-atlassian-api/confluence-oauth1-private.pem 2048
openssl rsa \
  -in ~/.config/custom-atlassian-api/confluence-oauth1-private.pem \
  -pubout \
  -out ~/.config/custom-atlassian-api/confluence-oauth1-public.pem
chmod 600 ~/.config/custom-atlassian-api/confluence-oauth1-private.pem
```

## 2. 创建 Incoming Application Link

这一步需要 Confluence 管理员操作。在 Confluence 的 Application Links
中创建一个传入连接：

- Consumer key：`custom-atlassian-api-demo`
- Consumer name：`custom-atlassian-api OAuth demo`
- Public key：`confluence-oauth1-public.pem` 的内容

其他 Application Link 的 token 绑定了各自的 consumer key 和私钥，不能复用。

## 3. 执行三段授权

```bash
export CONFLUENCE_URL=https://confluence.example.com
export CONFLUENCE_OAUTH_CONSUMER_KEY=custom-atlassian-api-demo
export CONFLUENCE_OAUTH_PRIVATE_KEY_FILE=\
"$HOME/.config/custom-atlassian-api/confluence-oauth1-private.pem"

uv run python -m examples.confluence_oauth1_demo authorize
```

Demo 默认不读取系统代理环境变量，避免 SOCKS 配置干扰内网 Confluence。
确实需要代理时传 `--trust-env`。

程序会：

1. 调用 `/plugins/servlet/oauth/request-token`。
2. 打开 `/plugins/servlet/oauth/authorize`，由用户点击允许。
3. 提示输入 Confluence 显示的 verifier。
4. 调用 `/plugins/servlet/oauth/access-token`。
5. 将 token 以 `0600` 权限写入
   `~/.config/custom-atlassian-api/confluence-oauth1.json`。
6. 使用 OAuth 签名调用 `/rest/api/content?limit=1`。

以后可以直接复用 token：

```bash
uv run python -m examples.confluence_oauth1_demo request \
  --api-path '/rest/api/space?limit=1'
```

Confluence 的“查看 OAuth Access Tokens”页面会列出完成授权的 demo
consumer。撤销该条 token 后，`request` 命令应返回认证失败。
