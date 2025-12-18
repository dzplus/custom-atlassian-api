"""
Tempo Account 资源

API: /rest/tempo-accounts/1/account
"""

from typing import Optional
from atlassian.common.base import BaseResource
from atlassian.tempo.models.account import (
    Account,
    AccountCreate,
    AccountLink,
)


class AccountResource(BaseResource):
    """
    Tempo 账户资源

    API 端点:
    - GET /account - 获取所有账户
    - POST /account - 创建账户
    - GET /account/{accountId} - 获取账户
    - PUT /account/{accountId} - 更新账户
    - DELETE /account/{accountId} - 删除账户
    - GET /account/key/{accountKey} - 按 Key 获取账户
    - GET /account/project/{projectId} - 获取项目关联的账户
    """

    BASE_PATH = "/rest/tempo-accounts/1/account"
    LINK_PATH = "/rest/tempo-accounts/1/link"

    async def get_all(self, include_archived: bool = False) -> list[Account]:
        """
        获取所有账户

        Args:
            include_archived: 是否包含已归档账户

        Returns:
            list[Account]: 账户列表
        """
        params = {}
        if include_archived:
            params["includeArchived"] = "true"
        data = await self._client.get_json(self.BASE_PATH, params=params)
        return [Account.model_validate(item) for item in data]

    async def get_all_raw(self, include_archived: bool = False) -> list[dict]:
        """获取所有账户原始数据"""
        params = {}
        if include_archived:
            params["includeArchived"] = "true"
        return await self._client.get_json(self.BASE_PATH, params=params)

    async def get(self, account_id: int) -> Account:
        """
        获取账户

        Args:
            account_id: 账户 ID

        Returns:
            Account: 账户
        """
        data = await self._client.get_json(f"{self.BASE_PATH}/{account_id}")
        return Account.model_validate(data)

    async def get_raw(self, account_id: int) -> dict:
        """获取账户原始数据"""
        return await self._client.get_json(f"{self.BASE_PATH}/{account_id}")

    async def get_by_key(self, account_key: str) -> Account:
        """
        按 Key 获取账户

        Args:
            account_key: 账户 Key

        Returns:
            Account: 账户
        """
        data = await self._client.get_json(f"{self.BASE_PATH}/key/{account_key}")
        return Account.model_validate(data)

    async def create(
        self,
        key: str,
        name: str,
        status: str = "OPEN",
        lead_username: Optional[str] = None,
        category_type_id: Optional[int] = None,
        customer_id: Optional[int] = None,
        contact: Optional[str] = None,
        global_: bool = False,
    ) -> Account:
        """
        创建账户

        Args:
            key: 账户唯一 Key
            name: 账户名称
            status: 状态 (OPEN, CLOSED, ARCHIVED)
            lead_username: 负责人用户名
            category_type_id: 分类类型 ID
            customer_id: 客户 ID
            contact: 联系方式
            global_: 是否全局账户

        Returns:
            Account: 创建的账户
        """
        account = AccountCreate(
            key=key,
            name=name,
            status=status,
            lead_username=lead_username,
            category_type_id=category_type_id,
            customer_id=customer_id,
            contact=contact,
            global_=global_,
        )
        data = await self._client.post_json(
            self.BASE_PATH,
            data=account.to_api_dict(),
        )
        return Account.model_validate(data)

    async def update(
        self,
        account_id: int,
        name: Optional[str] = None,
        status: Optional[str] = None,
        lead_username: Optional[str] = None,
        contact: Optional[str] = None,
    ) -> Account:
        """
        更新账户

        Args:
            account_id: 账户 ID
            name: 账户名称
            status: 状态
            lead_username: 负责人用户名
            contact: 联系方式

        Returns:
            Account: 更新后的账户
        """
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if status is not None:
            update_data["status"] = status
        if lead_username is not None:
            update_data["leadUsername"] = lead_username
        if contact is not None:
            update_data["contact"] = contact

        data = await self._client.put_json(
            f"{self.BASE_PATH}/{account_id}",
            data=update_data,
        )
        return Account.model_validate(data)

    async def delete(self, account_id: int) -> bool:
        """
        删除账户

        Args:
            account_id: 账户 ID

        Returns:
            bool: 是否成功
        """
        await self._client.delete_json(f"{self.BASE_PATH}/{account_id}")
        return True

    async def get_by_project(self, project_id: int) -> list[Account]:
        """
        获取项目关联的账户

        Args:
            project_id: Jira 项目 ID

        Returns:
            list[Account]: 账户列表
        """
        data = await self._client.get_json(f"{self.BASE_PATH}/project/{project_id}")
        return [Account.model_validate(item) for item in data]

    # ========== 账户关联 ==========

    async def get_links(self, account_id: int) -> list[AccountLink]:
        """
        获取账户的项目关联

        Args:
            account_id: 账户 ID

        Returns:
            list[AccountLink]: 关联列表
        """
        data = await self._client.get_json(f"{self.BASE_PATH}/{account_id}/link")
        return [AccountLink.model_validate(item) for item in data]

    async def get_project_links(self, project_id: int) -> list[AccountLink]:
        """
        获取项目的账户关联

        Args:
            project_id: Jira 项目 ID

        Returns:
            list[AccountLink]: 关联列表
        """
        data = await self._client.get_json(f"{self.LINK_PATH}/project/{project_id}")
        return [AccountLink.model_validate(item) for item in data]
