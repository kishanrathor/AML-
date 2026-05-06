import streamlit as st
from dotenv import load_dotenv

load_dotenv()

import core.observability  # noqa: F401
from graph.workflow import graph

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AML Banking Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"],
[data-testid="stMain"] { background: #f8fafc; }

[data-testid="stHeader"] { display: none; }

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 860px !important;
}

[data-testid="stSidebar"] {
    background: #1e293b;
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] hr { border-color: #334155 !important; }

.stButton > button {
    background: #334155 !important;
    color: #e2e8f0 !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: #475569 !important;
    border-color: #64748b !important;
}

[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 2px 0 !important;
}

.intent-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.badge-aml     { background: #fee2e2; color: #dc2626; }
.badge-account { background: #dbeafe; color: #1d4ed8; }
.badge-support { background: #fef9c3; color: #b45309; }

[data-testid="stChatInput"] textarea {
    color: #000000 !important;
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    font-size: 0.9rem !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #94a3b8 !important; }
[data-testid="stChatInput"] {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    import uuid
    st.session_state.thread_id = str(uuid.uuid4())

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:8px 0 20px 0;">
        <div style="font-size:1.6rem;margin-bottom:6px;">🛡️</div>
        <div style="font-size:1rem;font-weight:700;color:#f1f5f9;">AML Banking AI</div>
        <div style="font-size:0.75rem;color:#94a3b8;margin-top:2px;">Compliance Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown('<p style="font-size:0.7rem;color:#64748b;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:10px;">Capabilities</p>', unsafe_allow_html=True)

    for icon, title, desc in [
        ("🚨", "AML Alerts",    "Suspicious activity, risk scores, SAR"),
        ("🏦", "KYC & Accounts","Verification, freeze, PEP checks"),
        ("🔍", "Transactions",  "Monitoring, patterns, investigation"),
        ("📋", "Compliance",    "PMLA, FATF, reporting guidelines"),
        ("🛎", "Support",       "Helpdesk, officer guidance"),
    ]:
        st.markdown(f"""
        <div style="display:flex;gap:10px;padding:8px 0;border-bottom:1px solid #334155;">
            <span style="font-size:1rem;">{icon}</span>
            <div>
                <div style="font-size:0.8rem;font-weight:600;color:#cbd5e1;">{title}</div>
                <div style="font-size:0.7rem;color:#64748b;">{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;padding:4px 0;margin-bottom:12px;">
        <span style="font-size:0.75rem;color:#64748b;">Messages</span>
        <span style="font-size:0.75rem;font-weight:600;color:#94a3b8;">{len(st.session_state.messages)}</span>
    </div>""", unsafe_allow_html=True)

    if st.button("🗑️  Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(__import__("uuid").uuid4())
        st.rerun()

    st.markdown('<div style="margin-top:20px;text-align:center;font-size:0.65rem;color:#475569;">LangGraph · Groq · Opik</div>', unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#1e293b;border-radius:14px;padding:20px 28px;margin-bottom:24px;display:flex;align-items:center;gap:16px;">
    <div style="font-size:2rem;">🛡️</div>
    <div>
        <div style="font-size:1.3rem;font-weight:700;color:#f1f5f9;">AML Banking Assistant</div>
        <div style="font-size:0.8rem;color:#94a3b8;margin-top:3px;">
            <span style="display:inline-block;width:7px;height:7px;background:#22c55e;border-radius:50%;margin-right:5px;vertical-align:middle;"></span>
            Online &middot; Anti-Money Laundering &amp; Compliance Intelligence
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Welcome cards (only when no messages) ────────────────────────────────────
if not st.session_state.messages:
    col1, col2, col3, col4 = st.columns(4)
    for col, icon, title, desc in [
        (col1, "🚨", "AML Alert",    "Check suspicious activity and risk scores"),
        (col2, "📄", "File SAR",     "Suspicious Activity Report guidance"),
        (col3, "🔐", "KYC Status",   "Customer identity verification"),
        (col4, "🔍", "Transaction",  "Investigate unusual patterns"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:16px;text-align:center;height:110px;">
                <div style="font-size:1.4rem;margin-bottom:6px;">{icon}</div>
                <div style="font-size:0.82rem;font-weight:600;color:#1e293b;margin-bottom:4px;">{title}</div>
                <div style="font-size:0.72rem;color:#64748b;line-height:1.4;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div style="text-align:center;padding:28px 0 12px 0;color:#64748b;font-size:0.9rem;">Ask me about AML alerts, KYC verification, transaction monitoring, or compliance guidelines.</div>', unsafe_allow_html=True)

# ── Chat history — single render point ───────────────────────────────────────
ICONS  = {"aml": "🚨", "account": "🏦", "support": "🛎"}
LABELS = {"aml": "AML Alert", "account": "Account", "support": "Support"}

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and msg.get("intent"):
            intent = msg["intent"]
            cls = f"badge-{intent}" if intent in ICONS else "badge-support"
            st.markdown(
                f'<span class="intent-badge {cls}">{ICONS.get(intent, "🛎")} {LABELS.get(intent, intent.title())}</span>',
                unsafe_allow_html=True,
            )
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask about AML alerts, KYC, transactions, or compliance..."):

    # Call graph — only send new user message, checkpointer handles history
    with st.spinner("Analyzing..."):
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        result = graph.invoke(
            {"messages": [{"role": "user", "content": prompt}]},
            config
        )

    response = result["messages"][-1]
    # handle both dict and AIMessage
    response_text = response if isinstance(response, str) else (
        response.get("content") if isinstance(response, dict) else response.content
    )

    intent = result.get("intent", "support").strip().lower()
    for key in ["aml", "account", "support"]:
        if key in intent:
            intent = key
            break

    # Append both to session_state for display — single source of truth
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "intent": intent,
    })
    st.rerun()
