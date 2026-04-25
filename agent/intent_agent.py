from core.llm import get_llm
llm  =   get_llm()


def detect_intent(state):

    query = state["query"]

    prompt = f"""
    You are an intent classifier for a banking AI system.

    Classify the user's request into one of these intents:

    loan
    account
    support

    User query: {query}

    Return ONLY the intent word, nothing else.
    """

    response = llm.invoke(prompt)

    state["intent"] = response.content.strip().lower()

    return state