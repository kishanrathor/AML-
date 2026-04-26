from typing import List, TypedDict
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    messages: List[BaseMessage]   # 👈 MAIN memory
    intent: str                   # routing
    context: str                  # RAG context (optional)