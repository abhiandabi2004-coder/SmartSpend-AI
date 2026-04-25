"""
Supabase client — all database operations live here.
Uses service-role key for server-side ops;
JWT token is passed for user-scoped RLS queries.
"""

from __future__ import annotations
import os
import streamlit as st
from supabase import create_client, Client
from typing import Optional

# ── Client factory ────────────────────────────────────────────────────────────

@st.cache_resource
def get_supabase_client() -> Client:
    """Return a cached Supabase client using env/secrets credentials."""
    try:
        url  = st.secrets["SUPABASE_URL"]
        key  = st.secrets["SUPABASE_ANON_KEY"]
    except Exception:
        url  = os.environ.get("SUPABASE_URL", "")
        key  = os.environ.get("SUPABASE_ANON_KEY", "")

    if not url or not key:
        st.error("⚠️ Supabase credentials not found. Check your secrets.toml or environment variables.")
        st.stop()

    return create_client(url, key)


def get_authed_client() -> Client:
    """Return client with user's JWT set so RLS policies apply correctly."""
    client = get_supabase_client()
    token  = st.session_state.get("access_token")
    if token:
        client.auth.set_session(
            access_token=token,
            refresh_token=st.session_state.get("refresh_token", ""),
        )
    return client


# ── Auth operations ───────────────────────────────────────────────────────────

def sign_up(email: str, password: str) -> dict:
    client = get_supabase_client()
    res = client.auth.sign_up({"email": email, "password": password})
    return {"user": res.user, "session": res.session, "error": None}


def sign_in(email: str, password: str) -> dict:
    client = get_supabase_client()
    try:
        res = client.auth.sign_in_with_password({"email": email, "password": password})
        return {
            "user": {"id": res.user.id, "email": res.user.email},
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "error": None,
        }
    except Exception as e:
        return {"user": None, "access_token": None, "refresh_token": None, "error": str(e)}


def sign_out():
    client = get_supabase_client()
    try:
        client.auth.sign_out()
    except Exception:
        pass


# ── Expense CRUD ──────────────────────────────────────────────────────────────

def get_expenses(user_id: str) -> list[dict]:
    """Fetch all expenses for this user, newest first."""
    try:
        client = get_authed_client()
        res = (
            client.table("expenses")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return res.data or []
    except Exception as e:
        st.error(f"Error fetching expenses: {e}")
        return []


def add_expense(user_id: str, amount: float, category: str, description: str) -> dict:
    """Insert a new expense row. Returns inserted row or error."""
    try:
        client = get_authed_client()
        res = (
            client.table("expenses")
            .insert({
                "user_id": user_id,
                "amount": round(float(amount), 2),
                "category": category,
                "description": description,
            })
            .execute()
        )
        return {"data": res.data, "error": None}
    except Exception as e:
        return {"data": None, "error": str(e)}


def update_expense(expense_id: int, user_id: str, amount: float, category: str, description: str) -> dict:
    """Update an existing expense. user_id check prevents cross-user edits."""
    try:
        client = get_authed_client()
        res = (
            client.table("expenses")
            .update({
                "amount": round(float(amount), 2),
                "category": category,
                "description": description,
            })
            .eq("id", expense_id)
            .eq("user_id", user_id)
            .execute()
        )
        return {"data": res.data, "error": None}
    except Exception as e:
        return {"data": None, "error": str(e)}


def delete_expense(expense_id: int, user_id: str) -> dict:
    """Delete an expense. Scoped to user_id for safety."""
    try:
        client = get_authed_client()
        res = (
            client.table("expenses")
            .delete()
            .eq("id", expense_id)
            .eq("user_id", user_id)
            .execute()
        )
        return {"error": None}
    except Exception as e:
        return {"error": str(e)}


# ── Analytics helpers ─────────────────────────────────────────────────────────

def get_spending_summary(expenses: list[dict]) -> dict:
    """Compute totals, category breakdown, and top category from expense list."""
    if not expenses:
        return {
            "total": 0,
            "count": 0,
            "by_category": {},
            "top_category": None,
            "top_category_amount": 0,
            "avg_transaction": 0,
        }

    total = sum(e["amount"] for e in expenses)
    by_cat: dict[str, float] = {}
    for e in expenses:
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + e["amount"]

    top_cat = max(by_cat, key=by_cat.get)

    return {
        "total": round(total, 2),
        "count": len(expenses),
        "by_category": {k: round(v, 2) for k, v in sorted(by_cat.items(), key=lambda x: -x[1])},
        "top_category": top_cat,
        "top_category_amount": round(by_cat[top_cat], 2),
        "avg_transaction": round(total / len(expenses), 2),
    }
