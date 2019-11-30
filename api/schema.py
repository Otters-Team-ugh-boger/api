from decimal import Decimal
from enum import Enum

import pydantic


class RequestUser(pydantic.BaseModel):
    name: str
    password: str


class ResponseUser(RequestUser):
    id: int


class PaymentMethodType(str, Enum):
    ETH = "ETH"


class RequestPaymentMethod(pydantic.BaseModel):
    user_id: int
    type: PaymentMethodType
    private_key: str


class ResponsePaymentMethod(RequestPaymentMethod):
    id: int


class RequestFoundation(pydantic.BaseModel):
    name: str
    description: str
    public_key: str


class ResponseFoundation(RequestFoundation):
    id: int


class RequestPaymentRule(pydantic.BaseModel):
    payment_method_id: int
    foundation_id: int
    amount: Decimal


class ResponsePaymentRule(RequestPaymentRule):
    id: int
