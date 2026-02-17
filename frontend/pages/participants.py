import streamlit as st
from api import get, post

group_id = st.session_state.get("group_id")

if not group_id:
    st.warning("Select a group first")
    st.stop()

st.title("👤 Participants")

name = st.text_input("Participant Name")
if st.button("Add Participant"):
    post(f"/participants/{group_id}", {"name": name})
    st.rerun()

res = get(f"/participants/{group_id}")
participants = res.json() if res.status_code == 200 else []

for p in participants:
    st.write("•", p["name"])
