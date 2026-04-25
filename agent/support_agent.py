from core.llm import get_llm
from rag.retriever import retrieve_context

llm  =   get_llm()
def support_agent(state):

    query = state["query"]

    docs = retrieve_context(query)

    prompt = f"""
    You are a helpful banking customer support assistant.

    Help customers with general banking queries such as net banking, card issues, transaction disputes, KYC, branch/ATM locator, and general banking services.

    Use the knowledge below to answer.

    Context:
    {docs}

    Question:
    {query}

    Be polite, clear, and concise.
    """

    response = llm.invoke(prompt)

    state["response"] = response.content

    return state