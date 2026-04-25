"""
Global CSS theme — Refined dark fintech aesthetic
Fonts: DM Sans (body) + Syne (display)
"""

import streamlit as st

def inject_global_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=DM+Mono:wght@400;500&display=swap');

    /* ── Root Variables ────────────────────────────── */
    :root {
        --bg-deep:        #0a0d14;
        --bg-card:        #111520;
        --bg-elevated:    #171d2e;
        --bg-glass:       rgba(255,255,255,0.04);
        --border:         rgba(255,255,255,0.07);
        --border-active:  rgba(99,179,237,0.4);
        --accent-blue:    #63b3ed;
        --accent-cyan:    #4ecdc4;
        --accent-gold:    #f6c90e;
        --accent-red:     #fc6d6d;
        --accent-green:   #56cfae;
        --accent-purple:  #a78bfa;
        --text-primary:   #eef2f7;
        --text-secondary: #8b93a7;
        --text-muted:     #525d73;
        --font-display:   'Syne', sans-serif;
        --font-body:      'DM Sans', sans-serif;
        --font-mono:      'DM Mono', monospace;
        --radius-sm:      8px;
        --radius-md:      14px;
        --radius-lg:      20px;
        --shadow-card:    0 4px 32px rgba(0,0,0,0.4);
        --shadow-glow:    0 0 24px rgba(99,179,237,0.15);
    }

    /* ── Base Reset ────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: var(--font-body) !important;
        background-color: var(--bg-deep) !important;
        color: var(--text-primary) !important;
    }

    .stApp {
        background: var(--bg-deep) !important;
        background-image:
            radial-gradient(ellipse 60% 40% at 80% 10%, rgba(99,179,237,0.06) 0%, transparent 60%),
            radial-gradient(ellipse 40% 30% at 10% 80%, rgba(78,205,196,0.05) 0%, transparent 50%);
        min-height: 100vh;
    }

    /* ── Sidebar ───────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: var(--bg-card) !important;
        border-right: 1px solid var(--border) !important;
        padding-top: 0 !important;
    }
    section[data-testid="stSidebar"] > div {
        padding: 0 !important;
    }
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 24px 20px 20px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 16px;
    }
    .brand-icon { font-size: 24px; }
    .brand-name {
        font-family: var(--font-display);
        font-size: 18px;
        font-weight: 700;
        color: var(--text-primary);
    }
    .brand-ai {
        font-family: var(--font-mono);
        font-size: 10px;
        font-weight: 500;
        color: var(--accent-blue);
        background: rgba(99,179,237,0.12);
        border: 1px solid rgba(99,179,237,0.25);
        border-radius: 4px;
        padding: 2px 6px;
        letter-spacing: 0.05em;
    }
    .user-pill {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 20px;
        margin: 0 12px 16px;
        background: var(--bg-glass);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
    }
    .user-avatar {
        width: 30px;
        height: 30px;
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: var(--font-display);
        font-weight: 700;
        font-size: 13px;
        color: var(--bg-deep);
        flex-shrink: 0;
        line-height: 30px;
        text-align: center;
    }
    .user-email {
        font-size: 12px;
        color: var(--text-secondary);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .nav-label {
        font-family: var(--font-mono);
        font-size: 10px;
        letter-spacing: 0.12em;
        color: var(--text-muted);
        padding: 0 20px 8px;
        text-transform: uppercase;
    }
    .sidebar-spacer { flex: 1; min-height: 40px; }

    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        border: none !important;
        color: var(--text-secondary) !important;
        font-family: var(--font-body) !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        text-align: left !important;
        padding: 10px 20px !important;
        border-radius: var(--radius-sm) !important;
        margin: 2px 12px !important;
        width: calc(100% - 24px) !important;
        transition: all 0.15s ease !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: var(--bg-glass) !important;
        color: var(--text-primary) !important;
    }
    section[data-testid="stSidebar"] .stButton:last-child button {
        color: var(--accent-red) !important;
        margin-top: 8px !important;
    }

    /* ── Main content area ─────────────────────────── */
    .main .block-container {
        padding: 32px 40px !important;
        max-width: 1200px !important;
    }

    /* ── Page headings ─────────────────────────────── */
    .page-header {
        margin-bottom: 32px;
    }
    .page-title {
        font-family: var(--font-display);
        font-size: 28px;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.2;
        margin: 0 0 6px;
    }
    .page-subtitle {
        font-size: 14px;
        color: var(--text-secondary);
        margin: 0;
    }

    /* ── Cards ─────────────────────────────────────── */
    .stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 22px 24px;
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s ease;
    }
    .stat-card:hover { border-color: var(--border-active); }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent-color, var(--accent-blue)), transparent);
        opacity: 0.6;
    }
    .stat-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 10px;
        font-family: var(--font-mono);
    }
    .stat-value {
        font-family: var(--font-display);
        font-size: 30px;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1;
        margin-bottom: 6px;
    }
    .stat-meta {
        font-size: 12px;
        color: var(--text-secondary);
    }
    .stat-icon {
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 22px;
        opacity: 0.6;
    }

    /* ── AI Insight Card ───────────────────────────── */
    .insight-card {
        background: linear-gradient(135deg, rgba(99,179,237,0.06), rgba(78,205,196,0.04));
        border: 1px solid rgba(99,179,237,0.2);
        border-radius: var(--radius-lg);
        padding: 24px;
        margin-bottom: 16px;
        position: relative;
    }
    .insight-card .insight-type {
        font-family: var(--font-mono);
        font-size: 10px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 3px 8px;
        border-radius: 4px;
        display: inline-block;
        margin-bottom: 10px;
        font-weight: 500;
    }
    .insight-card .insight-body {
        font-size: 15px;
        line-height: 1.6;
        color: var(--text-primary);
    }
    .insight-warning { border-color: rgba(252,109,109,0.3) !important; background: linear-gradient(135deg, rgba(252,109,109,0.05), rgba(246,201,14,0.03)) !important; }
    .insight-warning .insight-type { background: rgba(252,109,109,0.15); color: var(--accent-red); }
    .insight-tip { border-color: rgba(86,207,174,0.25) !important; }
    .insight-tip .insight-type { background: rgba(86,207,174,0.12); color: var(--accent-green); }
    .insight-summary .insight-type { background: rgba(99,179,237,0.12); color: var(--accent-blue); }

    /* ── Transaction rows ──────────────────────────── */
    .txn-row {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 14px 0;
        border-bottom: 1px solid var(--border);
    }
    .txn-row:last-child { border-bottom: none; }
    .txn-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
    }
    .txn-info { flex: 1; min-width: 0; }
    .txn-desc {
        font-size: 14px;
        font-weight: 500;
        color: var(--text-primary);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .txn-cat {
        font-size: 12px;
        color: var(--text-muted);
        margin-top: 2px;
    }
    .txn-amount {
        font-family: var(--font-mono);
        font-size: 15px;
        font-weight: 500;
        color: var(--accent-red);
        flex-shrink: 0;
    }
    .txn-date {
        font-size: 11px;
        color: var(--text-muted);
        flex-shrink: 0;
    }

    /* ── Forms ─────────────────────────────────────── */
    .stTextInput input, .stNumberInput input, .stSelectbox select, .stTextArea textarea {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-family: var(--font-body) !important;
        font-size: 14px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(99,179,237,0.1) !important;
    }
    label, .stTextInput label, .stSelectbox label, .stNumberInput label {
        color: var(--text-secondary) !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        font-family: var(--font-body) !important;
    }

    /* Primary button */
    .stButton button[kind="primary"], button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan)) !important;
        color: var(--bg-deep) !important;
        border: none !important;
        font-family: var(--font-body) !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        border-radius: var(--radius-sm) !important;
        padding: 10px 24px !important;
        transition: opacity 0.2s !important;
    }
    .stButton button[kind="primary"]:hover { opacity: 0.88 !important; }

    /* ── Alerts ────────────────────────────────────── */
    .stSuccess > div {
        background: rgba(86,207,174,0.1) !important;
        border: 1px solid rgba(86,207,174,0.3) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--accent-green) !important;
    }
    .stError > div {
        background: rgba(252,109,109,0.1) !important;
        border: 1px solid rgba(252,109,109,0.3) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--accent-red) !important;
    }
    .stWarning > div {
        background: rgba(246,201,14,0.1) !important;
        border: 1px solid rgba(246,201,14,0.3) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--accent-gold) !important;
    }
    .stInfo > div {
        background: rgba(99,179,237,0.08) !important;
        border: 1px solid rgba(99,179,237,0.2) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--accent-blue) !important;
    }

    /* ── Dividers & misc ───────────────────────────── */
    hr { border-color: var(--border) !important; }
    .stSpinner > div { border-top-color: var(--accent-blue) !important; }
    .stProgress > div > div { background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan)) !important; }
    [data-testid="stMetricValue"] {
        font-family: var(--font-display) !important;
        font-weight: 800 !important;
        color: var(--text-primary) !important;
    }

    /* ── Auth page ─────────────────────────────────── */
    .auth-container {
        max-width: 420px;
        margin: 60px auto 0;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 40px 36px;
        box-shadow: var(--shadow-card), var(--shadow-glow);
    }
    .auth-logo {
        text-align: center;
        margin-bottom: 28px;
    }
    .auth-logo-icon { font-size: 40px; display: block; margin-bottom: 8px; }
    .auth-logo-title {
        font-family: var(--font-display);
        font-size: 24px;
        font-weight: 800;
        color: var(--text-primary);
    }
    .auth-logo-sub {
        font-size: 13px;
        color: var(--text-secondary);
        margin-top: 4px;
    }

    /* ── Section headers ───────────────────────────── */
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
    }
    .section-title {
        font-family: var(--font-display);
        font-size: 16px;
        font-weight: 700;
        color: var(--text-primary);
    }

    /* ── Category badge ────────────────────────────── */
    .cat-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }

    /* ── Loading ───────────────────────────────────── */
    .ai-loading {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 20px;
        color: var(--text-secondary);
        font-size: 14px;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-deep); }
    ::-webkit-scrollbar-thumb { background: var(--bg-elevated); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
    </style>
    """, unsafe_allow_html=True)
