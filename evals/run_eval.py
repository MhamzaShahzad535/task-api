import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json

from src.routers.ai import load_prompt
from src.llm.client import ask_llm, parse_triage_response


with open("evals/cases.json", encoding="utf-8") as f:
    cases = json.load(f)


correct = 0


for i, case in enumerate(cases, 1):

    prompt = load_prompt(case["text"])

    try:
        raw = ask_llm(prompt)

        try:
            result = parse_triage_response(raw)

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

Original support message:
{case["text"]}

Previous invalid response:
{raw}

Fix the response so it matches the required schema exactly.
"""

            repaired = ask_llm(repair_prompt)
            result = parse_triage_response(repaired)

        category_ok = result.category == case["expected"]["category"]
        urgency_ok = result.urgency == case["expected"]["urgency"]

        passed = category_ok and urgency_ok

        if passed:
            correct += 1

        print(
            f"Case {i}: "
            f"{'PASS' if passed else 'FAIL'} "
            f"category={result.category} "
            f"urgency={result.urgency}"
        )

    except Exception as e:
        print(f"Case {i}: FAIL {e}")


score = correct / len(cases) * 100

print()
print(f"Evaluation score: {correct}/{len(cases)} = {score:.0f}%")
