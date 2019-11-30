import datetime as dt
from decimal import Decimal
from enum import Enum

import pydantic


class UserBase(pydantic.BaseModel):
    name: str


class RequestUser(UserBase):
    password: str


class ResponseUser(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserToken(pydantic.BaseModel):
    user_id: int
    token: str

    class Config:
        orm_mode = True


class PaymentMethodType(str, Enum):
    ETH = "ETH"


class RequestPaymentMethod(pydantic.BaseModel):
    private_key: str
    type: PaymentMethodType


class ResponsePaymentMethod(RequestPaymentMethod):
    id: int

    class Config:
        orm_mode = True


class RequestFoundation(pydantic.BaseModel):
    name: str
    description: str
    payment_address: str


class ResponseFoundation(RequestFoundation):
    id: int


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
    created_at: dt.datetime

    class Config:
        orm_mode = True