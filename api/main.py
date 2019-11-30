from typing import List

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from api import schemas, models
from api.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> schemas.ResponseUser:
    _tmp = token
    return schemas.ResponseUser(id=1, name="boger", password="ugh")


@app.post("/user/token")
def create_user_token(user: schemas.RequestUser) -> str:
    _tmp = user
    return "__PLACEHOLDER_TOKEN"


# USER LOGOUT HANDLE


@app.get("/payments/methods")
def get_payment_methods(
        user: schemas.ResponseUser = Depends(get_current_user),
) -> List[schemas.ResponsePaymentMethod]:
    return [
        schemas.ResponsePaymentMethod(
            id=1,
            user_id=user.id,
            type=schemas.PaymentMethodType.ETH,
            private_key="PRIVATE_KEY_PLACEHOLDER",
        )
    ]


@app.post("/payments/methods")
def create_payment_method(
        payment_method: schemas.RequestPaymentMethod, user: schemas.ResponseUser = Depends(get_current_user)
) -> schemas.ResponsePaymentMethod:
    return schemas.ResponsePaymentMethod(
        id=1,
        user_id=user.id,
        type=schemas.PaymentMethodType.ETH,
        private_key="PRIVATE_KEY_PLACEHOLDER",
    )


@app.get("/payments/methods/{payment_method_id}")
def get_payment_method(
        payment_method_id: int, user: schemas.ResponseUser = Depends(get_current_user)
) -> schemas.ResponsePaymentMethod:
    return schemas.ResponsePaymentMethod(
        id=payment_method_id,
        user_id=user.id,
        type=schemas.PaymentMethodType.ETH,
        private_key="PRIVATE_KEY_PLACEHOLDER",
    )


@app.delete("/payments/methods/{payment_method_id}")
def delete_payment_method(
        payment_method_id: int, user: schemas.ResponseUser = Depends(get_current_user)
) -> None:
    _tmp = payment_method_id, user


@app.get("/payments/rules")
def get_payment_rules() -> List[schemas.ResponsePaymentRule]:
    return [schemas.ResponsePaymentRule(id=1, payment_method_id=1, foundation_id=1, amount=1)]


@app.post("/payments/rules")
def create_payment_rule(payment_rule: schemas.RequestPaymentRule) -> schemas.ResponsePaymentRule:
    return schemas.ResponsePaymentRule(id=1, **payment_rule.dict())


@app.get("/payments/rules/{payment_rule_id}")
def get_payment_rule(payment_rule_id: int) -> schemas.ResponsePaymentRule:
    return schemas.ResponsePaymentRule(
        id=payment_rule_id, payment_method_id=1, foundation_id=1, amount=1
    )


@app.delete("/payments/rules/{payment_rule_id}")
def delete_payment_rule(payment_rule_id: int):
    _tmp = payment_rule_id
    pass
