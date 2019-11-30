from typing import List, Optional

from sqlalchemy.orm import Session

from api import models, schema
from api.security import create_access_token, hash_password, verify_password


def get_user_by_name(db: Session, name: str) -> models.User:
    return db.query(models.User).filter(models.User.name == name).first()


def create_user(db: Session, user: schema.RequestUser) -> models.User:
    hashed_password = hash_password(user.password)
    user_rcd = models.User(name=user.name, hashed_password=hashed_password)
    db.add(user_rcd)
    db.commit()
    db.refresh(user_rcd)
    return user_rcd


def create_user_token(db: Session, user_id: int) -> models.UserToken:
    token = create_access_token()
    user_token_rcd = models.UserToken(user_id=user_id, token=token)
    db.add(user_token_rcd)
    db.commit()
    db.refresh(user_token_rcd)
    return user_token_rcd


def get_user_by_token(db: Session, token: str) -> models.User:
    user_token_rcd = (
        db.query(models.UserToken).filter(models.UserToken.token == token).first()
    )
    return user_token_rcd.user


def authenticate_user(db, name: str, password: str) -> Optional[models.User]:
    user_rcd = get_user_by_name(db, name)
    if not user_rcd:
        return None
    if not verify_password(password, user_rcd.hashed_password):
        return None
    return user_rcd


def get_payment_methods(db: Session, user_id: int) -> List[models.PaymentMethod]:
    return (
        db.query(models.PaymentMethod)
        .filter(models.PaymentMethod.user_id == user_id)
        .all()
    )


def create_payment_method(
    db: Session, user_id: int, payment_method: schema.RequestPaymentMethod
) -> models.PaymentMethod:
    payment_method_rcd = models.PaymentMethod(user_id=user_id, **payment_method.dict())
    db.add(payment_method_rcd)
    db.commit()
    db.refresh(payment_method_rcd)
    return payment_method_rcd


def get_payment_method(db: Session, payment_method_id: int) -> models.PaymentMethod:
    return (
        db.query(models.PaymentMethod)
        .filter(models.PaymentMethod.id == payment_method_id)
        .first()
    )


def delete_payment_method(db: Session, payment_method_id: int) -> bool:
    db.delete(get_payment_method(db, payment_method_id))
    db.commit()
    return True


def get_payment_rules(db: Session, user_id: int) -> List[models.PaymentRule]:
    return (
        db.query(models.PaymentRule)
        .join(models.PaymentRule.payment_method, models.PaymentMethod.user)
        .filter(models.User.id == user_id)
        .all()
    )


def create_payment_rule(
    db: Session, payment_rule: schema.RequestPaymentRule,
) -> models.PaymentRule:
    payment_rule_rcd = models.PaymentRule(**payment_rule.dict())
    db.add(payment_rule_rcd)
    db.commit()
    db.refresh(payment_rule_rcd)
    return payment_rule_rcd


def get_payment_rule(db: Session, payment_rule_id: int) -> models.PaymentRule:
    return (
        db.query(models.PaymentRule)
        .filter(models.PaymentRule.id == payment_rule_id)
        .first()
    )


def delete_payment_rule(db: Session, payment_rule_id: int) -> bool:
    x = get_payment_rule(db, payment_rule_id)
    db.delete(x)
    db.commit()
    return True


def create_payment(db: Session, payment_rule_id: int) -> models.Payment:
    payment_rcd = models.Payment(payment_rule_id=payment_rule_id)
    db.add(payment_rcd)
    db.commit()
    db.refresh(payment_rcd)
    return payment_rcd


def get_payments(db: Session, user_id: int) -> List[models.Payment]:
    return (
        db.query(models.Payment)
        .join(
            models.Payment.payment_rule,
            models.PaymentRule.payment_method,
            models.PaymentMethod.user,
        )
        .filter(models.User.id == user_id)
        .all()
    )
