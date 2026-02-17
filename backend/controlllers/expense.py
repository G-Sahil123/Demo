from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Expense, Group, ExpenseSplit
from app.schemas import ExpenseCreate

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/")
def add_expense(payload: ExpenseCreate, db: Session = Depends(get_db)):

    final_splits = []

    if payload.splitMode == "equal":
        group = db.query(Group).filter(Group.id == payload.groupId).first()

        if not group or not group.participants:
            raise HTTPException(400, "Group has no participants")

        share = payload.amount / len(group.participants)

        for p in group.participants:
            final_splits.append(
                ExpenseSplit(participant_id=p.id, share_amount=share)
            )

    elif payload.splitMode == "custom":
        if not payload.splits:
            raise HTTPException(400, "Custom splits required")

        total = sum(s.shareAmount for s in payload.splits)
        if total != payload.amount:
            raise HTTPException(400, "Split amounts must equal total expense")

        for s in payload.splits:
            final_splits.append(
                ExpenseSplit(
                    participant_id=s.participantId,
                    share_amount=s.shareAmount
                )
            )

    else:
        raise HTTPException(400, "Invalid split mode")

    expense = Expense(
        group_id=payload.groupId,
        description=payload.description,
        amount=payload.amount,
        paid_by=payload.paidBy,
        split_mode=payload.splitMode,
        splits=final_splits
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


@router.get("/{group_id}")
def get_expenses(group_id: int, db: Session = Depends(get_db)):
    return db.query(Expense).filter(Expense.group_id == group_id).all()
