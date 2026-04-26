from core.llm import get_llm
from rag.retriever import retrieve_context
from rag.utils import trim_conversation

llm = get_llm()


def support_agent(state):
    messages = state.get("messages", [])

    # 🧠 get latest user query
    user_query = messages[-1]["content"]

    # 📚 RAG context
    docs = retrieve_context(user_query)

    # ✂️ apply STM trimming (keep history)
    trimmed = trim_conversation(messages)
    print("trimmed = ", trimmed)

    # 🧾 system prompt with RAG context
    system_prompt = f"""You are a helpful banking customer support assistant.
Help customers with general banking queries such as net banking, card issues, transaction disputes, KYC, branch/ATM locator, and general banking services.
Use the knowledge below to answer. Be polite, clear, and concise.

Context:
{docs}"""

    # 🤖 call LLM with full conversation history
    llm_messages = [{"role": "system", "content": system_prompt}] + trimmed
    response = llm.invoke(llm_messages)

    messages.append({"role": "assistant", "content": response.content})

    return {"messages": messages}
