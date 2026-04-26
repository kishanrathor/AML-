import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from opik.integrations.langchain import OpikTracer

load_dotenv()

# Shared tracer instance (reused across all agents)
opik_tracer = OpikTracer(
    project_name=os.getenv("COMET_PROJECT_NAME", "banking-ai"),
    tags=["langgraph", "groq"],
)


def get_llm():
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0.2,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        callbacks=[opik_tracer],
    )
    return llm
