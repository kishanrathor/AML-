from typing import Annotated, List
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    messages: Annotated[List[dict], add_messages]  # LangGraph manages accumulation
    intent: str
    context: str
