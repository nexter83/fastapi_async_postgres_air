from typing import List

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import LimitOffsetPage, add_pagination
from ..services.accounts import AccountServices
from ..schemas.accounts import (
    AccountSchemaBase,
    AccountResponse,
    CreateAccountSchema,
    UpdateAccountSchema,
    AccountOutSchema,
)
from ..services.auth import RoleChecker

router = APIRouter(prefix="/api/accounts", tags=["accounts"])

ok = "ok"
allow_create_resource = RoleChecker(["admin"])
allow_read_resource = RoleChecker(["admin", "user"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[AccountOutSchema],
    dependencies=[Depends(allow_read_resource)],
)
async def get_accounts(
    service: AccountServices = Depends(),
    order_column=None,
    is_desc: bool = False,
) -> dict:
    res = await service.get_accounts(order_column, is_desc)
    return res


@router.get(
    "/{account_id}",
    status_code=status.HTTP_200_OK,
    response_model=AccountOutSchema,
    dependencies=[Depends(allow_read_resource)],
)
async def get_account(account_id: int, service: AccountServices = Depends()) -> dict:
    res = await service.get_account(account_id)
    return res


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountOutSchema,
    dependencies=[Depends(allow_create_resource)],
)
async def create_account(
    account: CreateAccountSchema, service: AccountServices = Depends()
) -> dict:
    res = await service.create_account(account)
    return res


@router.put(
    "/{account_id}",
    response_model=AccountSchemaBase,
    dependencies=[Depends(allow_create_resource)],
)
async def update_account(
    account_id: int, account: UpdateAccountSchema, service: AccountServices = Depends()
) -> dict:
    res = await service.update_account(account_id, account)
    return res


@router.delete("/{account_id}", dependencies=[Depends(allow_create_resource)])
async def delete_account(
    account_id: int, service: AccountServices = Depends()
) -> Response:
    return await service.delete_account(account_id)

add_pagination(router)