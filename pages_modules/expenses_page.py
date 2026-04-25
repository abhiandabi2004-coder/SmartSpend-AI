"""My Expenses page — list, filter, edit, delete, and export"""

import streamlit as st
import pandas as pd
from utils.supabase_client import get_expenses, update_expense, delete_expense
from utils.session import get_user_id
from utils.categories import CATEGORIES, get_icon, get_color, get_bg


def render():
    user_id = get_user_id()

    st.markdown("""
    <div class="page-header">
        <div class="page-title">My Expenses</div>
        <div class="page-subtitle">Manage and review all your transactions</div>
    </div>""", unsafe_allow_html=True)

    expenses = get_expenses(user_id)

    if not expenses:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px; background:var(--bg-card);
                    border:1px solid var(--border); border-radius:var(--radius-lg);">
            <div style="font-size:40px; margin-bottom:12px">📭</div>
            <div style="font-family:var(--font-display); font-size:18px; font-weight:700;
                        color:var(--text-primary); margin-bottom:6px">No expenses found</div>
            <div style="color:var(--text-secondary); font-size:13px">Go to Add Expense to record your first transaction</div>
        </div>""", unsafe_allow_html=True)
        return

    # ── Filters ───────────────────────────────────────────────────────────────
    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
    with col_f1:
        search = st.text_input("🔍 Search", placeholder="Search descriptions…", key="exp_search")
    with col_f2:
        filter_cat = st.selectbox("Category", ["All"] + CATEGORIES, key="exp_cat")
    with col_f3:
        sort_by = st.selectbox("Sort by", ["Newest first", "Oldest first", "Highest amount", "Lowest amount"], key="exp_sort")

    # Apply filters
    filtered = expenses
    if search:
        filtered = [e for e in filtered if search.lower() in e.get("description", "").lower()]
    if filter_cat != "All":
        filtered = [e for e in filtered if e["category"] == filter_cat]

    # Sort
    if sort_by == "Oldest first":
        filtered = sorted(filtered, key=lambda x: x.get("created_at", ""))
    elif sort_by == "Highest amount":
        filtered = sorted(filtered, key=lambda x: x["amount"], reverse=True)
    elif sort_by == "Lowest amount":
        filtered = sorted(filtered, key=lambda x: x["amount"])

    # ── Export ────────────────────────────────────────────────────────────────
    if filtered:
        df = pd.DataFrame([{
            "Date": str(e.get("created_at", ""))[:10],
            "Category": e["category"],
            "Description": e.get("description", ""),
            "Amount (₹)": e["amount"],
        } for e in filtered])

        col_info, col_export = st.columns([2, 1])
        with col_info:
            total = sum(e["amount"] for e in filtered)
            st.markdown(f"""
            <div style="font-size:13px; color:var(--text-secondary); padding:8px 0">
                Showing <b style="color:var(--text-primary)">{len(filtered)}</b> expenses
                · Total: <b style="color:var(--accent-red)">₹{total:,.2f}</b>
            </div>""", unsafe_allow_html=True)
        with col_export:
            csv = df.to_csv(index=False)
            st.download_button(
                "⬇️ Export CSV",
                data=csv,
                file_name="spendsmart_expenses.csv",
                mime="text/csv",
                use_container_width=True,
                key="export_csv",
            )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Expense rows ──────────────────────────────────────────────────────────
    if "edit_id" not in st.session_state:
        st.session_state.edit_id = None

    for expense in filtered:
        _expense_row(expense, user_id, expenses)

    # If editing, show edit form below
    if st.session_state.edit_id:
        _edit_form(st.session_state.edit_id, user_id, expenses)


def _expense_row(expense: dict, user_id: str, all_expenses: list):
    eid   = expense["id"]
    cat   = expense["category"]
    icon  = get_icon(cat)
    color = get_color(cat)
    bg    = get_bg(cat)
    desc  = expense.get("description", "—")
    date  = str(expense.get("created_at", ""))[:10]
    amt   = expense["amount"]

    col_main, col_edit, col_del = st.columns([5, 0.7, 0.7])

    with col_main:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:14px;
                    background:var(--bg-card); border:1px solid var(--border);
                    border-radius:var(--radius-md); padding:14px 18px;">
            <div style="width:40px; height:40px; border-radius:10px; background:{bg};
                        color:{color}; display:flex; align-items:center;
                        justify-content:center; font-size:20px; flex-shrink:0">{icon}</div>
            <div style="flex:1; min-width:0">
                <div style="font-size:14px; font-weight:500; color:var(--text-primary);
                            white-space:nowrap; overflow:hidden; text-overflow:ellipsis">{desc}</div>
                <div style="font-size:12px; color:var(--text-muted); margin-top:2px">{cat} · {date}</div>
            </div>
            <div style="font-family:var(--font-mono); font-size:16px; font-weight:500;
                        color:var(--accent-red); flex-shrink:0">-₹{amt:,.2f}</div>
        </div>""", unsafe_allow_html=True)

    with col_edit:
        st.markdown("<div style='margin-top:6px'>", unsafe_allow_html=True)
        if st.button("✏️", key=f"edit_{eid}", help="Edit expense", use_container_width=True):
            st.session_state.edit_id = eid
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_del:
        st.markdown("<div style='margin-top:6px'>", unsafe_allow_html=True)
        if st.button("🗑️", key=f"del_{eid}", help="Delete expense", use_container_width=True):
            result = delete_expense(eid, user_id)
            if result["error"]:
                st.error(f"❌ {result['error']}")
            else:
                st.success("Deleted!")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def _edit_form(edit_id: int, user_id: str, expenses: list):
    exp = next((e for e in expenses if e["id"] == edit_id), None)
    if not exp:
        st.session_state.edit_id = None
        return

    st.markdown("""
    <div style="background:var(--bg-elevated); border:1px solid var(--border-active);
                border-radius:var(--radius-lg); padding:24px; margin-top:16px">
        <div class="section-title" style="margin-bottom:16px">✏️ Edit Expense</div>
    """, unsafe_allow_html=True)

    cat_idx = CATEGORIES.index(exp["category"]) if exp["category"] in CATEGORIES else 0

    new_amount   = st.number_input("Amount (₹)", value=float(exp["amount"]), min_value=0.01, step=0.01, format="%.2f", key="edit_amount")
    new_category = st.selectbox("Category", CATEGORIES, index=cat_idx, format_func=lambda c: f"{get_icon(c)}  {c}", key="edit_cat")
    new_desc     = st.text_input("Description", value=exp.get("description", ""), key="edit_desc", max_chars=120)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 Save Changes", type="primary", use_container_width=True, key="save_edit"):
            if not new_desc.strip():
                st.error("Description cannot be empty.")
            else:
                result = update_expense(edit_id, user_id, new_amount, new_category, new_desc.strip())
                if result["error"]:
                    st.error(f"❌ {result['error']}")
                else:
                    st.success("✅ Expense updated!")
                    st.session_state.edit_id = None
                    st.rerun()
    with c2:
        if st.button("✕ Cancel", use_container_width=True, key="cancel_edit"):
            st.session_state.edit_id = None
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
