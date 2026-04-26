from core.llm import get_llm
from rag.retriever import retrieve_context
from rag.utils import trim_conversation   # your trimming function

llm = get_llm()


def claim_agent(state):

    messages = state.get("messages", [])

    user_query = messages[-1]["content"]

  
    docs = retrieve_context(user_query)

   
    trimmed = trim_conversation(messages)
    print("trimmed = ", trimmed)

    # 🧾 system prompt with RAG context
    system_prompt = f"""You are a vehicle insurance claim assistant.
Help the user with claim process, required documents, claim status, and steps.
Use the context below if relevant.

Context:
{docs}"""

    # 🤖 call LLM with full conversation history
    llm_messages = [{"role": "system", "content": system_prompt}] + trimmed
    response = llm.invoke(llm_messages)

    # 🔥 append to full messages (not trimmed)
    messages.append({"role": "assistant", "content": response.content})

    return {"messages": messages}