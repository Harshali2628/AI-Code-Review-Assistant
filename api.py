from fastapi import FastAPI
from pydantic import BaseModel
from utils.ai_reviewer import review_code

app = FastAPI(
    title="AI Code Review API",
    version="1.0.0"
)

class CodeRequest(BaseModel):
    code: str


@app.get("/")
def home():
    return {"message": "AI Code Review API Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/review")
def review(request: CodeRequest):
    result = review_code(request.code)
    return {"review": result}