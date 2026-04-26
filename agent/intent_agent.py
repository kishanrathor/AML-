from core.llm import get_llm

llm = get_llm()


def detect_intent(state):

    messages = state.get("messages", [])

    # 🧠 get latest user message
    user_query = messages[-1]["content"]
    prompt = f"""
You are an intent classifier for a banking AI system.

Classify the user's request into one of these intents:

loan   - for loan, EMI, repayment, credit queries
account - for account opening, savings, FD, interest rate queries
support - for net banking, cards, KYC, disputes, general help

User query: {user_query}

Return ONLY one word:
loan / account / support
"""

    response = llm.invoke(prompt)

    intent = response.content.strip().lower()

    return {
        "intent": intent,
        "messages": messages   # 👈 IMPORTANT (do not lose memory)
    }