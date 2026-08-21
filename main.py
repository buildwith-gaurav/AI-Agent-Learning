from fastapi import FastAPI
from pydantic import BaseModel

from services import run_prompt

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str


@app.post("/chat")
def chat(user: PromptRequest):

    result = run_prompt(user.prompt)

    return {
        "response": str(result)
    }
