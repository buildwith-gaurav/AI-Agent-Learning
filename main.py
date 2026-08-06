from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return{"message: Hello AI Agent Developer "}


class loginrequest(BaseModel):
    email:str
    password:str

@app.post("/login")
def login(user:loginrequest):
    if user.email != "admin@gmail.com":
        raise HTTPException(
            status_code=401,
            detail="invalid email"
        )

    if user.password != "123456":
        raise HTTPException(
            status_code=401,
            detail="invalid password"
        )

    return {
        "message":"login sucessfully"
    }

 
