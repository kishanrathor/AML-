from fastapi import APIRouter
from pydantic import BaseModel
from graph.workflow import graph
from opik import track

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    query: str


@router.post("/")
@track(name="groq-llm-call")
def chat(request: ChatRequest):

    query = request.query

    result = graph.invoke({
        "query": query,
        "intent": "",
        "response": ""
    })

    return {
        "response": result["response"]
    }