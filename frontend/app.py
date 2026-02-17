import streamlit as st

st.set_page_config(
    page_title="HisabKitab",
    layout="wide"
)

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None

if "group_id" not in st.session_state:
    st.session_state.group_id = None

# Sidebar
with st.sidebar:
    st.title("📒 HisabKitab")

    if st.session_state.token:
        st.success("Logged in")

        if st.button("🚪 Logout"):
            st.session_state.token = None
            st.session_state.group_id = None
            st.rerun()
    else:
        st.info("Please login")

# Route guard
if not st.session_state.token:
    st.switch_page("pages/1_Login.py")
