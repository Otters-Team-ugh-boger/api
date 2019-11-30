from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import  APIKeyHeader
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from api import crud, models, schema
from api.database import SessionLocal, engine
from api.security import verify_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
security_scheme = APIKeyHeader(tokenUrl="/user/token")


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()


async def get_current_user(
        token: str = Depends(security_scheme), db: Session = Depends(get_db)
) -> schema.ResponseUser:
    return crud.get_user_by_token(db, token)


def authenticate_user(db, username: str, password: str) -> Optional[models.User]:
    user = crud.get_user_by_name(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


@app.post("/user/signup")
def create_user(
        user: schema.RequestUser, db: Session = Depends(get_db)
) -> schema.ResponseUser:
    db_user = crud.create_user(db, user)
    return db_user


@app.post("/user/token")
def create_user_token(user: schema.RequestUser, db: Session = Depends(get_db)) -> str:
    db_user = authenticate_user(db, user.name, user.password)
    if db_user is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = crud.create_user_token(db, db_user.id)
    return token


@app.post("/user/token")
def create_user_token(user: schema.RequestUser) -> str:
    _tmp = user
    return "__PLACEHOLDER_TOKEN"


# USER LOGOUT HANDLE


@app.get("/payments/methods")
def get_payment_methods(
        db: Session = Depends(get_db),
        user: schema.ResponseUser = Depends(get_current_user),
) -> List[schema.ResponsePaymentMethod]:
    return crud.get_payment_methods(db, user.id)


@app.post("/payments/methods")
def create_payment_method(
        payment_method: schema.RequestPaymentMethod,
        db: Session = Depends(get_db),
        user: schema.ResponseUser = Depends(get_current_user),
) -> schema.ResponsePaymentMethod:
    return schema.ResponsePaymentMethod.from_orm(
        crud.create_payment_method(db, user.id, payment_method)
    )


@app.get("/payments/methods/{payment_method_id}")
def get_payment_method(
        payment_method_id: int,
        db: Session = Depends(get_db),
        user: schema.ResponseUser = Depends(get_current_user),
) -> schema.ResponsePaymentMethod:
    return schema.ResponsePaymentMethod.from_orm(
        crud.get_payment_method(db, payment_method_id)
    )


@app.delete("/payments/methods/{payment_method_id}")
def delete_payment_method(
        payment_method_id: int,
        db: Session = Depends(get_db),
        user: schema.ResponseUser = Depends(get_current_user),
) -> None:
    crud.delete_payment_method(db, payment_method_id)


@app.get("/payments/rules")
def get_payment_rules(
        db: Session = Depends(get_db), user: schema.ResponseUser = Depends(get_current_user)
) -> List[schema.ResponsePaymentRule]:
    return crud.get_payment_rules(db, user.id)


@app.post("/payments/rules")
def create_payment_rule(
        payment_rule: schema.RequestPaymentRule, db: Session = Depends(get_db)
) -> schema.ResponsePaymentRule:
    return crud.create_payment_rule(db, payment_rule)


@app.get("/payments/rules/{payment_rule_id}")
def get_payment_rule(
        payment_rule_id: int, db: Session = Depends(get_db)
) -> schema.ResponsePaymentRule:
    return crud.get_payment_rule(db, payment_rule_id)


@app.delete("/payments/rules/{payment_rule_id}")
def delete_payment_rule(payment_rule_id: int, db: Session = Depends(get_db)):
    crud.delete_payment_rule(db, payment_rule_id)


@app.post("/payments/rules/{payment_rule_id}/trigger")
def trigger_payment_rule(
        payment_rule_id: int, db: Session = Depends(get_db)
) -> schema.ResponsePaymentRule:
    return crud.create_payment(db, payment_rule_id)


@app.get("/payments/history")
def get_payment_history(
        db: Session = Depends(get_db),
        user: schema.ResponseUser = Depends(get_current_user),
) -> List[schema.ResponsePayment]:
    return crud.get_payments(db, user.id)
