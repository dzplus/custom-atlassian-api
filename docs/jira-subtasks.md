# Jira 子任务排序与换父级

## 排序

```python
await jira.issue.reorder_subtasks("DEMO-100", original=0, current=1)
allowed = await jira.issue.can_reorder_subtasks("DEMO-100")
```

参数是父任务 Key 和从 0 开始的兄弟列表位置。请求为
`POST /rest/api/2/issue/DEMO-100/subtask/move`，JSON 同时包含 `original` 和 `current`。
GET 同一资源只表示排序能力。

旧方法 `move_subtasks(issue, new_parent_issue_key)` 错把排序解释为换父级，
该调用不再接受。迁移到 `reparent_subtask`，不可把父任务 Key 当排序位置。
`move_subtasks(parent, original, current)` 和 `can_move_subtask(parent)`
保留为弃用别名，产生 `DeprecationWarning`。

## 保留原单换父级

```python
preview = await jira.issue.preview_reparent_subtask("DEMO-101", "DEMO-200")
# CLI 展示 preview 的 subtask、source_parent、target_parent、supported、can_move。
result = await jira.issue.reparent_subtask("DEMO-101", "DEMO-200")
# status == "moved"：parent 与双方子任务列表已回读核对。
# status == "no_change"：已经在目标父级，未提交表单。
```

当前执行支持范围是 **Jira Server 8.13.5、Basic 认证、站点部署在 URL 根目录**。
其他版本或认证方式仍可只读预览；执行明确抛出 `unsupported_server`。
此限制表示本库已验证的范围，不表示其他版本的 Jira 没有网页迁移能力。
无需安装额外插件。HTTP、认证和 Cookie 都复用 `JiraClient`。
同一个客户端的网页迁移必须串行执行，因为 Jira 向导使用会话状态。

源必须是已有子任务，目标必须是同项目的非子任务。调用者需要能浏览三张单，
并具有源单的 Move Issues 权限；最终表单还会接受 Jira 的实时权限与业务校验。
跨项目迁移不在这个方法的范围内。

执行读取网页上的 `jiraform`、`atl_token` 和表单 action，选择
`move.subtask.parent.operation.name`，随后向 `MoveSubTaskParent.jspa`
提交 `parentIssue`。只允许预期的同站点页面跳转；不会关闭 CSRF 校验。
提交前再次核对源父级，提交后按原单 ID/Key、真实 parent、源/目标子任务列表验真。
请求仅包含父级选择与表单控制字段，不提交状态、负责人、报告人或业务日期。
Jira 自身会增加迁移历史、更新系统 `updated` 时间，并可能触发实例配置的自动化规则。

错误类型为 `atlassian.jira.resources.subtask_parent.SubtaskReparentError`，
稳定错误码在异常的 `code` 属性：

| code | 调用方处理 |
| --- | --- |
| unsupported_server / unsupported_form | 使用网页操作，核对版本、认证或自定义表单 |
| permission_denied / move_rejected | 核对权限和目标，不自动改其他字段 |
| concurrent_change / inconsistent_state | 重新读取并展示现状 |
| result_unknown | 先回读原单 parent 和两边列表，禁止直接重放写请求 |

不存在或不可见的单据沿用客户端的 HTTP 错误；类型、项目不合法抛出 `ValueError`。
传输异常后会先回读；只要三方状态已一致就返回 `moved`，否则报告未知结果。

## 网页操作

打开源子任务，选择“更多 → 移动”，选择更改父问题的操作，下一步输入
同项目目标父任务，点击“更改父问题”。完成后检查源子任务的父级，以及
两个父任务的子任务列表。不要通过复制和删除替代原单迁移。

## 契约依据

- [Jira 8.13.5 REST：排序](https://docs.atlassian.com/software/jira/docs/api/REST/8.13.5/#api/2/issue/{issueIdOrKey}/subtask-moveSubTasks)：描述为兄弟任务排序；该版 Schema 漏列 `original`，实际请求与内置 `viewissue/subtasks/subtasks.js` 一致。
- [MoveSubTaskParent Java API](https://docs.atlassian.com/software/jira/docs/api/8.13.5/com/atlassian/jira/web/action/issue/MoveSubTaskParent.html)：网页 action 与 `setParentIssue`。
- [JRASERVER-68763](https://jira.atlassian.com/browse/JRASERVER-68763)：Server REST 换父级功能请求。这里封装网页操作，不宣称 REST 排序端点具备换父级能力。
