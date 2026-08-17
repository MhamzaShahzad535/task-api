from fastapi import APIRouter
from pydantic import BaseModel

from src.llm.client import ask_llm


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


class AIRequest(BaseModel):
    prompt: str


@router.post("/ask")
def ask_ai(request: AIRequest):
    answer = ask_llm(request.prompt)

    return {
        "prompt": request.prompt,
        "answer": answer
    }