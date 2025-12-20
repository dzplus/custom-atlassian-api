"""
Tempo Team 数据模型
"""

from typing import Optional, Union
from pydantic import BaseModel, Field, field_validator


class TeamLead(BaseModel):
    """团队负责人"""
    key: str
    display_name: Optional[str] = Field(None, alias="displayName")

    class Config:
        populate_by_name = True


class Team(BaseModel):
    """Tempo 团队"""
    id: int
    name: str
    summary: Optional[str] = None
    lead: Optional[Union[str, TeamLead]] = None  # 可以是字符串或对象
    program: Optional[dict] = None

    @field_validator('lead', mode='before')
    @classmethod
    def validate_lead(cls, v):
        """验证 lead 字段，如果是字符串则转换为 TeamLead 对象"""
        if isinstance(v, str):
            return TeamLead(key=v)
        return v

    class Config:
        populate_by_name = True
        extra = "allow"  # 允许额外字段


class TeamMember(BaseModel):
    """团队成员"""
    id: int
    team_id: int = Field(alias="teamId")
    member_key: str = Field(alias="memberKey")
    display_name: Optional[str] = Field(None, alias="displayName")
    member_type: str = Field("USER", alias="type")  # USER, TEAM
    role_id: Optional[int] = Field(None, alias="roleId")
    active: bool = True

    # 时间范围
    date_from: Optional[str] = Field(None, alias="dateFrom")
    date_to: Optional[str] = Field(None, alias="dateTo")

    # 承诺百分比
    commitment_percent: Optional[int] = Field(None, alias="commitmentPercent")

    class Config:
        populate_by_name = True
