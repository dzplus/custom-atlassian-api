"""
Field Models - 字段相关数据模型

包含字段元数据、配置、屏幕等模型
"""

from typing import Any, Optional
from pydantic import BaseModel, Field


class FieldMetadata(BaseModel):
    """
    字段元数据

    描述字段的基本信息和配置
    """
    id: Optional[str] = None
    key: Optional[str] = None
    name: Optional[str] = None
    custom: Optional[bool] = None
    orderable: Optional[bool] = None
    navigable: Optional[bool] = None
    searchable: Optional[bool] = None
    clause_names: Optional[list[str]] = Field(None, alias="clauseNames")
    schema_: Optional[dict] = Field(None, alias="schema")

    model_config = {"populate_by_name": True}


class AllowedValue(BaseModel):
    """
    字段允许值

    用于定义字段可选的值（如下拉框选项）
    """
    id: Optional[str] = None
    name: Optional[str] = None
    value: Optional[str] = None
    self_url: Optional[str] = Field(None, alias="self")

    model_config = {"populate_by_name": True}


class FieldConfiguration(BaseModel):
    """
    字段配置

    定义字段在特定上下文中的行为
    """
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = Field(None, alias="isDefault")

    model_config = {"populate_by_name": True}


class FieldConfigurationItem(BaseModel):
    """
    字段配置项

    字段在配置中的具体设置
    """
    id: Optional[str] = None
    description: Optional[str] = None
    is_hidden: Optional[bool] = Field(None, alias="isHidden")
    is_required: Optional[bool] = Field(None, alias="isRequired")
    renderer: Optional[str] = None

    model_config = {"populate_by_name": True}


class FieldConfigurationScheme(BaseModel):
    """
    字段配置方案

    将字段配置映射到Issue类型
    """
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None

    model_config = {"populate_by_name": True}


class Screen(BaseModel):
    """
    屏幕模型

    定义字段在UI中的显示
    """
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    scope: Optional[dict] = None

    model_config = {"populate_by_name": True}


class ScreenTab(BaseModel):
    """
    屏幕标签页

    屏幕中的字段分组标签
    """
    id: Optional[int] = None
    name: Optional[str] = None

    model_config = {"populate_by_name": True}


class ScreenableField(BaseModel):
    """
    可屏幕化的字段

    可以添加到屏幕的字段
    """
    id: Optional[str] = None
    name: Optional[str] = None

    model_config = {"populate_by_name": True}


class ScreenScheme(BaseModel):
    """
    屏幕方案

    将屏幕映射到操作（创建、编辑、查看）
    """
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    screens: Optional[dict[str, int]] = None

    model_config = {"populate_by_name": True}


class IssueTypeScreenScheme(BaseModel):
    """
    Issue类型屏幕方案

    将屏幕方案映射到Issue类型
    """
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None

    model_config = {"populate_by_name": True}


class CustomFieldOption(BaseModel):
    """
    自定义字段选项

    自定义字段的可选值
    """
    id: Optional[str] = None
    value: Optional[str] = None
    disabled: Optional[bool] = None
    self_url: Optional[str] = Field(None, alias="self")

    model_config = {"populate_by_name": True}


class CustomFieldContext(BaseModel):
    """
    自定义字段上下文

    定义自定义字段在不同项目中的行为
    """
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_global_context: Optional[bool] = Field(None, alias="isGlobalContext")
    is_any_issue_type: Optional[bool] = Field(None, alias="isAnyIssueType")

    model_config = {"populate_by_name": True}


class FieldCreateMetadata(BaseModel):
    """
    字段创建元数据

    用于创建Issue时的字段信息
    """
    required: Optional[bool] = None
    schema_: Optional[dict] = Field(None, alias="schema")
    name: Optional[str] = None
    key: Optional[str] = None
    auto_complete_url: Optional[str] = Field(None, alias="autoCompleteUrl")
    has_default_value: Optional[bool] = Field(None, alias="hasDefaultValue")
    operations: Optional[list[str]] = None
    allowed_values: Optional[list[AllowedValue]] = Field(None, alias="allowedValues")
    default_value: Optional[Any] = Field(None, alias="defaultValue")

    model_config = {"populate_by_name": True}


class FieldEditMetadata(BaseModel):
    """
    字段编辑元数据

    用于编辑Issue时的字段信息
    """
    required: Optional[bool] = None
    schema_: Optional[dict] = Field(None, alias="schema")
    name: Optional[str] = None
    key: Optional[str] = None
    auto_complete_url: Optional[str] = Field(None, alias="autoCompleteUrl")
    has_default_value: Optional[bool] = Field(None, alias="hasDefaultValue")
    operations: Optional[list[str]] = None
    allowed_values: Optional[list[AllowedValue]] = Field(None, alias="allowedValues")

    model_config = {"populate_by_name": True}
