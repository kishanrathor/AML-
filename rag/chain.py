from rag.retriever import retrieve_context
from rag.prompts import get_rag_prompt
from rag.utils import trim_conversation
from core.llm import get_llm

llm = get_llm()


def rag_pipeline(state):

    messages = state.get("messages", [])

    user_query = messages[-1].content

    
    messages = trim_conversation(messages)

   
    context = retrieve_context(user_query)

   
    prompt = get_rag_prompt(context, user_query)

    response = llm.invoke(messages + [{"role": "system", "content": prompt}])


    messages.append(response)

    return {
        "messages": messages
    }