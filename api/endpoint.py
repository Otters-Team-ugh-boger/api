from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from api import crud, model, schema, payment
from api.database import get_db, engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()
security_scheme = APIKeyHeader(name="Authorization")


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(security_scheme)
) -> model.User:
    user = crud.get_user_by_token(db, token)
    if user is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/user/create", response_model=schema.ResponseUserCreate)
def create_user(user: schema.RequestUser, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    if not db_user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with a given username already exists",
        )
    user_token = crud.create_user_token(db, db_user.id)
    return {"id": db_user.id, "name": db_user.name, "token": user_token.token}


@app.post("/user/token", response_model=schema.UserToken)
def create_user_token(
    user: schema.RequestUser, db: Session = Depends(get_db)
) -> model.UserToken:
    user_rcd = crud.authenticate_user(db, user.name, user.password)
    if user_rcd is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return crud.create_user_token(db, user_rcd.id)


# USER LOGOUT HANDLE


@app.get("/payments/methods", response_model=List[schema.ResponsePaymentMethod])
def get_payment_methods(
    db: Session = Depends(get_db), user: model.User = Depends(get_current_user)
) -> List[dict]:
    return [{
        'id': payment_method.id,
        'type': payment_method.type,
        'address': payment.account_from_private_key(payment.eth_client, payment_method.private_key).address
    } for payment_method in crud.get_payment_methods(db, user.id)]


@app.post("/payments/methods", response_model=schema.ResponsePaymentMethod)
def create_payment_method(
    payment_method: schema.RequestPaymentMethod,
    db: Session = Depends(get_db),
    user: model.User = Depends(get_current_user),
) -> model.PaymentMethod:
    return crud.create_payment_method(db, user.id, payment_method)


@app.get(
    "/payments/methods/{payment_method_id}", response_model=schema.ResponsePaymentMethod
)
def get_payment_method(
    payment_method_id: int,
    db: Session = Depends(get_db),
    user: model.User = Depends(get_current_user),
) -> model.PaymentMethod:
    db_payment_method = crud.get_payment_method(db, payment_method_id, user.id)
    if not db_payment_method:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Payment method not found"
        )
    return db_payment_method


@app.delete("/payments/methods/{payment_method_id}", response_model=schema.ResponseSuccess)
def delete_payment_method(
    payment_method_id: int,
    db: Session = Depends(get_db),
    user: model.User = Depends(get_current_user),
):
    success = crud.delete_payment_method(db, payment_method_id, user.id)
    if not success:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Payment method not found"
        )
    return {
        'success': success
    }


@app.get("/payments/rules", response_model=List[schema.ResponsePaymentRule])
def get_payment_rules(
    db: Session = Depends(get_db), user: model.User = Depends(get_current_user)
) -> List[model.PaymentRule]:
    return crud.get_payment_rules(db, user.id)


@app.post("/payments/rules", response_model=schema.ResponsePaymentRule)
def create_payment_rule(
    payment_rule: schema.RequestPaymentRule, db: Session = Depends(get_db), user: model.User = Depends(get_current_user)
) -> model.PaymentRule:
    return crud.create_payment_rule(db, payment_rule, user.id)


@app.get("/payments/rules/{payment_rule_id}", response_model=schema.ResponsePaymentRule)
def get_payment_rule(
    payment_rule_id: int, db: Session = Depends(get_db), user: model.User = Depends(get_current_user)
) -> model.PaymentRule:
    payment_rule = crud.get_payment_rule(db, payment_rule_id, user.id)
    if not payment_rule:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Payment rule not found',
        )
    return payment_rule


@app.delete("/payments/rules/{payment_rule_id}", response_model=schema.ResponseSuccess)
def delete_payment_rule(payment_rule_id: int, db: Session = Depends(get_db)):
    success = crud.delete_payment_rule(db, payment_rule_id)
    if not success:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Payment method not found"
        )
    return {
        'success': success
    }


@app.post(
    "/payments/rules/{payment_rule_id}/trigger", response_model=schema.ResponsePayment
)
def trigger_payment_rule(
    payment_rule_id: int,
    db: Session = Depends(get_db),
    user: model.User = Depends(get_current_user),
):
    payment_rule_rcd = crud.get_payment_rule(db, payment_rule_id, user.id)
    transaction_hash = payment.send_eth_from_to_amount(
        client=payment.eth_client,
        from_private_key=payment_rule_rcd.payment_method.private_key,
        to_pubkey=payment_rule_rcd.foundation.payment_address,
        amount=payment_rule_rcd.amount,
    )
    return crud.create_payment(db, payment_rule_id, transaction_hash)


@app.get("/payments/history", response_model=List[schema.ResponsePayment])
def get_payment_history(
    db: Session = Depends(get_db), user: model.User = Depends(get_current_user)
) -> List[model.Payment]:
    return crud.get_payments(db, user.id)


@app.get("/foundations", response_model=List[schema.ResponseFoundation])
def get_foundations(db: Session = Depends(get_db)) -> List[model.Foundation]:
    return crud.get_foundations(db)


@app.post("/foundations", response_model=schema.ResponseFoundation)
def create_foundation(
    foundation: schema.RequestFoundation, db: Session = Depends(get_db)
) -> model.Foundation:
    return crud.create_foundation(db, foundation)
