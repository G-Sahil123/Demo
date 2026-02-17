from auth import require_auth
require_auth()

import streamlit as st
from api import get, post

st.title("👥 Groups")

# Create group
name = st.text_input("Group Name")
if st.button("Create Group"):
    post("/groups", {"name": name})
    st.success("Group created")
    st.rerun()

# List groups
res = get("/groups")
groups = res.json() if res.status_code == 200 else []

for g in groups:
    if st.button(g["name"], key=g["_id"]):
        st.session_state.group_id = g["_id"]
        st.rerun()
