from fastapi import FastAPI
from api.chat import router as chat_router
from dotenv import load_dotenv
import core.observability 
import os

load_dotenv()  

app = FastAPI(
    title="Banking AI Agent",
    version="1.0"
)

# include routes
app.include_router(chat_router)

@app.get("/")
def home():
    return {"message": "Banking AI Agent Running 🚀"}