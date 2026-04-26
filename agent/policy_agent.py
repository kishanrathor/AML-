from core.llm import get_llm
from rag.retriever import retrieve_context
from rag.utils import trim_conversation

llm = get_llm()


def policy_agent(state):
    messages = state.get("messages", [])

    # 🧠 get latest user query
    user_query = messages[-1]["content"]

    # 📚 RAG context
    docs = retrieve_context(user_query)

    # ✂️ apply STM trimming (keep history)
    trimmed = trim_conversation(messages)
    print("trimmed = ", trimmed)

    # 🧾 system prompt with RAG context
    system_prompt = f"""You are a banking account specialist.
Help the customer with account opening, account types, savings accounts, current accounts, fixed deposits, interest rates, and account-related queries.
Use the context below if available.

Context:
{docs}"""

    # 🤖 call LLM with full conversation history
    llm_messages = [{"role": "system", "content": system_prompt}] + trimmed
    response = llm.invoke(llm_messages)

    messages.append({"role": "assistant", "content": response.content})

    return {"messages": messages}
