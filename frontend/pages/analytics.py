import streamlit as st
from api import get

group_id = st.session_state.get("group_id")

st.title("📊 Analytics")

res = get(f"/analytics/{group_id}")
data = res.json()

st.metric("Total Spent", data["totalSpent"])
st.metric("Average / Person", data["avgPerPerson"])

st.subheader("Balances")
for name, amt in data["balances"].items():
    st.write(f"{name}: {amt}")

st.subheader("Settlements")
for s in data["settlements"]:
    st.write(f"{s['from']} → {s['to']} : ₹{s['amount']}")
