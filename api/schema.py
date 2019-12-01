import datetime as dt
from decimal import Decimal
from enum import Enum
from typing import Optional

import pydantic


class UserBase(pydantic.BaseModel):
    name: str


class RequestUser(UserBase):
    password: str


class ResponseUser(UserBase):
    id: int

    class Config:
        orm_mode = True


class ResponseUserCreate(UserBase):
    id: int
    token: str


class UserToken(pydantic.BaseModel):
    user_id: int
    token: str

    class Config:
        orm_mode = True


class PaymentMethodType(str, Enum):
    ETH = "ETH"


class PaymentMethodBase(pydantic.BaseModel):
    type: PaymentMethodType


class RequestPaymentMethod(PaymentMethodBase):
    private_key: str


class ResponsePaymentMethod(PaymentMethodBase):
    id: int
    address: str

    class Config:
        orm_mode = True


class RequestFoundation(pydantic.BaseModel):
    name: str
    description: str
    payment_address: str


class ResponseFoundation(RequestFoundation):
    id: int

    class Config:
        orm_mode = True


class RequestPaymentRule(pydantic.BaseModel):
    payment_method_id: int
    foundation_id: int
    amount: Decimal


class ResponsePaymentRule(RequestPaymentRule):
    id: int

    class Config:
        orm_mode = True


class ResponsePayment(pydantic.BaseModel):
    id: int
    payment_rule_id: int
    transaction_hash: Optional[str]
    created_at: dt.datetime

    class Config:
        orm_mode = True


class ResponseSuccess(pydantic.BaseModel):
    success: bool
