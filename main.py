from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

from services import ask_gemini

app = FastAPI()

# @app.get("/")
# def home():
#     return{"message: Hello AI Agent Developer "}


class PromptRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat(user:PromptRequest):
    answer = ask_gemini(user.prompt)

    

    return {
        "response":answer
    }

 
