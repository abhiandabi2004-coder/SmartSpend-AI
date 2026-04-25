"""
💸 SpendSmart AI — Expense Management Web App
Main entry point — handles routing between pages
"""

import streamlit as st
from pages_modules import (
    auth_page,
    dashboard_page,
    add_expense_page,
    expenses_page,
    ai_advisor_page,
)
from utils.session import init_session
from utils.theme import inject_global_css
from utils.supabase_client import sign_out  # ✅ FIXED

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SpendSmart AI",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()
init_session()

# ── Session Safety Check ─────────────────────────────────────────────────────
if "user" not in st.session_state or st.session_state.user is None:
    st.session_state.user = None

# ── Route based on auth state ─────────────────────────────────────────────────
if not st.session_state.user:
    auth_page.render()
    st.stop()

# ── Sidebar Navigation ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span class="brand-icon">💸</span>
        <span class="brand-name">SpendSmart</span>
        <span class="brand-ai">AI</span>
    </div>
    """, unsafe_allow_html=True)

    # ✅ Safe user handling
    user = st.session_state.user
    user_email = (
        user["email"] if isinstance(user, dict)
        else getattr(user, "email", "User")
    )

    st.markdown(f"""
    <div class="user-pill">
        <span class="user-avatar">{user_email[0].upper()}</span>
        <span class="user-email">{user_email}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='nav-label'>NAVIGATION</div>", unsafe_allow_html=True)

    pages = {
        "📊 Dashboard": "dashboard",
        "➕ Add Expense": "add_expense",
        "📋 My Expenses": "expenses",
        "🤖 AI Advisor": "ai_advisor",
    }

    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"

    for label, key in pages.items():
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.current_page = key
            st.rerun()

    st.markdown("<div class='sidebar-spacer'></div>", unsafe_allow_html=True)

    # ✅ FIXED LOGOUT (IMPORTANT)
    if st.button("🚪 Sign Out", use_container_width=True, key="signout"):
        try:
            sign_out()  # 🔥 logs out from Supabase properly
        except Exception:
            pass
        st.session_state.clear()
        st.rerun()

# ── Render Active Page ───────────────────────────────────────────────────────
page = st.session_state.get("current_page", "dashboard")

st.title(page.replace("_", " ").title())

# ✅ Error boundary (prevents crash)
try:
    if page == "dashboard":
        dashboard_page.render()
    elif page == "add_expense":
        add_expense_page.render()
    elif page == "expenses":
        expenses_page.render()
    elif page == "ai_advisor":
        ai_advisor_page.render()
    else:
        st.error("Page not found")

except Exception as e:
    st.error("⚠️ Something went wrong")
    st.exception(e)