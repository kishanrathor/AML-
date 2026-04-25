from core.llm import get_llm
from rag.retriever import retrieve_context
llm  =   get_llm()


def policy_agent(state):

    query = state["query"]

    docs = retrieve_context(query)

    prompt = f"""
    You are a banking account specialist.

    Help the customer with account opening, account types, savings accounts, current accounts, fixed deposits, interest rates, and account-related queries.

    Use the context below if available.

    Context:
    {docs}

    Question:
    {query}

    Provide accurate and helpful banking information.
    """

    response = llm.invoke(prompt)

    state["response"] = response.content

    return state