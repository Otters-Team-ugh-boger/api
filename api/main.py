from typing import List, Union

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from api import schemas, models, crud
from api.database import SessionLocal, engine
from api.security import verify_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> schemas.ResponseUser:
    return crud.get_user_by_token(db, token)


def authenticate_user(db, username: str, password: str):
    user = crud.get_user_by_name(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@app.post("/user/signup")
def create_user(user: schemas.RequestUser, db: Session = Depends(get_db)) -> schemas.ResponseUser:
    db_user = crud.create_user(db, user)
    return db_user


@app.post("/user/token")
def create_user_token(user: schemas.RequestUser, db: Session = Depends(get_db)) -> str:
    db_user = authenticate_user(db, user.name, user.password)
    if not db_user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = crud.create_user_token(db, db_user.id)
    return token


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
