import streamlit as st
from api import get, post
from auth import require_auth

require_auth()

group_id = st.session_state.get("group_id")
st.title("💸 Expenses")

# Load participants
res = get(f"/participants/{group_id}")
participants = res.json()

payer = st.selectbox(
    "Paid By",
    participants,
    format_func=lambda x: x["name"]
)

amount = st.number_input("Amount", min_value=0.0)
desc = st.text_input("Description")

split_mode = st.radio("Split Mode", ["equal", "custom"])

splits = []

if split_mode == "custom":
    st.subheader("Custom Split")
    remaining = amount

    for p in participants:
        share = st.number_input(
            f"{p['name']}",
            min_value=0.0,
            key=p["_id"]
        )
        splits.append({
            "participantId": p["_id"],
            "shareAmount": share
        })
        remaining -= share

    st.write("Remaining:", round(remaining, 2))

if st.button("Add Expense"):
    payload = {
        "groupId": group_id,
        "description": desc,
        "amount": amount,
        "paidBy": payer["_id"],
        "splitMode": split_mode,
        "splits": splits if split_mode == "custom" else []
    }
    post("/expenses", payload)
    st.success("Expense added")
    st.rerun()
