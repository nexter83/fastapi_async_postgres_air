from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Response
from sqlalchemy import desc
from ..database import get_async_session
from ..models.accounts import Account


class AccountServices:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def _get_account(self, account_id: int):
        result = await self.session.execute(
            select(Account).where(Account.account_id == account_id)
        )
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result

    async def get_accounts(
        self,
        page: int = None,
        page_size: int = None,
        order_column=None,
        is_desc: bool = False,
    ):
        result = await self.session.execute(
            select(Account)
            .offset(page)
            .limit(page_size)
            .order_by(desc(order_column) if is_desc else order_column)
        )
        return result.scalars().all()

    async def get_account(self, account_id: int):
        res = await self._get_account(account_id)
        return res.scalars().first()

    async def create_account(self, account):
        new_account = Account(**account.dict())
        self.session.add(new_account)
        await self.session.commit()
        return new_account

    async def update_account(self, account_id: int, account):
        upd_account = (
            update(Account)
            .where(Account.account_id == account_id)
            .values(**account.dict())
        )
        upd_account = upd_account.values(update_ts=datetime.utcnow())
        upd_account.execution_options(synchronize_session="fetch")

        await self.session.execute(upd_account)
        await self.session.commit()
        return await self.get_account(account_id)

    async def delete_account(self, account_id: int):
        upd_account = delete(Account).where(Account.account_id == account_id)
        upd_account.execution_options(synchronize_session="fetch")

        await self.session.execute(upd_account)
        await self.session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
