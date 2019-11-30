import datetime
from decimal import Decimal
from enum import Enum
from typing import List

import pydantic


class UserBase(pydantic.BaseModel):
    name: str


class RequestUser(UserBase):
    password: str


class ResponseUser(RequestUser):
    id: int


class User(UserBase):
    id: int
    hashed_password: str

    payment_methods: List['PaymentMethod'] = []
    tokens: List['UserToken'] = []

    class Config:
        orm_mode = True


class UserTokenBase(pydantic.BaseModel):
    user_id: int
    token: str


class UserToken(UserTokenBase):
    id: int
    created_at: datetime.datetime

    user: 'User'

    class Config:
        orm_mode = True


class PaymentMethodType(str, Enum):
    ETH = "ETH"


class PaymentMethodBase(pydantic.BaseModel):
    private_key: str
    type: PaymentMethodType


class RequestPaymentMethod(PaymentMethodBase):
    pass


class ResponsePaymentMethod(PaymentMethodBase):
    id: int


class PaymentMethod(PaymentMethodBase):
    id: int
    user_id: int

    user: 'User'

    class Config:
        orm_mode = True


class FoundationBase(pydantic.BaseModel):
    name: str
    description: str
    payment_address: str


class Foundation(FoundationBase):
    id: int

    payment_rules: List['PaymentRule'] = []

    class Config:
        orm_mode = True


class RequestFoundation(pydantic.BaseModel):
    name: str
    description: str
    public_key: str


class ResponseFoundation(RequestFoundation):
    id: int


class PaymentRuleBase(pydantic.BaseModel):
    payment_method_id: int
    foundation_id: int
    amount: Decimal


class RequestPaymentRule(PaymentRuleBase):
    pass


class ResponsePaymentRule(RequestPaymentRule):
    id: int


class PaymentRule(PaymentRuleBase):
    payment_method: PaymentMethod
    foundation: Foundation
    payment_history: List['PaymentHistory']

    class Config:
        orm_mode = True


class PaymentHistoryBase(pydantic.BaseModel):
    pass


class PaymentHistory(PaymentHistoryBase):
    id: int
    payment_rule_id: int
    created_at: datetime.datetime

    payment_rule: PaymentRule

    class Config:
        orm_mode = True
