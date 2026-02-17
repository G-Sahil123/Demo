import streamlit as st
from api import get, post, put, delete
from auth import require_auth

require_auth()

group_id = st.session_state.get("group_id")
st.title("💸 Expenses")

# -------------------------------
# Load participants
# -------------------------------
res = get(f"/participants/{group_id}")
participants = res.json()

participant_map = {p["_id"]: p["name"] for p in participants}

# -------------------------------
# EDIT MODE STATE
# -------------------------------
edit_expense = st.session_state.get("edit_expense")

st.subheader("➕ Add / Edit Expense")

payer = st.selectbox(
    "Paid By",
    participants,
    format_func=lambda x: x["name"],
    index=(
        next(
            (i for i, p in enumerate(participants)
             if edit_expense and p["_id"] == edit_expense["paidBy"]),
            0
        )
        if edit_expense else 0
    )
)

amount = st.number_input(
    "Amount",
    min_value=0.0,
    value=edit_expense["amount"] if edit_expense else 0.0
)

desc = st.text_input(
    "Description",
    value=edit_expense["description"] if edit_expense else ""
)

split_mode = st.radio(
    "Split Mode",
    ["equal", "custom"],
    index=0 if not edit_expense or edit_expense["splitMode"] == "equal" else 1
)

splits = []

if split_mode == "custom":
    st.subheader("Custom Split")
    remaining = amount

    existing_splits = {
        s["participantId"]: s["shareAmount"]
        for s in (edit_expense["splits"] if edit_expense else [])
    }

    for p in participants:
        share = st.number_input(
            p["name"],
            min_value=0.0,
            value=existing_splits.get(p["_id"], 0.0),
            key=f"split-{p['_id']}"
        )
        splits.append({
            "participantId": p["_id"],
            "shareAmount": share
        })
        remaining -= share

    st.info(f"Remaining: ₹{round(remaining, 2)}")

# -------------------------------
# SAVE BUTTON
# -------------------------------
if st.button("💾 Save Expense"):
    payload = {
        "groupId": group_id,
        "description": desc,
        "amount": amount,
        "paidBy": payer["_id"],
        "splitMode": split_mode,
        "splits": splits if split_mode == "custom" else []
    }

    if edit_expense:
        put(f"/expenses/{edit_expense['_id']}", payload)
        st.success("Expense updated")
        st.session_state.edit_expense = None
    else:
        post("/expenses", payload)
        st.success("Expense added")

    st.rerun()

# -------------------------------
# LIST EXPENSES
# -------------------------------
st.divider()
st.subheader("📋 Expense List")

res = get(f"/expenses/{group_id}")
expenses = res.json()

for e in expenses:
    col1, col2, col3 = st.columns([6, 1, 1])

    col1.write(
        f"**{e['description']}** — ₹{e['amount']}  \n"
        f"Paid by: {participant_map.get(e['paidBy'], 'Unknown')}"
    )

    if col2.button("✏️", key=f"edit-{e['_id']}"):
        st.session_state.edit_expense = e
        st.rerun()

    if col3.button("🗑️", key=f"del-{e['_id']}"):
        delete(f"/expenses/{e['_id']}")
        st.warning("Expense deleted")
        st.rerun()
