from langchain_groq import ChatGroq

from rag.retriever import retrieve_context
from rag.prompts import get_rag_prompt
import os
from core.llm  import get_llm
llm  =   get_llm()


def rag_pipeline(query: str):

    # Step 1: Retrieve context
    context = retrieve_context(query)

    # Step 2: Build prompt
    prompt = get_rag_prompt(context, query)

    # Step 3: LLM generate answer
    response = llm.invoke(prompt)
    
    
    print(response.content)

    return response.content

if __name__ == "__main__":
    rag_pipeline("Give me the claim details which details you want for claim")