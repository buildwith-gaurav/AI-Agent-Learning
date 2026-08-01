from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return{"message: Hello AI Agent Developer "}

@app.get("/about")
def about():
    return {
        {"message: AI Agent Learning"},
        {"day":2},
        {"developer":"buildwith-gaurav"}
    }
 
