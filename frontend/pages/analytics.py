from auth import require_auth
require_auth()

import streamlit as st
import pandas as pd
from api import get

group_id = st.session_state.get("group_id")

st.title("📊 Analytics")

res = get(f"/analytics/{group_id}")
data = res.json()

# -------------------------------
# METRICS
# -------------------------------
col1, col2 = st.columns(2)
col1.metric("💰 Total Spent", f"₹{data['totalSpent']}")
col2.metric("👤 Avg / Person", f"₹{data['avgPerPerson']}")

# -------------------------------
# BALANCES TABLE
# -------------------------------
st.subheader("⚖️ Balances")

balances_df = pd.DataFrame(
    list(data["balances"].items()),
    columns=["Participant", "Balance"]
)

st.dataframe(balances_df, use_container_width=True)

# -------------------------------
# PIE CHART
# -------------------------------
st.subheader("🥧 Spending Distribution")

st.pyplot(
    balances_df.set_index("Participant")
    .plot.pie(
        y="Balance",
        autopct="%1.1f%%",
        legend=False,
        figsize=(5, 5)
    ).figure
)

# -------------------------------
# BAR CHART
# -------------------------------
st.subheader("📊 Balance Comparison")

st.bar_chart(
    balances_df.set_index("Participant")
)

# -------------------------------
# SETTLEMENTS
# -------------------------------
st.subheader("🔁 Settlements")

if not data["settlements"]:
    st.info("No settlements needed 🎉")
else:
    for s in data["settlements"]:
        st.write(f"➡️ **{s['from']} → {s['to']}** : ₹{s['amount']}")
