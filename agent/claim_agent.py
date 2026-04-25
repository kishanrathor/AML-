from core.llm import get_llm
from rag.retriever import retrieve_context
llm  =   get_llm()

def claim_agent(state):

    query = state["query"]

    docs = retrieve_context(query)

    prompt = f"""
    You are a banking loan specialist assistant.

    Help the customer with loan applications, EMI calculations, loan eligibility, repayment schedules, and loan-related queries.

    Use the knowledge below if available.

    Context:
    {docs}

    Question:
    {query}

    Explain clearly step-by-step.
    """

    response = llm.invoke(prompt)

    state["response"] = response.content

    return state