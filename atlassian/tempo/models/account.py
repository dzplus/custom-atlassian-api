"""
Tempo Account 数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field


class AccountLead(BaseModel):
    """账户负责人"""
    key: str
    display_name: Optional[str] = Field(None, alias="displayName")

    class Config:
        populate_by_name = True


class AccountCustomer(BaseModel):
    """账户客户"""
    id: int
    key: str
    name: str


class Account(BaseModel):
    """Tempo 账户"""
    id: int
    key: str
    name: str
    status: str  # OPEN, CLOSED, ARCHIVED
    global_: bool = Field(alias="global")
    category_type: Optional[str] = Field(None, alias="categoryType")
    category_type_id: Optional[int] = Field(None, alias="categoryTypeId")
    lead: Optional[AccountLead] = None
    customer: Optional[AccountCustomer] = None
    contact: Optional[str] = None

    class Config:
        populate_by_name = True


class AccountCreate(BaseModel):
    """创建账户参数"""
    key: str
    name: str
    status: str = "OPEN"  # OPEN, CLOSED, ARCHIVED
    lead_username: Optional[str] = Field(None, alias="leadUsername")
    category_type_id: Optional[int] = Field(None, alias="categoryTypeId")
    customer_id: Optional[int] = Field(None, alias="customerId")
    contact: Optional[str] = None
    global_: bool = Field(False, alias="global")

    class Config:
        populate_by_name = True

    def to_api_dict(self) -> dict:
        """转换为 API 请求格式"""
        data = {
            "key": self.key,
            "name": self.name,
            "status": self.status,
            "global": self.global_,
        }
        if self.lead_username:
            data["leadUsername"] = self.lead_username
        if self.category_type_id:
            data["categoryTypeId"] = self.category_type_id
        if self.customer_id:
            data["customerId"] = self.customer_id
        if self.contact:
            data["contact"] = self.contact
        return data


class AccountLink(BaseModel):
    """账户与项目的关联"""
    id: int
    scope_type: str = Field(alias="scopeType")  # PROJECT
    scope: str  # project key
    account_id: int = Field(alias="accountId")
    account_key: Optional[str] = Field(None, alias="accountKey")
    default_: bool = Field(False, alias="default")

    class Config:
        populate_by_name = True
