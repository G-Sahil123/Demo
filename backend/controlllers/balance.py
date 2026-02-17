from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Group, Expense
from app.utils.settlement_engine import calculate_balances, settle_balances

router = APIRouter(prefix="/balances", tags=["Balances"])

@router.get("/{group_id}")
def get_balances(group_id: int, db: Session = Depends(get_db)):

    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()

    raw_balances = calculate_balances(expenses)
    settlements = settle_balances(raw_balances)

    total_spent = sum(e.amount for e in expenses)

    id_to_name = {p.id: p.name for p in group.participants}

    balances = {
        id_to_name.get(pid, pid): amount
        for pid, amount in raw_balances.items()
    }

    named_settlements = [
        {
            "from": id_to_name.get(s["from"], s["from"]),
            "to": id_to_name.get(s["to"], s["to"]),
            "amount": round(s["amount"], 2)
        }
        for s in settlements
    ]

    members = len(balances)
    avg_per_person = total_spent / members if members else 0

    return {
        "totalSpent": total_spent,
        "expenseCount": len(expenses),
        "avgPerPerson": avg_per_person,
        "balances": balances,
        "settlements": named_settlements,
        "membersCount": members
    }
