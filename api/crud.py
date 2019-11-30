from typing import List

from sqlalchemy.orm import Session

from api import models, schema
from api.security import hash_password, create_access_token


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.name == username).first()


def create_user(db: Session, user: schema.RequestUser):
    hashed_password = hash_password(user.password)
    db_user = models.User(name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_token(db: Session, token: str):
    db_token = db.query(models.UserToken).filter(models.UserToken.token == token).first()
    return db_token.user


def create_user_token(db: Session, user_id: int):
    token = create_access_token()
    db_token = models.UserToken(user_id=user_id, token=token)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_payment_methods(db: Session, user_id: int) -> List[models.PaymentMethod]:
    return db.query(models.PaymentMethod).filter(models.User.id == user_id).all()


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
    return True


def get_payment_rules(db: Session, user_id: int) -> List[models.PaymentRule]:
    return (
        db.query(models.PaymentRule)
            .filter(models.PaymentRule.payment_method.user_id == user_id)
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
    db.delete(get_payment_rule(db, payment_rule_id))
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
            .filter(models.Payment.payment_rule.payment_method.user_id == user_id)
            .all()
    )
