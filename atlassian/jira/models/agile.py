"""
Agile Models - Jira Agile/Scrum 相关数据模型

用于 /rest/agile/1.0/* API
"""

from typing import Optional, Any
from pydantic import BaseModel, Field


# ==================== Board 相关模型 ====================


class BoardLocation(BaseModel):
    """Board 位置信息"""
    project_id: Optional[int] = Field(None, alias="projectId")
    display_name: Optional[str] = Field(None, alias="displayName")
    project_name: Optional[str] = Field(None, alias="projectName")
    project_key: Optional[str] = Field(None, alias="projectKey")
    project_type_key: Optional[str] = Field(None, alias="projectTypeKey")
    avatar_uri: Optional[str] = Field(None, alias="avatarURI")
    name: Optional[str] = None

    model_config = {"populate_by_name": True}


class Board(BaseModel):
    """敏捷看板"""
    id: Optional[int] = None
    self_url: Optional[str] = Field(None, alias="self")
    name: Optional[str] = None
    type: Optional[str] = None  # scrum, kanban
    location: Optional[BoardLocation] = None

    model_config = {"populate_by_name": True}


class BoardList(BaseModel):
    """看板列表（分页）"""
    max_results: Optional[int] = Field(None, alias="maxResults")
    start_at: Optional[int] = Field(None, alias="startAt")
    total: Optional[int] = None
    is_last: Optional[bool] = Field(None, alias="isLast")
    values: Optional[list[Board]] = None

    model_config = {"populate_by_name": True}


class ColumnConfig(BaseModel):
    """列配置"""
    name: Optional[str] = None
    statuses: Optional[list[dict]] = None
    min: Optional[int] = None
    max: Optional[int] = None

    model_config = {"populate_by_name": True}


class EstimationConfig(BaseModel):
    """估算配置"""
    type: Optional[str] = None
    field: Optional[dict] = None

    model_config = {"populate_by_name": True}


class RankingConfig(BaseModel):
    """排名配置"""
    rank_custom_field_id: Optional[int] = Field(None, alias="rankCustomFieldId")

    model_config = {"populate_by_name": True}


class BoardConfiguration(BaseModel):
    """看板配置"""
    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    location: Optional[BoardLocation] = None
    filter: Optional[dict] = None
    sub_query: Optional[dict] = Field(None, alias="subQuery")
    column_config: Optional[dict] = Field(None, alias="columnConfig")
    estimation: Optional[EstimationConfig] = None
    ranking: Optional[RankingConfig] = None

    model_config = {"populate_by_name": True}


# ==================== Sprint 相关模型 ====================


class Sprint(BaseModel):
    """Sprint（冲刺）"""
    id: Optional[int] = None
    self_url: Optional[str] = Field(None, alias="self")
    state: Optional[str] = None  # future, active, closed
    name: Optional[str] = None
    start_date: Optional[str] = Field(None, alias="startDate")
    end_date: Optional[str] = Field(None, alias="endDate")
    complete_date: Optional[str] = Field(None, alias="completeDate")
    origin_board_id: Optional[int] = Field(None, alias="originBoardId")
    goal: Optional[str] = None

    model_config = {"populate_by_name": True}


class SprintList(BaseModel):
    """Sprint 列表（分页）"""
    max_results: Optional[int] = Field(None, alias="maxResults")
    start_at: Optional[int] = Field(None, alias="startAt")
    total: Optional[int] = None
    is_last: Optional[bool] = Field(None, alias="isLast")
    values: Optional[list[Sprint]] = None

    model_config = {"populate_by_name": True}


class CreateSprintRequest(BaseModel):
    """创建 Sprint 请求"""
    name: str
    origin_board_id: int = Field(alias="originBoardId")
    start_date: Optional[str] = Field(None, alias="startDate")
    end_date: Optional[str] = Field(None, alias="endDate")
    goal: Optional[str] = None

    model_config = {"populate_by_name": True}


class UpdateSprintRequest(BaseModel):
    """更新 Sprint 请求"""
    name: Optional[str] = None
    state: Optional[str] = None  # future, active, closed
    start_date: Optional[str] = Field(None, alias="startDate")
    end_date: Optional[str] = Field(None, alias="endDate")
    complete_date: Optional[str] = Field(None, alias="completeDate")
    goal: Optional[str] = None

    model_config = {"populate_by_name": True}


# ==================== Epic 相关模型 ====================


class Epic(BaseModel):
    """Epic"""
    id: Optional[int] = None
    key: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    name: Optional[str] = None
    summary: Optional[str] = None
    color: Optional[dict] = None
    done: Optional[bool] = None

    model_config = {"populate_by_name": True}


class EpicList(BaseModel):
    """Epic 列表（分页）"""
    max_results: Optional[int] = Field(None, alias="maxResults")
    start_at: Optional[int] = Field(None, alias="startAt")
    total: Optional[int] = None
    is_last: Optional[bool] = Field(None, alias="isLast")
    values: Optional[list[Epic]] = None

    model_config = {"populate_by_name": True}


class UpdateEpicRequest(BaseModel):
    """更新 Epic 请求"""
    name: Optional[str] = None
    summary: Optional[str] = None
    color: Optional[dict] = None  # {"key": "color_1"} to {"key": "color_9"}
    done: Optional[bool] = None

    model_config = {"populate_by_name": True}


class RankEpicRequest(BaseModel):
    """Epic 排序请求"""
    rank_before_epic: Optional[str] = Field(None, alias="rankBeforeEpic")
    rank_after_epic: Optional[str] = Field(None, alias="rankAfterEpic")
    rank_custom_field_id: Optional[int] = Field(None, alias="rankCustomFieldId")

    model_config = {"populate_by_name": True}


# ==================== Issue 相关模型 (Agile) ====================


class AgileIssue(BaseModel):
    """Agile Issue（包含敏捷字段）"""
    id: Optional[str] = None
    key: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")
    expand: Optional[str] = None
    fields: Optional[dict] = None

    model_config = {"populate_by_name": True}


class AgileIssueList(BaseModel):
    """Agile Issue 列表（分页）"""
    max_results: Optional[int] = Field(None, alias="maxResults")
    start_at: Optional[int] = Field(None, alias="startAt")
    total: Optional[int] = None
    issues: Optional[list[AgileIssue]] = None

    model_config = {"populate_by_name": True}


class IssueEstimation(BaseModel):
    """Issue 估算"""
    field_id: Optional[str] = Field(None, alias="fieldId")
    value: Optional[Any] = None

    model_config = {"populate_by_name": True}


class RankIssuesRequest(BaseModel):
    """Issue 排序请求"""
    issues: list[str]
    rank_before_issue: Optional[str] = Field(None, alias="rankBeforeIssue")
    rank_after_issue: Optional[str] = Field(None, alias="rankAfterIssue")
    rank_custom_field_id: Optional[int] = Field(None, alias="rankCustomFieldId")

    model_config = {"populate_by_name": True}


class MoveIssuesToSprintRequest(BaseModel):
    """移动 Issue 到 Sprint 请求"""
    issues: list[str]
    rank_before_issue: Optional[str] = Field(None, alias="rankBeforeIssue")
    rank_after_issue: Optional[str] = Field(None, alias="rankAfterIssue")
    rank_custom_field_id: Optional[int] = Field(None, alias="rankCustomFieldId")

    model_config = {"populate_by_name": True}


class MoveIssuesToBacklogRequest(BaseModel):
    """移动 Issue 到 Backlog 请求"""
    issues: list[str]

    model_config = {"populate_by_name": True}


class MoveIssuesToEpicRequest(BaseModel):
    """移动 Issue 到 Epic 请求"""
    issues: list[str]

    model_config = {"populate_by_name": True}


# ==================== 属性相关模型 ====================


class EntityPropertyKey(BaseModel):
    """实体属性键"""
    self_url: Optional[str] = Field(None, alias="self")
    key: Optional[str] = None

    model_config = {"populate_by_name": True}


class EntityPropertyKeys(BaseModel):
    """实体属性键列表"""
    keys: Optional[list[EntityPropertyKey]] = None

    model_config = {"populate_by_name": True}


class EntityProperty(BaseModel):
    """实体属性"""
    key: Optional[str] = None
    value: Optional[Any] = None

    model_config = {"populate_by_name": True}


# ==================== 快速过滤器模型 ====================


class QuickFilter(BaseModel):
    """快速过滤器"""
    id: Optional[int] = None
    name: Optional[str] = None
    jql: Optional[str] = None
    description: Optional[str] = None
    position: Optional[int] = None
    board_id: Optional[int] = Field(None, alias="boardId")

    model_config = {"populate_by_name": True}


class QuickFilterList(BaseModel):
    """快速过滤器列表"""
    max_results: Optional[int] = Field(None, alias="maxResults")
    start_at: Optional[int] = Field(None, alias="startAt")
    total: Optional[int] = None
    is_last: Optional[bool] = Field(None, alias="isLast")
    values: Optional[list[QuickFilter]] = None

    model_config = {"populate_by_name": True}
