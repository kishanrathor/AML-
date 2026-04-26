import os
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

from agent.intent_agent import detect_intent
from agent.policy_agent import policy_agent
from agent.claim_agent import claim_agent
from agent.support_agent import support_agent
from graph.route import route
from graph.state import AgentState

load_dotenv()

DB_URI = os.getenv("DATABASE_URL")

# ── Connection pool (survives Streamlit reruns) ───────────────────────────────
pool = ConnectionPool(
    conninfo=DB_URI,
    max_size=10,
    kwargs={"autocommit": True},
)

# ── Setup tables once ─────────────────────────────────────────────────────────
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()

# ── Checkpointer using pool ───────────────────────────────────────────────────
checkpointer = PostgresSaver(pool)

# ── Build graph ───────────────────────────────────────────────────────────────
workflow = StateGraph(AgentState)

workflow.add_node("intent_agent", detect_intent)
workflow.add_node("policy_agent", policy_agent)
workflow.add_node("claim_agent", claim_agent)
workflow.add_node("support_agent", support_agent)

workflow.set_entry_point("intent_agent")

workflow.add_conditional_edges(
    "intent_agent",
    route,
    {
        "claim_agent": "claim_agent",
        "policy_agent": "policy_agent",
        "support_agent": "support_agent",
    },
)

workflow.add_edge("policy_agent", END)
workflow.add_edge("claim_agent", END)
workflow.add_edge("support_agent", END)

# ── Compile ───────────────────────────────────────────────────────────────────
graph = workflow.compile(checkpointer=checkpointer)
