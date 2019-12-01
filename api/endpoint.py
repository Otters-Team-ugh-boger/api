from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from api import crud, model, schema, payment
from api.database import get_db, engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()
security_scheme = APIKeyHeader(name="Authorization")


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(security_scheme)
) -> schema.ResponseUser:
    return crud.get_user_by_token(db, token)


@app.post("/user/create", response_model=schema.ResponseUserCreate)
def create_user(user: schema.RequestUser, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    user_token = crud.create_user_token(db, db_user.id)
    return {"id": db_user.id, "name": db_user.name, "token": user_token.token}


@app.post("/user/token", response_model=schema.UserToken)
def create_user_token(user: schema.RequestUser, db: Session = Depends(get_db)) -> str:
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
    db: Session = Depends(get_db), user: schema.ResponseUser = Depends(get_current_user)
) -> List[schema.ResponsePaymentMethod]:
    return crud.get_payment_methods(db, user.id)


@app.post("/payments/methods", response_model=schema.ResponsePaymentMethod)
def create_payment_method(
    payment_method: schema.RequestPaymentMethod,
    db: Session = Depends(get_db),
    user: schema.ResponseUser = Depends(get_current_user),
) -> schema.ResponsePaymentMethod:
    return crud.create_payment_method(db, user.id, payment_method)


@app.get(
    "/payments/methods/{payment_method_id}", response_model=schema.ResponsePaymentMethod
)
def get_payment_method(
    payment_method_id: int,
    db: Session = Depends(get_db),
    user: schema.ResponseUser = Depends(get_current_user),
) -> schema.ResponsePaymentMethod:
    return crud.get_payment_method(db, payment_method_id)


@app.delete("/payments/methods/{payment_method_id}")
def delete_payment_method(
    payment_method_id: int,
    db: Session = Depends(get_db),
    user: schema.ResponseUser = Depends(get_current_user),
):
    crud.delete_payment_method(db, payment_method_id)


@app.get("/payments/rules", response_model=List[schema.ResponsePaymentRule])
def get_payment_rules(
    db: Session = Depends(get_db), user: schema.ResponseUser = Depends(get_current_user)
) -> List[schema.ResponsePaymentRule]:
    return crud.get_payment_rules(db, user.id)


@app.post("/payments/rules", response_model=schema.ResponsePaymentRule)
def create_payment_rule(
    payment_rule: schema.RequestPaymentRule, db: Session = Depends(get_db)
) -> schema.ResponsePaymentRule:
    return crud.create_payment_rule(db, payment_rule)


@app.get("/payments/rules/{payment_rule_id}", response_model=schema.ResponsePaymentRule)
def get_payment_rule(
    payment_rule_id: int, db: Session = Depends(get_db)
) -> schema.ResponsePaymentRule:
    return crud.get_payment_rule(db, payment_rule_id)


@app.delete("/payments/rules/{payment_rule_id}")
def delete_payment_rule(payment_rule_id: int, db: Session = Depends(get_db)):
    crud.delete_payment_rule(db, payment_rule_id)


@app.post(
    "/payments/rules/{payment_rule_id}/trigger",
    response_model=schema.ResponsePaymentTrigger,
)
def trigger_payment_rule(
    payment_rule_id: int,
    db: Session = Depends(get_db),
    user: schema.ResponseUser = Depends(get_current_user),
):
    db_payment_rule = crud.get_payment_rule(db, payment_rule_id, user.id)
    db_payment_method = db_payment_rule.payment_method
    tx_hash = payment.send_eth_from_to_amount(
        client=payment.eth_client,
        from_privkey=db_payment_method.private_key,
        to_pubkey=db_payment_rule.foundation.payment_address,
        amount=db_payment_rule.amount,
    )
    db_payment = crud.create_payment(db, payment_rule_id)
    return {
        "tx_hash": tx_hash,
        "id": db_payment.id,
        "payment_rule_id": db_payment.payment_rule_id,
        "created_at": db_payment.created_at,
    }


@app.get("/payments/history", response_model=List[schema.ResponsePayment])
def get_payment_history(
    db: Session = Depends(get_db), user: schema.ResponseUser = Depends(get_current_user)
) -> List[schema.ResponsePayment]:
    return crud.get_payments(db, user.id)
