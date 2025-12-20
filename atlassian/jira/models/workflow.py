"""
Workflow Models - 工作流相关数据模型

包含工作流、工作流方案、转换等模型
"""

from typing import Any, Optional
from pydantic import BaseModel, Field


class Transition(BaseModel):
    """
    工作流转换

    表示从一个状态到另一个状态的转换
    """
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    from_status: Optional[list[str]] = Field(None, alias="from")
    to_status: Optional[str] = Field(None, alias="to")
    type: Optional[str] = None
    screen: Optional[dict] = None
    rules: Optional[dict] = None

    model_config = {"populate_by_name": True}


class Workflow(BaseModel):
    """
    工作流模型
    """
    name: Optional[str] = None
    description: Optional[str] = None
    last_modified_date: Optional[str] = Field(None, alias="lastModifiedDate")
    last_modified_user: Optional[str] = Field(None, alias="lastModifiedUser")
    steps: Optional[int] = None
    is_default: Optional[bool] = Field(None, alias="isDefault")

    model_config = {"populate_by_name": True}


class WorkflowScheme(BaseModel):
    """
    工作流方案模型

    将工作流映射到Issue类型
    """
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    default_workflow: Optional[str] = Field(None, alias="defaultWorkflow")
    issue_type_mappings: Optional[dict[str, str]] = Field(None, alias="issueTypeMappings")
    draft: Optional[bool] = None
    self_url: Optional[str] = Field(None, alias="self")
    update_draft_if_needed: Optional[bool] = Field(None, alias="updateDraftIfNeeded")

    model_config = {"populate_by_name": True}


class WorkflowSchemeAssociations(BaseModel):
    """
    工作流方案关联

    显示哪些项目使用了该工作流方案
    """
    project_ids: list[str] = Field(alias="projectIds")

    model_config = {"populate_by_name": True}


class WorkflowMapping(BaseModel):
    """
    工作流映射

    Issue类型到工作流的映射
    """
    workflow: Optional[str] = None
    issue_type: Optional[str] = Field(None, alias="issueType")
    update_draft_if_needed: Optional[bool] = Field(None, alias="updateDraftIfNeeded")

    model_config = {"populate_by_name": True}


class WorkflowStatus(BaseModel):
    """
    工作流状态详情

    扩展的状态信息，包含工作流上下文
    """
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = Field(None, alias="iconUrl")
    status_category: Optional[dict] = Field(None, alias="statusCategory")

    model_config = {"populate_by_name": True}


class TransitionScreenDetails(BaseModel):
    """
    转换屏幕详情
    """
    id: Optional[str] = None
    name: Optional[str] = None

    model_config = {"populate_by_name": True}


class TransitionRule(BaseModel):
    """
    转换规则
    """
    type: Optional[str] = None
    configuration: Optional[dict] = None

    model_config = {"populate_by_name": True}


class IssueTypeMapping(BaseModel):
    """
    Issue类型映射

    用于工作流方案中的Issue类型到工作流的映射
    """
    issue_type: Optional[str] = Field(None, alias="issueType")
    workflow: Optional[str] = None
    update_draft_if_needed: Optional[bool] = Field(None, alias="updateDraftIfNeeded")

    model_config = {"populate_by_name": True}


class DefaultWorkflow(BaseModel):
    """
    默认工作流设置
    """
    workflow: str
    update_draft_if_needed: Optional[bool] = Field(None, alias="updateDraftIfNeeded")

    model_config = {"populate_by_name": True}


class WorkflowSchemeDraft(BaseModel):
    """
    工作流方案草稿

    用于修改工作流方案前的草稿版本
    """
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    default_workflow: Optional[str] = Field(None, alias="defaultWorkflow")
    issue_type_mappings: Optional[dict[str, str]] = Field(None, alias="issueTypeMappings")
    original_default_workflow: Optional[str] = Field(None, alias="originalDefaultWorkflow")
    original_issue_type_mappings: Optional[dict[str, str]] = Field(None, alias="originalIssueTypeMappings")
    draft: bool = True
    last_modified_user: Optional[dict] = Field(None, alias="lastModifiedUser")
    last_modified: Optional[str] = Field(None, alias="lastModified")
    self_url: Optional[str] = Field(None, alias="self")

    model_config = {"populate_by_name": True}
