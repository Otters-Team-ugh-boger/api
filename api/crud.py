from typing import List, Optional

from sqlalchemy.orm import Session

from api import model, schema
from api.security import create_access_token, hash_password, verify_password


def get_user_by_name(db: Session, name: str) -> model.User:
    return db.query(model.User).filter(model.User.name == name).first()


def create_user(db: Session, user: schema.RequestUser) -> model.User:
    hashed_password = hash_password(user.password)
    user_rcd = model.User(name=user.name, hashed_password=hashed_password)
    db.add(user_rcd)
    db.commit()
    db.refresh(user_rcd)
    return user_rcd


def create_user_token(db: Session, user_id: int) -> model.UserToken:
    token = create_access_token()
    user_token_rcd = model.UserToken(user_id=user_id, token=token)
    db.add(user_token_rcd)
    db.commit()
    db.refresh(user_token_rcd)
    return user_token_rcd


def get_user_by_token(db: Session, token: str) -> model.User:
    user_token_rcd = (
        db.query(model.UserToken).filter(model.UserToken.token == token).first()
    )
    return user_token_rcd.user


def authenticate_user(db, name: str, password: str) -> Optional[model.User]:
    user_rcd = get_user_by_name(db, name)
    if not user_rcd:
        return None
    if not verify_password(password, user_rcd.hashed_password):
        return None
    return user_rcd


def get_payment_methods(db: Session, user_id: int) -> List[model.PaymentMethod]:
    return (
        db.query(model.PaymentMethod)
        .filter(model.PaymentMethod.user_id == user_id)
        .all()
    )


def create_payment_method(
    db: Session, user_id: int, payment_method: schema.RequestPaymentMethod
) -> model.PaymentMethod:
    payment_method_rcd = model.PaymentMethod(
        user_id=user_id,
        private_key=payment_method.private_key,
        type=payment_method.type,
    )
    db.add(payment_method_rcd)
    db.commit()
    db.refresh(payment_method_rcd)
    return payment_method_rcd


def get_payment_method(db: Session, payment_method_id: int) -> model.PaymentMethod:
    return (
        db.query(model.PaymentMethod)
        .filter(model.PaymentMethod.id == payment_method_id)
        .first()
    )


def delete_payment_method(db: Session, payment_method_id: int) -> bool:
    db.delete(get_payment_method(db, payment_method_id))
    db.commit()
    return True


def get_payment_rules(db: Session, user_id: int) -> List[model.PaymentRule]:
    return (
        db.query(model.PaymentRule)
        .join(model.PaymentRule.payment_method, model.PaymentMethod.user)
        .filter(model.User.id == user_id)
        .all()
    )


def create_payment_rule(
    db: Session, payment_rule: schema.RequestPaymentRule,
) -> model.PaymentRule:
    payment_rule_rcd = model.PaymentRule(**payment_rule.dict())
    db.add(payment_rule_rcd)
    db.commit()
    db.refresh(payment_rule_rcd)
    return payment_rule_rcd


def get_payment_rule(
    db: Session, payment_rule_id: int, user_id: int
) -> model.PaymentRule:
    return (
        db.query(model.PaymentRule)
        .join(model.PaymentRule.payment_method, model.PaymentMethod.user,)
        .filter(model.PaymentRule.id == payment_rule_id)
        .filter(model.User.id == user_id)
        .first()
    )


def delete_payment_rule(db: Session, payment_rule_id: int) -> bool:
    x = get_payment_rule(db, payment_rule_id)
    db.delete(x)
    db.commit()
    return True


def create_payment(db: Session, payment_rule_id: int) -> model.Payment:
    payment_rcd = model.Payment(payment_rule_id=payment_rule_id)
    db.add(payment_rcd)
    db.commit()
    db.refresh(payment_rcd)
    return payment_rcd


def get_payments(db: Session, user_id: int) -> List[model.Payment]:
    return (
        db.query(model.Payment)
        .join(
            model.Payment.payment_rule,
            model.PaymentRule.payment_method,
            model.PaymentMethod.user,
        )
        .filter(model.User.id == user_id)
        .all()
    )


def get_foundations(db: Session) -> List[model.Foundation]:
    return db.query(model.Foundation).all()


def create_foundation(
    db: Session, foundation: schema.RequestFoundation
) -> model.Foundation:
    foundation_rcd = model.Foundation(**foundation.dict())
    db.add(foundation_rcd)
    db.commit()
    db.refresh(foundation_rcd)
    return foundation_rcd
