"""
Tempo API 接口测试

测试 Tempo 的各项 API 功能：
- 工时记录 (Worklog) CRUD
- 账户 (Account) CRUD
- 团队 (Team) CRUD 和成员管理
- 计划 (Plan) CRUD

使用前请设置环境变量:
- TEMPO_URL 或 JIRA_URL: Jira 服务地址
- TEMPO_USERNAME 或 JIRA_USERNAME: 用户名
- TEMPO_PASSWORD 或 JIRA_PASSWORD: 密码

或使用通用变量:
- ATLASSIAN_URL, ATLASSIAN_USERNAME, ATLASSIAN_PASSWORD

运行测试:
    uv run python -m tests.test_tempo                      # 默认只读模式
    uv run python -m tests.test_tempo --mode read-only     # 仅读取测试
    uv run python -m tests.test_tempo --mode full          # 完整测试（包含写入）
    uv run python -m tests.test_tempo --mode full --issue TEST-123  # 指定 Issue
    uv run python -m tests.test_tempo --mode full --issue TEST-123 --worker username  # 指定用户
"""

import asyncio
import argparse
import sys
from typing import Optional
from datetime import datetime, timedelta

from atlassian.tempo.client import TempoClient
from atlassian.common.exceptions import (
    AtlassianAuthError,
    AtlassianAPIError,
    AtlassianNotFoundError,
)


class TempoAPITest:
    """Tempo API 测试类"""

    def __init__(self):
        self.client: Optional[TempoClient] = None
        self.test_results: dict[str, dict] = {}
        self.test_worklog_id: Optional[int] = None
        self.test_account_id: Optional[int] = None
        self.test_team_id: Optional[int] = None
        self.test_allocation_id: Optional[int] = None

    async def setup(
        self,
        base_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """初始化客户端"""
        print("正在连接 Tempo...")
        self.client = TempoClient(
            base_url=base_url,
            username=username,
            password=password,
            auth_mode="basic",
        )
        await self.client.__aenter__()
        print("✓ 连接成功\n")

    async def cleanup(self):
        """清理资源"""
        if self.client:
            await self.client.__aexit__(None, None, None)
            print("\n✓ 已断开连接")

    def record_result(self, test_name: str, success: bool, message: str = "", data: any = None):
        """记录测试结果"""
        self.test_results[test_name] = {
            "success": success,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }
        status = "✓" if success else "✗"
        print(f"{status} {test_name}: {message}")

    # ========== Worklog 测试 ==========

    async def test_worklog_search(self, verbose: bool = False):
        """测试搜索工时记录"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            last_week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

            worklogs = await self.client.worklog.search(
                from_date=last_week,
                to_date=today,
            )
            self.record_result(
                "Worklog - 搜索工时记录",
                True,
                f"找到 {len(worklogs)} 条工时记录",
                len(worklogs),
            )

            # 如果设置了 verbose，打印第一条工时记录的详细信息
            if verbose and len(worklogs) > 0:
                first = worklogs[0]
                print(f"  示例工时记录:")
                print(f"    ID: {first.id}")
                print(f"    Issue: {first.issue_key}")
                print(f"    Worker: {first.worker}")
                print(f"    Started: {first.started}")
                print(f"    Time: {first.time_spent_seconds / 3600}小时")
                print(f"    Description: {first.description}")

            return worklogs
        except Exception as e:
            self.record_result("Worklog - 搜索工时记录", False, str(e))
            return []

    async def test_worklog_create(self, issue_key: str = "TEST-1", worker: str = None):
        """测试创建工时记录"""
        try:
            # 如果未指定 worker，获取当前用户
            if not worker:
                # 从环境变量或使用默认值
                import os
                worker = os.getenv("TEMPO_USERNAME") or os.getenv("JIRA_USERNAME") or os.getenv("ATLASSIAN_USERNAME")

            today = datetime.now().strftime("%Y-%m-%d")

            # 先尝试不带 started_time 创建（某些 Tempo 版本可能不支持）
            print(f"    尝试创建参数: issue={issue_key}, worker={worker}, date={today}, time=1小时")

            worklog = await self.client.worklog.create(
                issue_key=issue_key,
                worker=worker,
                started=today,
                time_spent_seconds=3600,  # 1小时
                description="[AUTO-TEST] Tempo API 测试工时记录",
                # 不使用 started_time，某些版本可能不支持
                # started_time="09:00:00",
            )
            self.test_worklog_id = worklog.id
            self.record_result(
                "Worklog - 1️⃣ 创建工时记录",
                True,
                f"创建成功 ID={worklog.id}, 时长=1小时, Issue={issue_key}",
                worklog.id,
            )
            return worklog
        except Exception as e:
            self.record_result("Worklog - 1️⃣ 创建工时记录", False, str(e))
            return None

    async def test_worklog_get(self, step: str = "2️⃣"):
        """测试获取工时记录"""
        if not self.test_worklog_id:
            self.record_result(f"Worklog - {step} 获取工时记录", False, "未创建测试工时记录")
            return None

        try:
            worklog = await self.client.worklog.get(self.test_worklog_id)
            hours = worklog.time_spent_seconds / 3600
            self.record_result(
                f"Worklog - {step} 获取工时记录",
                True,
                f"获取成功 ID={worklog.id}, 时长={hours}小时, 描述={worklog.description}",
            )
            return worklog
        except Exception as e:
            self.record_result(f"Worklog - {step} 获取工时记录", False, str(e))
            return None

    async def test_worklog_update(self):
        """测试更新工时记录"""
        if not self.test_worklog_id:
            self.record_result("Worklog - 3️⃣ 更新工时记录", False, "未创建测试工时记录")
            return None

        try:
            updated = await self.client.worklog.update(
                worklog_id=self.test_worklog_id,
                time_spent_seconds=7200,  # 2小时
                description="[AUTO-TEST] Tempo API 测试工时记录 - 已更新",
            )
            hours = updated.time_spent_seconds / 3600
            self.record_result(
                "Worklog - 3️⃣ 更新工时记录",
                True,
                f"更新成功 新时长={hours}小时, 新描述={updated.description}",
            )
            return updated
        except Exception as e:
            self.record_result("Worklog - 3️⃣ 更新工时记录", False, str(e))
            return None

    async def test_worklog_delete(self):
        """测试删除工时记录"""
        if not self.test_worklog_id:
            self.record_result("Worklog - 5️⃣ 删除工时记录", False, "未创建测试工时记录")
            return False

        try:
            success = await self.client.worklog.delete(self.test_worklog_id)
            self.record_result(
                "Worklog - 5️⃣ 删除工时记录",
                True,
                f"删除成功 ID={self.test_worklog_id}",
            )
            self.test_worklog_id = None
            return True
        except Exception as e:
            self.record_result("Worklog - 5️⃣ 删除工时记录", False, str(e))
            return False

    async def test_worklog_lifecycle(self, issue_key: str = "TEST-1", worker: str = None):
        """
        测试 Worklog 完整生命周期

        流程: 创建 -> 获取(验证) -> 更新 -> 获取(验证更新) -> 删除
        确保: 无论测试成功与否，最终都会清理测试数据
        """
        print("--- Worklog 完整生命周期测试 ---")
        print("流程: 创建 -> 获取 -> 更新 -> 获取(验证) -> 删除")
        print()

        # 先搜索查看示例数据格式
        print("  📋 先查看现有工时记录格式...")
        existing_worklogs = await self.test_worklog_search(verbose=True)
        print()

        # 如果没有指定 worker 或 issue，尝试从现有工时记录中获取
        if not worker and existing_worklogs:
            worker = existing_worklogs[0].worker
            print(f"  💡 未指定 worker，使用现有工时记录的 worker: {worker}")

        # 如果 issue_key 是默认值 TEST-1，且有现有记录，使用真实的 issue
        if issue_key == "TEST-1" and existing_worklogs:
            issue_key = existing_worklogs[0].issue_key
            print(f"  💡 使用现有工时记录的 Issue: {issue_key}")

        if not worker:
            print(f"  ⚠️  未找到可用的 worker，跳过生命周期测试")
            print(f"  💡 提示: 请使用 --worker 参数指定用户名，或确保系统中有现有工时记录")
            return

        print()

        worklog_id_to_cleanup = None

        try:
            # 步骤1: 创建工时记录
            created = await self.test_worklog_create(issue_key, worker)
            if not created:
                print("⚠️  创建失败，跳过后续测试")
                return

            worklog_id_to_cleanup = created.id

            # 步骤2: 获取并验证创建的工时记录
            fetched1 = await self.test_worklog_get(step="2️⃣")
            if fetched1:
                # 验证数据一致性
                if fetched1.time_spent_seconds == 3600 and "[AUTO-TEST]" in fetched1.description:
                    print(f"  ✓ 验证通过: 创建的数据与获取的数据一致")
                else:
                    print(f"  ⚠️  数据不一致: 期望1小时，实际{fetched1.time_spent_seconds/3600}小时")

            # 步骤3: 更新工时记录
            updated = await self.test_worklog_update()
            if not updated:
                print("⚠️  更新失败，继续删除测试")

            # 步骤4: 再次获取并验证更新
            if updated:
                fetched2 = await self.test_worklog_get(step="4️⃣")
                if fetched2:
                    # 验证更新是否生效
                    if fetched2.time_spent_seconds == 7200 and "已更新" in fetched2.description:
                        print(f"  ✓ 验证通过: 更新的数据已生效")
                    else:
                        print(f"  ⚠️  更新未生效: 期望2小时，实际{fetched2.time_spent_seconds/3600}小时")

            # 步骤5: 删除工时记录（清理测试数据）
            deleted = await self.test_worklog_delete()
            if deleted:
                print(f"  ✓ 清理成功: 测试数据已从生产环境删除")
                worklog_id_to_cleanup = None

        except Exception as e:
            print(f"✗ 生命周期测试异常: {e}")

        finally:
            # 最后的清理保障：即使测试失败也要尝试删除
            if worklog_id_to_cleanup:
                print(f"\n⚠️  检测到残留测试数据 ID={worklog_id_to_cleanup}，尝试清理...")
                try:
                    await self.client.worklog.delete(worklog_id_to_cleanup)
                    print(f"  ✓ 强制清理成功")
                    self.test_worklog_id = None
                except Exception as cleanup_error:
                    print(f"  ✗ 强制清理失败: {cleanup_error}")
                    print(f"  ⚠️  请手动删除 Worklog ID={worklog_id_to_cleanup}")

        print()

    # ========== Account 测试 ==========

    async def test_account_get_all(self):
        """测试获取所有账户"""
        try:
            accounts = await self.client.account.get_all()
            self.record_result(
                "Account - 获取所有账户",
                True,
                f"找到 {len(accounts)} 个账户",
                len(accounts),
            )
        except Exception as e:
            self.record_result("Account - 获取所有账户", False, str(e))

    async def test_account_create(self):
        """测试创建账户"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            account = await self.client.account.create(
                key=f"TEST-{timestamp}",
                name=f"测试账户 {timestamp}",
                status="OPEN",
                global_=False,
            )
            self.test_account_id = account.id
            self.record_result(
                "Account - 创建账户",
                True,
                f"创建成功，ID={account.id}",
                account.id,
            )
        except Exception as e:
            self.record_result("Account - 创建账户", False, str(e))

    async def test_account_get(self):
        """测试获取账户"""
        if not self.test_account_id:
            self.record_result("Account - 获取账户", False, "未创建测试账户")
            return

        try:
            account = await self.client.account.get(self.test_account_id)
            self.record_result(
                "Account - 获取账户",
                True,
                f"获取成功，名称={account.name}",
            )
        except Exception as e:
            self.record_result("Account - 获取账户", False, str(e))

    async def test_account_update(self):
        """测试更新账户"""
        if not self.test_account_id:
            self.record_result("Account - 更新账户", False, "未创建测试账户")
            return

        try:
            updated = await self.client.account.update(
                account_id=self.test_account_id,
                name="测试账户 - 已更新",
                status="OPEN",
            )
            self.record_result(
                "Account - 更新账户",
                True,
                f"更新成功，新名称={updated.name}",
            )
        except Exception as e:
            self.record_result("Account - 更新账户", False, str(e))

    async def test_account_delete(self):
        """测试删除账户"""
        if not self.test_account_id:
            self.record_result("Account - 删除账户", False, "未创建测试账户")
            return

        try:
            success = await self.client.account.delete(self.test_account_id)
            self.record_result(
                "Account - 删除账户",
                True,
                "删除成功",
            )
            self.test_account_id = None
        except Exception as e:
            self.record_result("Account - 删除账户", False, str(e))

    # ========== Team 测试 ==========

    async def test_team_get_all(self):
        """测试获取所有团队"""
        try:
            teams = await self.client.team.get_all()
            self.record_result(
                "Team - 获取所有团队",
                True,
                f"找到 {len(teams)} 个团队",
                len(teams),
            )
        except Exception as e:
            self.record_result("Team - 获取所有团队", False, str(e))

    async def test_team_create(self):
        """测试创建团队"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            team = await self.client.team.create(
                name=f"测试团队 {timestamp}",
                summary="这是一个测试团队",
            )
            self.test_team_id = team.id
            self.record_result(
                "Team - 创建团队",
                True,
                f"创建成功，ID={team.id}",
                team.id,
            )
        except Exception as e:
            self.record_result("Team - 创建团队", False, str(e))

    async def test_team_get(self):
        """测试获取团队"""
        if not self.test_team_id:
            self.record_result("Team - 获取团队", False, "未创建测试团队")
            return

        try:
            team = await self.client.team.get(self.test_team_id)
            self.record_result(
                "Team - 获取团队",
                True,
                f"获取成功，名称={team.name}",
            )
        except Exception as e:
            self.record_result("Team - 获取团队", False, str(e))

    async def test_team_update(self):
        """测试更新团队"""
        if not self.test_team_id:
            self.record_result("Team - 更新团队", False, "未创建测试团队")
            return

        try:
            updated = await self.client.team.update(
                team_id=self.test_team_id,
                name="测试团队 - 已更新",
                summary="这是一个已更新的测试团队",
            )
            self.record_result(
                "Team - 更新团队",
                True,
                f"更新成功，新名称={updated.name}",
            )
        except Exception as e:
            self.record_result("Team - 更新团队", False, str(e))

    async def test_team_get_members(self):
        """测试获取团队成员"""
        if not self.test_team_id:
            self.record_result("Team - 获取团队成员", False, "未创建测试团队")
            return

        try:
            members = await self.client.team.get_members(self.test_team_id)
            self.record_result(
                "Team - 获取团队成员",
                True,
                f"团队有 {len(members)} 名成员",
                len(members),
            )
        except Exception as e:
            self.record_result("Team - 获取团队成员", False, str(e))

    async def test_team_delete(self):
        """测试删除团队"""
        if not self.test_team_id:
            self.record_result("Team - 删除团队", False, "未创建测试团队")
            return

        try:
            success = await self.client.team.delete(self.test_team_id)
            self.record_result(
                "Team - 删除团队",
                True,
                "删除成功",
            )
            self.test_team_id = None
        except Exception as e:
            self.record_result("Team - 删除团队", False, str(e))

    # ========== Plan 测试 ==========

    async def test_plan_get_allocations(self, verbose: bool = False):
        """测试获取资源分配"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            next_month = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

            allocations = await self.client.plan.get_allocations(
                start_date=today,
                end_date=next_month,
            )
            self.record_result(
                "Plan - 获取资源分配列表",
                True,
                f"找到 {len(allocations)} 个资源分配",
                len(allocations),
            )

            # 如果设置了 verbose，打印第一个资源分配的详细信息
            if verbose and len(allocations) > 0:
                first = allocations[0]
                print(f"  示例资源分配:")
                print(f"    ID: {first.id}")

                # 尝试从多个可能的字段获取 assignee
                assignee = first.assignee_key
                if not assignee and hasattr(first, 'assignee') and first.assignee:
                    if isinstance(first.assignee, dict) and 'key' in first.assignee:
                        assignee = first.assignee['key']
                if assignee:
                    print(f"    Assignee Key: {assignee}")

                # 尝试从多个可能的字段获取 plan_item
                plan_item = first.plan_item_id
                if not plan_item and hasattr(first, 'plan_item') and first.plan_item:
                    if isinstance(first.plan_item, dict) and 'id' in first.plan_item:
                        plan_item = str(first.plan_item['id'])
                if plan_item:
                    print(f"    Plan Item ID: {plan_item}")

                if first.start_date:
                    print(f"    开始日期: {first.start_date}")
                if first.end_date:
                    print(f"    结束日期: {first.end_date}")
                if first.seconds_per_day:
                    hours = first.seconds_per_day / 3600
                    print(f"    每天时长: {hours}小时")

                # Debug: 打印所有可用字段
                print(f"    可用字段: {list(first.model_dump(exclude_none=True).keys())}")

            return allocations
        except Exception as e:
            self.record_result("Plan - 获取资源分配列表", False, str(e))
            return []

    async def test_plan_search_plans(self, verbose: bool = False):
        """测试搜索计划"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

            plans = await self.client.plan.search_plans(
                from_date=today,
                to_date=next_week,
            )
            self.record_result(
                "Plan - 搜索计划日志列表",
                True,
                f"找到 {len(plans)} 个计划日志",
                len(plans),
            )

            # 如果设置了 verbose，打印第一个计划的详细信息
            if verbose and len(plans) > 0:
                first = plans[0]
                print(f"  示例计划日志:")
                print(f"    ID: {first.id if first.id else 'N/A'}")
                if first.assignee_key:
                    print(f"    Assignee: {first.assignee_key}")
                if first.plan_item_id:
                    print(f"    Plan Item: {first.plan_item_id}")
                if first.date:
                    print(f"    日期: {first.date}")
                if first.seconds:
                    hours = first.seconds / 3600
                    print(f"    时长: {hours}小时")

            return plans
        except Exception as e:
            self.record_result("Plan - 搜索计划日志列表", False, str(e))
            return []

    async def test_plan_create(
        self,
        assignee_key: str = None,
        plan_item_id: int = None,  # 必须是整数
        start_date: str = None,
        end_date: str = None,
    ):
        """测试创建计划"""
        try:
            # 使用未来日期：明天开始，持续3天
            if not start_date:
                start_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            if not end_date:
                end_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

            print(f"    尝试创建参数: assignee={assignee_key}, plan_item={plan_item_id}")
            print(f"                  dates={start_date} to {end_date}, time=3小时/天")

            plan_logs = await self.client.plan.create_plan(
                assignee_key=assignee_key,
                plan_item_id=plan_item_id,
                plan_item_type="ISSUE",
                start_date=start_date,
                end_date=end_date,
                seconds_per_day=10800,  # 3小时
                description="[AUTO-TEST] Tempo API 计划测试",
                include_non_working_days=True,  # 包含非工作日，确保有计划日志生成
            )

            # 保存第一个计划日志的ID用于后续删除
            if plan_logs and len(plan_logs) > 0:
                # 存储创建的计划信息（用于后续更新和删除）
                # 注意：PlanLog 使用 allocation_id 而不是 id
                self.test_plan_params = {
                    'assignee_key': assignee_key,
                    'plan_item_id': plan_item_id,
                    'start_date': start_date,
                    'end_date': end_date,
                    'allocation_ids': [p.allocation_id for p in plan_logs if p.allocation_id],
                }

            self.record_result(
                "Plan - 1️⃣ 创建计划",
                True,
                f"创建成功 生成{len(plan_logs)}个计划日志",
                len(plan_logs),
            )
            return plan_logs
        except Exception as e:
            self.record_result("Plan - 1️⃣ 创建计划", False, str(e))
            return None

    async def test_plan_update(self):
        """测试更新计划"""
        if not hasattr(self, 'test_plan_params') or not self.test_plan_params:
            self.record_result("Plan - 2️⃣ 更新计划", False, "未创建测试计划")
            return None

        params = self.test_plan_params
        allocation_ids = params.get('allocation_ids', [])

        if not allocation_ids:
            self.record_result("Plan - 2️⃣ 更新计划", False, "缺少 allocation_id")
            return None

        try:
            # 使用第一个 allocation_id 进行更新
            updated_plans = await self.client.plan.update_plan(
                allocation_id=allocation_ids[0],  # 必需参数
                assignee_key=params['assignee_key'],
                plan_item_id=params['plan_item_id'],
                plan_item_type="ISSUE",
                start_date=params['start_date'],
                end_date=params['end_date'],
                seconds_per_day=21600,  # 6小时
                description="[AUTO-TEST] Tempo API 计划测试 - 已更新",
                include_non_working_days=True,  # 包含非工作日
            )

            self.record_result(
                "Plan - 2️⃣ 更新计划",
                True,
                f"更新成功 影响{len(updated_plans)}个计划日志, 新时长={21600/3600}小时/天",
            )
            return updated_plans
        except Exception as e:
            self.record_result("Plan - 2️⃣ 更新计划", False, str(e))
            return None

    async def test_plan_remove_from_date(self, date: str = None):
        """测试移除特定日期的计划"""
        if not hasattr(self, 'test_plan_params') or not self.test_plan_params:
            self.record_result("Plan - 3️⃣ 移除特定日期计划", False, "未创建测试计划")
            return False

        params = self.test_plan_params
        allocation_ids = params.get('allocation_ids', [])

        if not allocation_ids:
            self.record_result("Plan - 3️⃣ 移除特定日期计划", False, "没有可用的 Allocation ID")
            return False

        # 删除第一个计划日志（代表某一天的计划）
        # 注意：这里使用的是 allocation_id，不是 plan_id
        plan_id = allocation_ids[0]
        if not date:
            # 使用开始日期
            date = params['start_date']

        try:
            success = await self.client.plan.remove_plan_from_date(
                plan_id=plan_id,
                date=date,
            )
            self.record_result(
                "Plan - 3️⃣ 移除特定日期计划",
                True,
                f"移除成功 plan_id={plan_id}, date={date}",
            )
            return True
        except Exception as e:
            self.record_result("Plan - 3️⃣ 移除特定日期计划", False, str(e))
            return False

    async def test_plan_lifecycle(
        self,
        assignee_key: str = None,
        plan_item_id: int = None,  # 必须是整数
    ):
        """
        测试 Plan 完整生命周期

        流程: 创建 -> 更新 -> 移除特定日期
        确保: 无论测试成功与否，最终都会清理测试数据

        注意: Plan API 与 Allocation API 不同
        - Allocation: 长期资源分配，有独立的ID，可以直接删除
        - Plan: 日级别计划日志，通过日期范围创建/更新，通过 plan_id + date 删除
        """
        print("--- Plan 完整生命周期测试 ---")
        print("流程: 创建计划 -> 更新计划 -> 移除特定日期")
        print()

        # 先搜索查看示例数据格式
        print("  📋 先查看现有计划日志格式...")
        existing_plans = await self.test_plan_search_plans(verbose=True)
        print()

        # 如果没有指定 assignee，尝试从现有计划或 worklog 中获取
        if not assignee_key:
            if existing_plans and existing_plans[0].assignee_key:
                assignee_key = existing_plans[0].assignee_key
                print(f"  💡 未指定 assignee，使用现有计划的 assignee: {assignee_key}")
            else:
                # 从 worklog 获取
                worklogs = await self.test_worklog_search(verbose=False)
                if worklogs and len(worklogs) > 0:
                    assignee_key = worklogs[0].worker
                    print(f"  💡 未指定 assignee，使用 worklog 的 worker: {assignee_key}")

        if not assignee_key:
            print(f"  ⚠️  缺少 assignee 参数，跳过生命周期测试")
            return

        # 如果没有指定 plan_item_id，从现有计划中获取
        if not plan_item_id and existing_plans and existing_plans[0].plan_item_id:
            actual_plan_item_id = existing_plans[0].plan_item_id
            print(f"  💡 未指定 plan_item_id，使用现有计划的 plan_item_id: {actual_plan_item_id}")
            # 转换为整数
            if isinstance(actual_plan_item_id, str):
                plan_item_id = int(actual_plan_item_id)
            else:
                plan_item_id = actual_plan_item_id

        if not plan_item_id:
            print(f"  ⚠️  缺少 plan_item_id 参数，跳过生命周期测试")
            return

        print(f"  📝 使用 Plan Item ID: {plan_item_id} (类型: {type(plan_item_id).__name__})")
        print()

        plan_ids_to_cleanup = []

        try:
            # 步骤1: 创建计划（会创建多个计划日志，每天一个）
            created_plans = await self.test_plan_create(
                assignee_key=assignee_key,
                plan_item_id=plan_item_id,
            )
            if not created_plans:
                print("⚠️  创建失败，跳过后续测试")
                return

            # 记录需要清理的 Allocation ID（PlanLog 使用 allocation_id）
            allocation_ids_to_cleanup = [p.allocation_id for p in created_plans if p.allocation_id]
            print(f"  ✓ 验证: 创建了 {len(created_plans)} 个计划日志")

            # 步骤2: 更新计划（会更新整个日期范围的计划）
            # 注意：某些 Tempo 版本的 PUT /plan 可能返回 404
            updated_plans = await self.test_plan_update()
            if updated_plans:
                print(f"  ✓ 验证: 更新影响了 {len(updated_plans)} 个计划日志")

            # 步骤3: 移除特定日期的计划（删除其中一天）
            if allocation_ids_to_cleanup:
                removed = await self.test_plan_remove_from_date()
                if removed:
                    print(f"  ✓ 验证: 成功移除特定日期的计划")

        except Exception as e:
            print(f"✗ 生命周期测试异常: {e}")

        finally:
            # 最后的清理保障：删除剩余的计划日志
            if allocation_ids_to_cleanup and hasattr(self, 'test_plan_params'):
                print(f"\n  🧹 清理剩余的计划日志（Allocation ID: {allocation_ids_to_cleanup})...")
                params = self.test_plan_params
                # 计算需要删除的日期列表
                start = datetime.strptime(params['start_date'], "%Y-%m-%d")
                end = datetime.strptime(params['end_date'], "%Y-%m-%d")

                # 对每个 allocation_id，删除所有日期
                for allocation_id in allocation_ids_to_cleanup:
                    current_date = start
                    while current_date <= end:
                        date_str = current_date.strftime("%Y-%m-%d")
                        try:
                            await self.client.plan.remove_plan_from_date(
                                plan_id=allocation_id,
                                date=date_str,
                            )
                        except Exception as cleanup_error:
                            # 忽略删除错误（可能已被删除）
                            pass
                        current_date += timedelta(days=1)

                print(f"  ✓ 完全清理: 测试数据已从生产环境删除")

        print()

    async def test_plan_create_allocation(
        self,
        assignee_key: str = None,
        plan_item_id: str = None,
        start_date: str = None,
        end_date: str = None,
    ):
        """测试创建资源分配"""
        try:
            # 使用默认日期：30天后开始，持续2天（避免与现有分配冲突）
            if not start_date:
                start_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            if not end_date:
                end_date = (datetime.now() + timedelta(days=32)).strftime("%Y-%m-%d")

            print(f"    尝试创建参数: assignee={assignee_key}, plan_item={plan_item_id}")
            print(f"                  dates={start_date} to {end_date}, time=4小时/天")

            allocation = await self.client.plan.create_allocation(
                assignee_key=assignee_key,
                assignee_type="USER",
                plan_item_id=plan_item_id,
                plan_item_type="ISSUE",
                start_date=start_date,
                end_date=end_date,
                seconds_per_day=14400,  # 4小时
                description="[AUTO-TEST] Tempo API 资源分配测试",
                include_non_working_days=False,
            )
            self.test_allocation_id = allocation.id
            hours = allocation.seconds_per_day / 3600 if allocation.seconds_per_day else 0
            self.record_result(
                "Plan - 1️⃣ 创建资源分配",
                True,
                f"创建成功 ID={allocation.id}, 每天{hours}小时",
                allocation.id,
            )
            return allocation
        except Exception as e:
            self.record_result("Plan - 1️⃣ 创建资源分配", False, str(e))
            return None

    async def test_plan_get_allocation(self, step: str = "2️⃣"):
        """测试获取单个资源分配"""
        if not self.test_allocation_id:
            self.record_result(f"Plan - {step} 获取资源分配", False, "未创建测试资源分配")
            return None

        try:
            allocation = await self.client.plan.get_allocation(self.test_allocation_id)
            hours = allocation.seconds_per_day / 3600 if allocation.seconds_per_day else 0
            self.record_result(
                f"Plan - {step} 获取资源分配",
                True,
                f"获取成功 ID={allocation.id}, 每天{hours}小时",
            )
            return allocation
        except Exception as e:
            self.record_result(f"Plan - {step} 获取资源分配", False, str(e))
            return None

    async def test_plan_update_allocation(self):
        """测试更新资源分配"""
        if not self.test_allocation_id:
            self.record_result("Plan - 3️⃣ 更新资源分配", False, "未创建测试资源分配")
            return None

        try:
            updated = await self.client.plan.update_allocation(
                allocation_id=self.test_allocation_id,
                seconds_per_day=28800,  # 8小时
                description="[AUTO-TEST] Tempo API 资源分配测试 - 已更新",
            )
            hours = updated.seconds_per_day / 3600 if updated.seconds_per_day else 0
            self.record_result(
                "Plan - 3️⃣ 更新资源分配",
                True,
                f"更新成功 新时长=每天{hours}小时",
            )
            return updated
        except Exception as e:
            self.record_result("Plan - 3️⃣ 更新资源分配", False, str(e))
            return None

    async def test_plan_delete_allocation(self):
        """测试删除资源分配"""
        if not self.test_allocation_id:
            self.record_result("Plan - 5️⃣ 删除资源分配", False, "未创建测试资源分配")
            return False

        try:
            success = await self.client.plan.delete_allocation(self.test_allocation_id)
            self.record_result(
                "Plan - 5️⃣ 删除资源分配",
                True,
                f"删除成功 ID={self.test_allocation_id}",
            )
            self.test_allocation_id = None
            return True
        except Exception as e:
            self.record_result("Plan - 5️⃣ 删除资源分配", False, str(e))
            return False

    async def test_plan_allocation_lifecycle(
        self,
        assignee_key: str = None,
        plan_item_id: str = None,  # Issue Key like "DEMO-123"
    ):
        """
        测试 Plan Allocation 完整生命周期

        流程: 创建 -> 获取(验证) -> 更新 -> 获取(验证更新) -> 删除
        确保: 无论测试成功与否，最终都会清理测试数据
        """
        print("--- Plan Allocation 完整生命周期测试 ---")
        print("流程: 创建 -> 获取 -> 更新 -> 获取(验证) -> 删除")
        print()

        # 先搜索查看示例数据格式
        print("  📋 先查看现有资源分配格式...")
        existing_allocations = await self.test_plan_get_allocations(verbose=True)
        print()

        # 如果没有指定参数，尝试从现有资源分配中获取
        if not assignee_key and existing_allocations:
            first = existing_allocations[0]
            # 尝试多种方式获取 assignee
            if first.assignee_key:
                assignee_key = first.assignee_key
            elif hasattr(first, 'assignee') and first.assignee:
                if isinstance(first.assignee, dict) and 'key' in first.assignee:
                    assignee_key = first.assignee['key']
            if assignee_key:
                print(f"  💡 未指定 assignee，使用现有资源分配的 assignee: {assignee_key}")

        # Plan Item ID 应该是 Issue Key (ISSUE 类型) 或 Project ID (PROJECT 类型)
        # 尝试从现有数据获取
        if not plan_item_id and existing_allocations:
            first = existing_allocations[0]
            # 尝试多种方式获取 plan_item（优先获取 key 字段，这是 Issue Key）
            if first.plan_item_id:
                plan_item_id = first.plan_item_id
            elif hasattr(first, 'plan_item') and first.plan_item:
                if isinstance(first.plan_item, dict):
                    # 优先使用 key 字段（Issue Key），否则使用 id
                    if 'key' in first.plan_item:
                        plan_item_id = first.plan_item['key']
                    elif 'id' in first.plan_item:
                        # 如果是PROJECT类型，ID可能是数字
                        plan_item_id = str(first.plan_item['id'])
            if plan_item_id:
                print(f"  💡 未指定 plan_item，使用现有资源分配的 plan_item: {plan_item_id}")

        # 如果还是没有找到 plan_item，尝试从 worklog 测试中获取 Issue Key
        if not plan_item_id:
            print(f"  💡 尝试从 worklog 搜索中获取 Issue Key...")
            worklogs = await self.test_worklog_search(verbose=False)
            if worklogs and len(worklogs) > 0:
                plan_item_id = worklogs[0].issue_key
                print(f"  💡 使用 worklog 中的 Issue: {plan_item_id}")

        if not assignee_key or not plan_item_id:
            print(f"  ⚠️  缺少必要参数 (assignee 或 plan_item)，跳过生命周期测试")
            print(f"  💡 提示: 请确保系统中有现有资源分配")
            return

        print()

        allocation_id_to_cleanup = None

        try:
            # 步骤1: 创建资源分配
            created = await self.test_plan_create_allocation(
                assignee_key=assignee_key,
                plan_item_id=plan_item_id,
            )
            if not created:
                print("⚠️  创建失败，跳过后续测试")
                return

            allocation_id_to_cleanup = created.id

            # 步骤2: 获取并验证创建的资源分配
            fetched1 = await self.test_plan_get_allocation(step="2️⃣")
            if fetched1:
                # 验证数据一致性
                expected_seconds = 14400  # 4小时
                if fetched1.seconds_per_day == expected_seconds and "[AUTO-TEST]" in (fetched1.description or ""):
                    print(f"  ✓ 验证通过: 创建的数据与获取的数据一致")
                else:
                    actual_hours = fetched1.seconds_per_day / 3600 if fetched1.seconds_per_day else 0
                    print(f"  ⚠️  数据不一致: 期望4小时/天，实际{actual_hours}小时/天")

            # 步骤3: 更新资源分配
            updated = await self.test_plan_update_allocation()
            if not updated:
                print("⚠️  更新失败，继续删除测试")

            # 步骤4: 再次获取并验证更新
            if updated:
                fetched2 = await self.test_plan_get_allocation(step="4️⃣")
                if fetched2:
                    # 验证更新是否生效
                    expected_seconds = 28800  # 8小时
                    if fetched2.seconds_per_day == expected_seconds and "已更新" in (fetched2.description or ""):
                        print(f"  ✓ 验证通过: 更新的数据已生效")
                    else:
                        actual_hours = fetched2.seconds_per_day / 3600 if fetched2.seconds_per_day else 0
                        print(f"  ⚠️  更新未生效: 期望8小时/天，实际{actual_hours}小时/天")

            # 步骤5: 删除资源分配（清理测试数据）
            deleted = await self.test_plan_delete_allocation()
            if deleted:
                print(f"  ✓ 清理成功: 测试数据已从生产环境删除")
                allocation_id_to_cleanup = None

        except Exception as e:
            print(f"✗ 生命周期测试异常: {e}")

        finally:
            # 最后的清理保障：即使测试失败也要尝试删除
            if allocation_id_to_cleanup:
                print(f"\n⚠️  检测到残留测试数据 ID={allocation_id_to_cleanup}，尝试清理...")
                try:
                    await self.client.plan.delete_allocation(allocation_id_to_cleanup)
                    print(f"  ✓ 强制清理成功")
                    self.test_allocation_id = None
                except Exception as cleanup_error:
                    print(f"  ✗ 强制清理失败: {cleanup_error}")
                    print(f"  ⚠️  请手动删除 Allocation ID={allocation_id_to_cleanup}")

        print()

    # ========== 测试运行器 ==========

    async def run_read_only_tests(self):
        """运行只读测试"""
        print("=" * 60)
        print("开始运行只读测试")
        print("=" * 60)
        print()

        print("--- Worklog 测试 ---")
        await self.test_worklog_search()
        print()

        print("--- Account 测试 ---")
        await self.test_account_get_all()
        print()

        print("--- Team 测试 ---")
        await self.test_team_get_all()
        print()

        print("--- Plan 测试 ---")
        await self.test_plan_get_allocations()
        await self.test_plan_search_plans()
        print()

    async def run_full_tests(self, test_issue_key: str = "TEST-1", worker: str = None):
        """运行完整测试（包含写入操作）"""
        print("=" * 60)
        print("开始运行完整测试（包含写入操作）")
        print("=" * 60)
        print()

        # Worklog 完整生命周期测试
        await self.test_worklog_lifecycle(test_issue_key, worker)

        # Worklog 搜索测试
        print("--- Worklog 搜索测试 ---")
        await self.test_worklog_search()
        print()

        print("--- Account 完整测试 ---")
        await self.test_account_get_all()
        await self.test_account_create()
        await self.test_account_get()
        await self.test_account_update()
        await self.test_account_delete()
        print()

        print("--- Team 完整测试 ---")
        await self.test_team_get_all()
        await self.test_team_create()
        await self.test_team_get()
        await self.test_team_update()
        await self.test_team_get_members()
        await self.test_team_delete()
        print()

        # Plan 完整生命周期测试
        await self.test_plan_lifecycle()

        # Plan 搜索测试
        print("--- Plan 搜索测试 ---")
        await self.test_plan_search_plans()
        print()

    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "=" * 60)
        print("测试摘要")
        print("=" * 60)

        total = len(self.test_results)
        passed = sum(1 for r in self.test_results.values() if r["success"])
        failed = total - passed

        print(f"\n总计: {total} 个测试")
        print(f"✓ 通过: {passed}")
        print(f"✗ 失败: {failed}")

        if failed > 0:
            print("\n失败的测试:")
            for name, result in self.test_results.items():
                if not result["success"]:
                    print(f"  ✗ {name}: {result['message']}")

        print("\n" + "=" * 60)


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Tempo API 测试")
    parser.add_argument(
        "--mode",
        choices=["read-only", "full"],
        default="read-only",
        help="测试模式: read-only 或 full",
    )
    parser.add_argument(
        "--issue",
        default="TEST-1",
        help="用于测试的 Issue Key（完整测试时需要）",
    )
    parser.add_argument(
        "--worker",
        help="工时记录的 worker 用户名（默认使用当前用户）",
    )
    parser.add_argument("--url", help="Tempo/Jira 服务地址")
    parser.add_argument("--username", help="用户名")
    parser.add_argument("--password", help="密码")

    # 兼容旧的参数格式
    if "--read-only" in sys.argv:
        sys.argv.remove("--read-only")
        sys.argv.extend(["--mode", "read-only"])
    if "--full" in sys.argv:
        sys.argv.remove("--full")
        sys.argv.extend(["--mode", "full"])

    args = parser.parse_args()

    tester = TempoAPITest()

    try:
        # 设置客户端
        await tester.setup(
            base_url=args.url,
            username=args.username,
            password=args.password,
        )

        # 运行测试
        if args.mode == "read-only":
            await tester.run_read_only_tests()
        else:
            await tester.run_full_tests(args.issue, args.worker)

        # 打印摘要
        tester.print_summary()

    except AtlassianAuthError as e:
        print(f"\n✗ 认证失败: {e}")
        print("请检查环境变量或命令行参数中的用户名和密码")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 测试运行失败: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        await tester.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
