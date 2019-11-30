from sqlalchemy.orm import Session

from api import models, schemas
from api.security import hash_password, create_access_token


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.name == username).first()


def create_user(db: Session, user: schemas.RequestUser):
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
