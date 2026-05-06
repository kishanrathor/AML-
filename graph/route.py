def route(state):

    intent = state["intent"]

    routes = {
        "aml":     "claim_agent",    # AML alerts & transaction monitoring
        "account": "policy_agent",   # KYC, account management
        "support": "support_agent",  # General banking support
    }

    for key in routes:
        if key in intent:
            return routes[key]

    return "support_agent"
