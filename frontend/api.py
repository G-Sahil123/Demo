import requests
import streamlit as st

BASE_URL = "http://localhost:8000/api"


def auth_headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def post(path, data):
    return requests.post(
        f"{BASE_URL}{path}",
        json=data,
        headers=auth_headers()
    )


def get(path):
    return requests.get(
        f"{BASE_URL}{path}",
        headers=auth_headers()
    )
