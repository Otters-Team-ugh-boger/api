from typing import List

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from . import schema

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> schema.ResponseUser:
    _tmp = token
    return schema.ResponseUser(id=1, name="boger", password="ugh")


@app.post("/user/token")
def create_user_token(user: schema.RequestUser) -> str:
    _tmp = user
    return "__PLACEHOLDER_TOKEN"


# USER LOGOUT HANDLE


@app.get("/payments/methods")
def get_payment_methods(
        user: schema.ResponseUser = Depends(get_current_user),
) -> List[schema.ResponsePaymentMethod]:
    return [
        schema.ResponsePaymentMethod(
            id=1,
            user_id=user.id,
            type=schema.PaymentMethodType.ETH,
            private_key="PRIVATE_KEY_PLACEHOLDER",
        )
    ]


@app.post("/payments/methods")
def create_payment_method(
        payment_method: schema.RequestPaymentMethod, user: schema.ResponseUser = Depends(get_current_user)
) -> schema.ResponsePaymentMethod:
    return schema.ResponsePaymentMethod(
        id=1,
        user_id=user.id,
        type=schema.PaymentMethodType.ETH,
        private_key="PRIVATE_KEY_PLACEHOLDER",
    )


@app.get("/payments/methods/{payment_method_id}")
def get_payment_method(
        payment_method_id: int, user: schema.ResponseUser = Depends(get_current_user)
) -> schema.ResponsePaymentMethod:
    return schema.ResponsePaymentMethod(
        id=payment_method_id,
        user_id=user.id,
        type=schema.PaymentMethodType.ETH,
        private_key="PRIVATE_KEY_PLACEHOLDER",
    )


@app.delete("/payments/methods/{payment_method_id}")
def delete_payment_method(
        payment_method_id: int, user: schema.ResponseUser = Depends(get_current_user)
) -> None:
    _tmp = payment_method_id, user


@app.get("/payments/rules")
def get_payment_rules() -> List[schema.ResponsePaymentRule]:
    return [schema.ResponsePaymentRule(id=1, payment_method_id=1, foundation_id=1, amount=1)]


@app.post("/payments/rules")
def create_payment_rule(payment_rule: schema.RequestPaymentRule) -> schema.ResponsePaymentRule:
    return schema.ResponsePaymentRule(id=1, **payment_rule.dict())


@app.get("/payments/rules/{payment_rule_id}")
def get_payment_rule(payment_rule_id: int) -> schema.ResponsePaymentRule:
    return schema.ResponsePaymentRule(
        id=payment_rule_id, payment_method_id=1, foundation_id=1, amount=1
    )


@app.delete("/payments/rules/{payment_rule_id}")
def delete_payment_rule(payment_rule_id: int):
    _tmp = payment_rule_id
    pass
