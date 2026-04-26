import streamlit as st
from dotenv import load_dotenv

load_dotenv()

import core.observability  # noqa: F401 — must be first to init Opik tracing
from graph.workflow import graph

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Banking AI Assistant",
    page_icon="🏦",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Page background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #e8f0fe 0%, #f0f4f8 100%);
    }
    [data-testid="stSidebar"] {
        background: #1a3c6e;
        color: white;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* Intent badges */
    .intent-badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
        text-transform: uppercase;
    }
    .badge-loan    { background: #dbeafe; color: #1d4ed8; }
    .badge-account { background: #dcfce7; color: #15803d; }
    .badge-support { background: #fef9c3; color: #a16207; }

    /* Chat bubbles */
    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 4px 8px;
    }

    /* Title */
    h1 { color: #1a3c6e !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bank-building.png", width=72)
    st.title("Banking AI")
    st.markdown("---")
    st.markdown("### How can I help?")
    st.markdown("""
- 💳 **Loan queries** — eligibility, EMI, repayment
- 🏦 **Account queries** — savings, FD, interest rates
- 🛎 **Support** — net banking, cards, KYC
    """)
    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(__import__("uuid").uuid4())
        st.rerun()

    st.markdown("---")
    st.caption("Powered by LangGraph + Groq LLM")

# ── Main area ─────────────────────────────────────────────────────────────────
st.title("🏦 Banking AI Assistant")
st.caption("Your intelligent banking companion — ask about loans, accounts, or get support.")
st.markdown("---")

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    import uuid
    st.session_state.thread_id = str(uuid.uuid4())

# ── Welcome message ───────────────────────────────────────────────────────────
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("👋 Hello! I'm your Banking AI Assistant. How can I help you today?")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("💳 **Loan**\nAsk about home loans, personal loans, EMI")
        with col2:
            st.success("🏦 **Account**\nSavings, current, FD, interest rates")
        with col3:
            st.warning("🛎 **Support**\nNet banking, cards, KYC, disputes")

# ── Render chat history ───────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and msg.get("intent"):
            intent = msg["intent"]
            label = {"loan": "💳 Loan", "account": "🏦 Account", "support": "🛎 Support"}.get(intent, intent.title())
            st.markdown(
                f'<span class="intent-badge badge-{intent}">{label}</span>',
                unsafe_allow_html=True,
            )
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask your banking question here..."):

    # show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing your query..."):

            config = {
                "configurable": {
                    "thread_id": st.session_state.thread_id
                }
            }

            result = graph.invoke(
                {
                    "messages": st.session_state.messages
                },
                config
            )

        # 🧠 extract response
        response = result["messages"][-1]["content"]

        # 🧠 extract intent (if exists)
        intent = result.get("intent", "support").strip().lower()

        # normalize intent
        for key in ["loan", "account", "support"]:
            if key in intent:
                intent = key
                break

        label = {
            "loan": "💳 Loan",
            "account": "🏦 Account",
            "support": "🛎 Support"
        }.get(intent, intent.title())

        st.markdown(
            f'<span class="intent-badge badge-{intent}">{label}</span>',
            unsafe_allow_html=True,
        )

        st.markdown(response)

    # save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "intent": intent,
    })