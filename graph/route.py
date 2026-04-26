def route(state):

    intent = state["intent"]

    routes = {
        "loan": "claim_agent",
        "account": "policy_agent",
        "support": "support_agent"
    }

    # fallback: partial match
    for key in routes:
        if key in intent:
            return routes[key]

    return "support_agent"
