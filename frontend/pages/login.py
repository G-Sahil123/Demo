import streamlit as st
from api import post

st.title("🔐 Login")

email = st.text_input("Email")
name = st.text_input("Name")

if st.button("Login"):
    res = post("/auth/google", {
        "email": email,
        "name": name,
        "googleId": email  # simple placeholder
    })

    if res.status_code == 200:
        st.session_state.token = res.json()["token"]
        st.success("Logged in successfully")
        st.rerun()
    else:
        st.error("Login failed")
