"""Dashboard — overview stats, charts, recent transactions"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.supabase_client import get_expenses, get_spending_summary
from utils.session import get_user_id
from utils.categories import get_icon, get_color, get_bg


def render():
    user_id = get_user_id()

    st.markdown("""
    <div class="page-header">
        <div class="page-title">Dashboard</div>
        <div class="page-subtitle">Your financial snapshot at a glance</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading your data…"):
        expenses = get_expenses(user_id)

    summary  = get_spending_summary(expenses)

    # ── KPI Cards ────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="stat-card" style="--accent-color: #fc6d6d">
            <div class="stat-label">Total Spent</div>
            <div class="stat-value">₹{summary['total']:,.0f}</div>
            <div class="stat-meta">{summary['count']} transactions</div>
            <div class="stat-icon">💳</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        top = summary.get("top_category", "—")
        icon = get_icon(top) if top else "—"
        st.markdown(f"""
        <div class="stat-card" style="--accent-color: {get_color(top)}">
            <div class="stat-label">Top Category</div>
            <div class="stat-value" style="font-size:22px">{icon} {top}</div>
            <div class="stat-meta">₹{summary.get('top_category_amount', 0):,.0f} spent</div>
            <div class="stat-icon">🏷️</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="stat-card" style="--accent-color: #56cfae">
            <div class="stat-label">Avg Transaction</div>
            <div class="stat-value">₹{summary.get('avg_transaction', 0):,.0f}</div>
            <div class="stat-meta">per expense</div>
            <div class="stat-icon">📊</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        cats = len(summary.get("by_category", {}))
        st.markdown(f"""
        <div class="stat-card" style="--accent-color: #a78bfa">
            <div class="stat-label">Categories Used</div>
            <div class="stat-value">{cats}</div>
            <div class="stat-meta">out of 9 categories</div>
            <div class="stat-icon">🗂️</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # ── Charts row ────────────────────────────────────────────────────────────
    if expenses:
        col_chart, col_recent = st.columns([1.1, 1])

        with col_chart:
            st.markdown("""
            <div class="section-header">
                <div class="section-title">Spending by Category</div>
            </div>""", unsafe_allow_html=True)
            _donut_chart(summary["by_category"])

        with col_recent:
            st.markdown("""
            <div class="section-header">
                <div class="section-title">Recent Transactions</div>
            </div>""", unsafe_allow_html=True)
            _recent_transactions(expenses[:8])
    else:
        _empty_state()


def _donut_chart(by_category: dict):
    if not by_category:
        return

    labels = list(by_category.keys())
    values = list(by_category.values())
    colors = [get_color(c) for c in labels]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color="#0a0d14", width=2)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>₹%{value:,.2f}<br>%{percent}<extra></extra>",
    )])

    total = sum(values)
    fig.add_annotation(
        text=f"₹{total:,.0f}",
        x=0.5, y=0.54,
        font=dict(family="Syne", size=20, color="#eef2f7"),
        showarrow=False,
    )
    fig.add_annotation(
        text="total",
        x=0.5, y=0.44,
        font=dict(family="DM Sans", size=12, color="#8b93a7"),
        showarrow=False,
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=0, b=0, l=0, r=0),
        height=280,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(family="DM Sans", size=12, color="#8b93a7"),
            bgcolor="rgba(0,0,0,0)",
        ),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _recent_transactions(expenses: list):
    rows = ""
    for e in expenses:
        icon = get_icon(e["category"])
        color = get_color(e["category"])
        bg    = get_bg(e["category"])
        date  = str(e.get("created_at", ""))[:10] if e.get("created_at") else ""
        desc  = e.get("description", "—")[:28]
        rows += f"""
        <div class="txn-row">
            <div class="txn-icon" style="background:{bg}; color:{color}">{icon}</div>
            <div class="txn-info">
                <div class="txn-desc">{desc}</div>
                <div class="txn-cat">{e['category']}</div>
            </div>
            <div style="text-align:right">
                <div class="txn-amount">-₹{e['amount']:,.2f}</div>
                <div class="txn-date">{date}</div>
            </div>
        </div>"""

    st.markdown(f"""
    <div style="background:var(--bg-card); border:1px solid var(--border);
                border-radius:var(--radius-lg); padding:4px 20px;">
        {rows}
    </div>""", unsafe_allow_html=True)


def _empty_state():
    st.markdown("""
    <div style="text-align:center; padding:60px 20px; background:var(--bg-card);
                border:1px solid var(--border); border-radius:var(--radius-lg);">
        <div style="font-size:48px; margin-bottom:16px;">📭</div>
        <div style="font-family:var(--font-display); font-size:20px; font-weight:700;
                    color:var(--text-primary); margin-bottom:8px;">No expenses yet</div>
        <div style="color:var(--text-secondary); font-size:14px;">
            Add your first expense to start tracking your spending
        </div>
    </div>""", unsafe_allow_html=True)
