from auth import require_auth
require_auth()

import streamlit as st
from api import get, post

group_id = st.session_state.get("group_id")

st.title("💸 Expenses")

res = get(f"/participants/{group_id}")
participants = res.json()

payer = st.selectbox(
    "Paid By",
    participants,
    format_func=lambda x: x["name"]
)

amount = st.number_input("Amount", min_value=0.0)
desc = st.text_input("Description")

if st.button("Add Expense"):
    post("/expenses", {
        "groupId": group_id,
        "description": desc,
        "amount": amount,
        "paidBy": payer["_id"],
        "splitMode": "equal"
    })
    st.success("Expense added")
    st.rerun()
