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

@app.get("/login")
def login():
    return {"message" : "login sucessfully"}

class loginrequest(BaseModel):
    email:str
    password:str

@app.post("/login")
def login(user:loginrequest):
    return {
        "message":"login sucessfully",
        "email": user.email
    }

 
