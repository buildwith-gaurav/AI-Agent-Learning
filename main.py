from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

from services import ask_gemini

app = FastAPI()




class PromptRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat(user:PromptRequest):
    answer = ask_gemini(user.prompt)

    

    return {
        "response":answer
    }

 
