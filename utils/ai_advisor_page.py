"""AI Financial Advisor page — personalized insights powered by Claude"""

import streamlit as st
from utils.supabase_client import get_expenses, get_spending_summary
from utils.session import get_user_id
from utils.ai_advisor import get_ai_insights
from utils.categories import get_icon, get_color


def render():
    user_id = get_user_id()

    st.markdown("""
    <div class="page-header">
        <div class="page-title">🤖 AI Financial Advisor</div>
        <div class="page-subtitle">Personalized insights powered by Claude AI</div>
    </div>""", unsafe_allow_html=True)

    with st.spinner("Loading your expense data…"):
        expenses = get_expenses(user_id)

    summary = get_spending_summary(expenses)

    if not expenses:
        st.info("ℹ️ Add some expenses first to get personalized AI insights!")
        return

    # ── Score card + Analyze button ──────────────────────────────────────────
    col_score, col_action = st.columns([2, 1])

    with col_score:
        _score_preview(summary)

    with col_action:
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:var(--bg-card); border:1px solid var(--border);
                    border-radius:var(--radius-lg); padding:24px">
            <div style="font-size:13px; color:var(--text-secondary); margin-bottom:16px; line-height:1.5">
                Our AI analyzes your spending patterns and generates personalized recommendations.
            </div>
        """, unsafe_allow_html=True)
        analyze = st.button("⚡ Analyze My Spending", type="primary", use_container_width=True, key="analyze_btn")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Run analysis ──────────────────────────────────────────────────────────
    if analyze or st.session_state.get("ai_insights"):
        if analyze:
            with st.spinner("🤖 Claude is analyzing your spending patterns…"):
                insights = get_ai_insights(expenses, summary)
            st.session_state.ai_insights = insights
        else:
            insights = st.session_state.ai_insights

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        _render_insights(insights, summary)


def _score_preview(summary: dict):
    total = summary["total"]
    cats  = len(summary.get("by_category", {}))

    st.markdown(f"""
    <div style="background:var(--bg-card); border:1px solid var(--border);
                border-radius:var(--radius-lg); padding:24px; margin-top:0">
        <div class="stat-label" style="margin-bottom:12px">SPENDING OVERVIEW</div>
        <div style="display:flex; gap:24px; flex-wrap:wrap">
            <div>
                <div style="font-family:var(--font-display); font-size:28px; font-weight:800;
                            color:var(--text-primary)">₹{total:,.0f}</div>
                <div style="font-size:12px; color:var(--text-muted); margin-top:2px">total tracked</div>
            </div>
            <div>
                <div style="font-family:var(--font-display); font-size:28px; font-weight:800;
                            color:var(--text-primary)">{summary['count']}</div>
                <div style="font-size:12px; color:var(--text-muted); margin-top:2px">transactions</div>
            </div>
            <div>
                <div style="font-family:var(--font-display); font-size:28px; font-weight:800;
                            color:var(--text-primary)">{cats}</div>
                <div style="font-size:12px; color:var(--text-muted); margin-top:2px">categories</div>
            </div>
        </div>
        <div style="margin-top:16px">
            <div style="font-size:12px; color:var(--text-muted); margin-bottom:6px">
                Top: {get_icon(summary.get('top_category','Other'))} {summary.get('top_category','—')}
                (₹{summary.get('top_category_amount',0):,.0f})
            </div>
        </div>
    </div>""", unsafe_allow_html=True)


def _render_insights(insights: dict, summary: dict):
    # Health score
    score = insights.get("score", 75)
    label = insights.get("score_label", "Good")
    score_color = {
        "Excellent": "#56cfae",
        "Good":      "#63b3ed",
        "Fair":      "#f6c90e",
        "Needs Work":"#fc6d6d",
    }.get(label, "#63b3ed")

    st.markdown(f"""
    <div style="background:var(--bg-card); border:1px solid var(--border);
                border-radius:var(--radius-lg); padding:24px; margin-bottom:20px;
                display:flex; align-items:center; gap:24px">
        <div style="text-align:center; flex-shrink:0">
            <div style="font-family:var(--font-display); font-size:44px; font-weight:800;
                        color:{score_color}">{score}</div>
            <div style="font-size:11px; font-weight:600; letter-spacing:0.08em;
                        color:{score_color}; text-transform:uppercase">{label}</div>
        </div>
        <div style="flex:1; min-width:0">
            <div style="background:var(--bg-elevated); border-radius:100px;
                        height:8px; overflow:hidden; margin-bottom:10px">
                <div style="width:{score}%; height:100%; background:linear-gradient(90deg, {score_color}80, {score_color});
                             border-radius:100px; transition:width 0.5s ease"></div>
            </div>
            <div style="font-size:13px; font-weight:600; color:var(--text-primary);
                        margin-bottom:4px">Financial Health Score</div>
            <div style="font-size:12px; color:var(--text-secondary)">
                Based on your spending patterns and budget thresholds
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Summary
    st.markdown(f"""
    <div class="insight-card insight-summary">
        <div class="insight-type">📋 Summary</div>
        <div class="insight-body">{insights.get('summary', '')}</div>
    </div>""", unsafe_allow_html=True)

    # Warnings
    warnings = insights.get("warnings", [])
    if warnings:
        for w in warnings:
            st.markdown(f"""
            <div class="insight-card insight-warning">
                <div class="insight-type">⚠️ Warning</div>
                <div class="insight-body">{w}</div>
            </div>""", unsafe_allow_html=True)

    # Tips
    tips = insights.get("tips", [])
    if tips:
        st.markdown("""
        <div style="font-family:var(--font-display); font-size:16px; font-weight:700;
                    color:var(--text-primary); margin:20px 0 12px">💡 Personalized Tips</div>""",
        unsafe_allow_html=True)

        for i, tip in enumerate(tips, 1):
            st.markdown(f"""
            <div class="insight-card insight-tip" style="margin-bottom:12px">
                <div class="insight-type">Tip {i}</div>
                <div class="insight-body">{tip}</div>
            </div>""", unsafe_allow_html=True)

    # Category breakdown bar chart
    by_cat = summary.get("by_category", {})
    if by_cat:
        st.markdown("""
        <div style="font-family:var(--font-display); font-size:16px; font-weight:700;
                    color:var(--text-primary); margin:24px 0 14px">📊 Category Breakdown</div>""",
        unsafe_allow_html=True)

        max_val = max(by_cat.values())
        for cat, amt in by_cat.items():
            pct = (amt / max_val) * 100
            icon  = get_icon(cat)
            color = get_color(cat)
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px">
                <div style="width:24px; text-align:center; font-size:16px; flex-shrink:0">{icon}</div>
                <div style="width:90px; font-size:13px; color:var(--text-secondary); flex-shrink:0">{cat}</div>
                <div style="flex:1; background:var(--bg-elevated); border-radius:100px; height:8px; overflow:hidden">
                    <div style="width:{pct}%; height:100%; background:{color}; border-radius:100px;
                                opacity:0.8"></div>
                </div>
                <div style="font-family:var(--font-mono); font-size:13px; color:var(--text-primary);
                            flex-shrink:0; text-align:right; min-width:80px">₹{amt:,.2f}</div>
            </div>""", unsafe_allow_html=True)
