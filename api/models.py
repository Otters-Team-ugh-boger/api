from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from api.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    payment_methods = relationship("PaymentMethod", back_populates="user")


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    private_key = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="payment_methods")


class Foundation(Base):
    __tablename__ = "foundations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    payment_address = Column(String)
