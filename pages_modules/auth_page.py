"""Authentication page — Login & Sign Up"""

import streamlit as st
from utils.supabase_client import sign_in, sign_up
from utils.session import set_user


def render():
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("""
        <div class="auth-container">
            <div class="auth-logo">
                <span class="auth-logo-icon">💸</span>
                <div class="auth-logo-title">SpendSmart AI</div>
                <div class="auth-logo-sub">Smart money tracking for modern life</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            _login_form()

        with tab_signup:
            _signup_form()

        st.markdown("""
        <div style="text-align:center; margin-top:24px; font-size:12px; color:var(--text-muted);">
            Your data is encrypted and private 🔒
        </div>
        """, unsafe_allow_html=True)


def _login_form():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    email    = st.text_input("Email address", key="login_email", placeholder="you@example.com")
    password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if st.button("Sign In →", type="primary", use_container_width=True, key="login_btn"):
        if not email or not password:
            st.error("Please fill in all fields.")
            return
        with st.spinner("Signing in…"):
            result = sign_in(email.strip(), password)
        if result["error"]:
            _friendly_error(result["error"])
        else:
            set_user(result["user"], result["access_token"], result["refresh_token"])
            st.success("Welcome back! 👋")
            st.rerun()


def _signup_form():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    email    = st.text_input("Email address", key="signup_email", placeholder="you@example.com")
    password = st.text_input("Password", type="password", key="signup_pass", placeholder="Min. 6 characters")
    confirm  = st.text_input("Confirm password", type="password", key="signup_confirm", placeholder="Repeat password")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if st.button("Create Account →", type="primary", use_container_width=True, key="signup_btn"):
        if not email or not password or not confirm:
            st.error("Please fill in all fields.")
            return
        if password != confirm:
            st.error("Passwords don't match.")
            return
        if len(password) < 6:
            st.error("Password must be at least 6 characters.")
            return
        with st.spinner("Creating your account…"):
            result = sign_up(email.strip(), password)
        if result.get("error"):
            _friendly_error(str(result["error"]))
        else:
            st.success("Account created! 🎉 Check your email to confirm, then sign in.")


def _friendly_error(msg: str):
    msg_lower = msg.lower()
    if "invalid login" in msg_lower or "invalid credentials" in msg_lower:
        st.error("❌ Incorrect email or password. Please try again.")
    elif "already registered" in msg_lower or "already exists" in msg_lower:
        st.error("❌ An account with this email already exists. Please sign in.")
    elif "email" in msg_lower:
        st.error("❌ Please enter a valid email address.")
    else:
        st.error(f"❌ {msg}")
