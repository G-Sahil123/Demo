from sqlalchemy import (
    Column, Integer, String, Float,
    ForeignKey, DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    google_id = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    groups = relationship("Group", back_populates="owner")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    owner = relationship("User", back_populates="groups")
    participants = relationship(
        "Participant",
        back_populates="group",
        cascade="all, delete"
    )

    expenses = relationship(
        "Expense",
        back_populates="group",
        cascade="all, delete"
    )

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    color = Column(String)

    group_id = Column(Integer, ForeignKey("groups.id"))

    group = relationship("Group", back_populates="participants")
    expenses_paid = relationship("Expense", back_populates="payer")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    split_mode = Column(String)

    group_id = Column(Integer, ForeignKey("groups.id"))
    paid_by = Column(Integer, ForeignKey("participants.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    group = relationship("Group", back_populates="expenses")
    payer = relationship("Participant", back_populates="expenses_paid")

    splits = relationship(
        "ExpenseSplit",
        back_populates="expense",
        cascade="all, delete"
    )

class ExpenseSplit(Base):
    __tablename__ = "expense_splits"

    id = Column(Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"))
    participant_id = Column(Integer, ForeignKey("participants.id"))
    share_amount = Column(Float)

    expense = relationship("Expense", back_populates="splits")
    participant = relationship("Participant")
