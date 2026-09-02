from fastapi import FastAPI
from pydantic import BaseModel

from services import run_prompt

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str


class AgentResponse(BaseModel):
    response: dict | str
    memory_context: str


@app.post("/chat", response_model=AgentResponse)
def chat(user: PromptRequest):

    result = run_prompt(user.prompt)

    return result