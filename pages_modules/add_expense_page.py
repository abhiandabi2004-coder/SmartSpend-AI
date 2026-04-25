"""Add Expense page — form to record a new expense"""

import streamlit as st
from utils.supabase_client import add_expense
from utils.session import get_user_id
from utils.categories import CATEGORIES, get_icon


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Add Expense</div>
        <div class="page-subtitle">Record a new transaction to track your spending</div>
    </div>
    """, unsafe_allow_html=True)

    user_id = get_user_id()

    col_form, col_tips = st.columns([1.2, 1])

    with col_form:
        st.markdown("""
        <div style="background:var(--bg-card); border:1px solid var(--border);
                    border-radius:var(--radius-lg); padding:28px 28px 24px;">
        """, unsafe_allow_html=True)

        amount      = st.number_input("Amount (₹)", min_value=0.01, step=0.01, format="%.2f", key="add_amount")
        category    = st.selectbox(
            "Category",
            CATEGORIES,
            format_func=lambda c: f"{get_icon(c)}  {c}",
            key="add_category",
        )
        description = st.text_input("Description", placeholder="e.g. Lunch at Saravana Bhavan", key="add_desc", max_chars=120)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("➕ Add Expense", type="primary", use_container_width=True, key="add_btn"):
            if amount <= 0:
                st.error("Please enter an amount greater than 0.")
            elif not description.strip():
                st.error("Please add a short description.")
            else:
                with st.spinner("Saving…"):
                    result = add_expense(user_id, amount, category, description.strip())
                if result["error"]:
                    st.error(f"❌ Failed to save: {result['error']}")
                else:
                    st.success(f"✅ Expense of ₹{amount:,.2f} added successfully!")
                    st.balloons()

        st.markdown("</div>", unsafe_allow_html=True)

    with col_tips:
        st.markdown("""
        <div style="background:var(--bg-card); border:1px solid var(--border);
                    border-radius:var(--radius-lg); padding:28px;">
            <div class="section-title" style="margin-bottom:16px">💡 Quick Tips</div>
        """, unsafe_allow_html=True)

        tips = [
            ("🍜 Food", "Include meals, groceries, snacks, and food delivery"),
            ("🚌 Transport", "Bus, auto, fuel, Ola/Uber, Metro card top-ups"),
            ("🎬 Entertainment", "OTT, movies, games, events, outings"),
            ("🛍️ Shopping", "Clothes, gadgets, personal items, Amazon orders"),
            ("💊 Health", "Medical bills, pharmacy, gym membership"),
            ("📚 Education", "Books, courses, college fees, stationery"),
            ("⚡ Utilities", "Phone bill, internet, electricity, water"),
        ]

        for icon_cat, desc in tips:
            st.markdown(f"""
            <div style="display:flex; gap:12px; margin-bottom:12px; align-items:flex-start">
                <div style="font-size:13px; font-weight:600; color:var(--text-primary);
                            min-width:110px">{icon_cat}</div>
                <div style="font-size:12px; color:var(--text-secondary)">{desc}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
