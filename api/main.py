from decimal import Decimal
from enum import Enum
from typing import List

from fastapi import FastAPI
import pydantic

app = FastAPI()


class User(pydantic.BaseModel):
    name: str
    password: str


class DbUser(User):
    id: int


class PaymentMethodType(str, Enum):
    ETH = "ETH"


class PaymentMethod(pydantic.BaseModel):
    user_id: int
    type: PaymentMethodType
    private_key: str


class DbPaymentMethod(PaymentMethod):
    id: int


class Foundation(pydantic.BaseModel):
    name: str
    description: str
    public_key: str


class DbFoundation(Foundation):
    id: int


class Payment(pydantic.BaseModel):
    payment_method_id: int
    foundation_id: int
    amount: Decimal


class DbPayment(Payment):
    id: int


@app.post("/user/login")
def read_item(user: User):
    return DbUser(id=1, name="boger", password="ugh")
