from typing import List, Dict


def round2(num: float) -> float:
    return round(num + 1e-9, 2)


def calculate_balances(expenses) -> Dict[int, float]:
    balances: Dict[int, float] = {}

    for e in expenses:
        payer_id = e.paid_by

        # Credit payer
        if payer_id:
            balances[payer_id] = round2(balances.get(payer_id, 0) + e.amount)

        # Debit participants
        for split in e.splits:
            pid = split.participant_id
            if not pid:
                continue
            balances[pid] = round2(balances.get(pid, 0) - split.share_amount)

    # Remove near-zero noise
    for k in list(balances.keys()):
        if abs(balances[k]) < 0.01:
            balances[k] = 0

    return balances


def settle_balances(balances: Dict[int, float]) -> List[Dict]:
    debtors = []
    creditors = []

    for pid, amount in balances.items():
        if amount < 0:
            debtors.append({"id": pid, "amount": -amount})
        elif amount > 0:
            creditors.append({"id": pid, "amount": amount})

    settlements = []
    i = j = 0

    while i < len(debtors) and j < len(creditors):
        debtor = debtors[i]
        creditor = creditors[j]

        settle_amount = min(debtor["amount"], creditor["amount"])

        settlements.append({
            "from": debtor["id"],
            "to": creditor["id"],
            "amount": round(settle_amount, 2)
        })

        debtor["amount"] -= settle_amount
        creditor["amount"] -= settle_amount

        if debtor["amount"] == 0:
            i += 1
        if creditor["amount"] == 0:
            j += 1

    return settlements
