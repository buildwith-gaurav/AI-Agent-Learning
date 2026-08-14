from fastapi import FastAPI
from pydantic import BaseModel

from services import (
    extract_city,
    extract_task,
    extract_calculation,
    execute_task,
)

app = FastAPI()



class PromptRequest(BaseModel):
    prompt: str


@app.post("/chat")
def chat(user: PromptRequest):

    city = extract_city(user.prompt)
    task = extract_task(user.prompt)
    calculation = extract_calculation(user.prompt)

    if city is None and calculation is None:
        return {
            "response": "I couldn't understand the request."
        }

    result = execute_task(
        city=city,
        task=task,
        calculation=calculation
    )

    return {
        "response": str(result)
    }
