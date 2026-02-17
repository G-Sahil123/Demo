import streamlit as st


def is_authenticated() -> bool:
    return bool(st.session_state.get("token"))


def require_auth():
    if not is_authenticated():
        st.warning("Please login first")
        st.switch_page("pages/1_Login.py")


def logout():
    st.session_state.token = None
    st.session_state.group_id = None
    st.rerun()
