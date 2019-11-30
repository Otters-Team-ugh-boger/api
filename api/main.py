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


class PaymentRule(pydantic.BaseModel):
    payment_method_id: int
    foundation_id: int
    amount: Decimal


class DbPaymentRule(PaymentRule):
    id: int


@app.get("/payment_rules")
def get_payment_rules() -> List[DbPaymentRule]:
    return [DbPaymentRule(id=1, payment_method_id=1, foundation_id=1, amount=1)]


@app.post("/payment_rules")
def create_payment_rule(payment_rule: PaymentRule) -> DbPaymentRule:
    return DbPaymentRule(id=1, **payment_rule.dict())


@app.get("/payment_rules/{payment_rule_id}")
def get_payment_rule(payment_rule_id: int) -> DbPaymentRule:
    return DbPaymentRule(
        id=payment_rule_id, payment_method_id=1, foundation_id=1, amount=1
    )


@app.delete("/payment_rules/{payment_rule_id}")
def delete_payment_rule(payment_rule_id: int):
    _tmp = payment_rule_id
    pass


@app.post("/user/login")
def read_item(user: User):
    return DbUser(id=1, name="boger", password="ugh")
