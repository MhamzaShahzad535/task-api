import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from src.llm.schema import TriageResult
from src.llm.cost import log_cost


load_dotenv()


client = OpenAI(
    base_url=os.environ["LLM_BASE_URL"],
    api_key=os.environ["LLM_API_KEY"],
    timeout=10.0,
    max_retries=2,
)


def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=os.environ["LLM_MODEL"],
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )

    log_cost(
        model=os.environ["LLM_MODEL"],
        prompt_tokens=getattr(response.usage, "prompt_tokens", None),
        completion_tokens=getattr(response.usage, "completion_tokens", None),
        total_tokens=getattr(response.usage, "total_tokens", None),
    )

    return response.choices[0].message.content


def parse_triage_response(raw: str) -> TriageResult:
    data = json.loads(raw)
    return TriageResult.model_validate(data)