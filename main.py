from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return{"message: Hello AI Agent Developer "}

@app.get("/about")
def about():
    return {
         "project": "AI Agent Learning",
         "day":3,
         "developer":"buildwith-gaurav"
    }

@app.get("/health")
def health():
    return{
        "status": "running",
        "server": "fastapi"
    }



 
