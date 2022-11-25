from pydantic import BaseModel
from datetime import datetime


class AccountSchemaBase(BaseModel):
    login: str
    first_name: str
    last_name: str
    update_ts: datetime | None = None
    frequent_flyer_id: int | None = None

    class Config:
        orm_mode = True


class AccountOutSchema(AccountSchemaBase):
    account_id: int


class ListAccountSchema(BaseModel):
    status: str
    total: int
    page: int = 0
    page_size: int = None
    count: int
    accounts: list[AccountOutSchema] = []


class CreateAccountSchema(AccountSchemaBase):
    pass


class UpdateAccountSchema(AccountSchemaBase):
    pass


class AccountResponse(BaseModel):
    status: str
    account: AccountOutSchema

    class Congig:
        orm_mode = True


