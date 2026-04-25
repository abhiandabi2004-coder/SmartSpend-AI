"""Session state initialization and helpers"""

import streamlit as st

def init_session():
    """Initialize all required session state keys"""
    defaults = {
        "user": None,
        "access_token": None,
        "refresh_token": None,
        "current_page": "dashboard",
        "edit_expense_id": None,
        "expense_form_submitted": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def get_user_id() -> str | None:
    """Return current user's UUID or None"""
    user = st.session_state.get("user")
    return user.get("id") if user else None

def get_user_email() -> str:
    user = st.session_state.get("user")
    return user.get("email", "User") if user else "User"

def is_authenticated() -> bool:
    return bool(st.session_state.get("user"))

def set_user(user_data: dict, access_token: str, refresh_token: str):
    st.session_state.user = user_data
    st.session_state.access_token = access_token
    st.session_state.refresh_token = refresh_token

def clear_session():
    for key in ["user", "access_token", "refresh_token", "current_page"]:
        st.session_state[key] = None if key != "current_page" else "dashboard"
