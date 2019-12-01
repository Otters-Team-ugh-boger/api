import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from api.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    payment_methods = relationship("PaymentMethod", back_populates="user")
    tokens = relationship("UserToken", back_populates="user")


class UserToken(Base):
    __tablename__ = "user_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, server_default=expression.true(), default=True)
    token = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="tokens")


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    private_key = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="payment_methods")
    payment_rules = relationship("PaymentRule", back_populates="payment_method")


class Foundation(Base):
    __tablename__ = "foundations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    payment_address = Column(String)

    payment_rules = relationship("PaymentRule", back_populates="foundation")


class PaymentRule(Base):
    __tablename__ = "payment_rules"

    id = Column(Integer, primary_key=True, index=True)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"))
    foundation_id = Column(Integer, ForeignKey("foundations.id"))
    amount = Column(Numeric(precision=18))

    payment_method = relationship("PaymentMethod", back_populates="payment_rules")
    foundation = relationship("Foundation", back_populates="payment_rules")
    payment_history = relationship("Payment", back_populates="payment_rule")


class Payment(Base):
    __tablename__ = "payment_history"

    id = Column(Integer, primary_key=True, index=True)
    payment_rule_id = Column(Integer, ForeignKey("payment_rules.id"))
    transaction_hash = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    payment_rule = relationship("PaymentRule", back_populates="payment_history")
