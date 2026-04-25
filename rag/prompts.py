def get_rag_prompt(context, query):

    return f"""
You are a banking assistant.

Use ONLY the context below to answer. If the context is insufficient, use your general banking knowledge.

Context:
{context}

Question:
{query}

Answer clearly and professionally.
"""