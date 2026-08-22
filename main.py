from fastapi import FastAPI
from pydantic import BaseModel

from services import run_prompt

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str

class AgentResponse(BaseModel):
    city: str | None = None
    temperature: float | None = None
    calculation: int | None = None
    final_result: int | None = None    


@app.post("/chat", response_model=AgentResponse)
def chat(user: PromptRequest):

    result = run_prompt(user.prompt)

    return result
