import os
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.llm.client import ask_llm, parse_triage_response


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


class TriageRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


def load_prompt(text: str) -> str:
    prompt_path = Path("prompts/support-triage-v1.md")
    prompt = prompt_path.read_text(encoding="utf-8")
    return prompt.replace("{text}", text)


@router.post("/triage")
def triage(request: TriageRequest):

    if os.getenv("LLM_ENABLED", "true").lower() != "true":
        raise HTTPException(
            status_code=503,
            detail="LLM feature is disabled"
        )

    prompt = load_prompt(request.text)

    try:
        raw_answer = ask_llm(prompt)
        result = parse_triage_response(raw_answer)
        return result.model_dump()

    except Exception:
        repair_prompt = f"""
The previous LLM response was invalid.

Return ONLY valid JSON with exactly these fields:
{{
  "category": "billing|bug|feature|other",
  "urgency": "low|normal|high",
  "confidence": 0.0,
  "reason": "one short sentence"
}}

The original support message was:
{request.text}

The previous response was:
{raw_answer}

Fix the response so it matches the required schema exactly.
"""

        try:
            repaired_answer = ask_llm(repair_prompt)
            result = parse_triage_response(repaired_answer)
            return result.model_dump()

        except Exception:
            raise HTTPException(
                status_code=422,
                detail="LLM returned invalid structured output after repair"
            )
