
#uvicorn backend.main:app --reload
#--reload hace que el servidor se reinicie automáticamente
#cada vez que guardás un archivo
#muy útil mientras desarrollás
from dotenv import load_dotenv
import os
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

import sys
sys.path.append("..")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import runAgent, buildSystemPrompt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    messages: list

@app.post("/chat")
def chat(request: ChatRequest):
    messages = request.messages

    if not messages or messages[0].get("role") != "system":
        messages.insert(0, {"role": "system", "content": buildSystemPrompt()})

    response = runAgent(messages)
    return { "response": response }