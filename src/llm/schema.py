from typing import Literal

from pydantic import BaseModel, Field


class TriageResult(BaseModel):
    category: Literal["billing", "bug", "feature", "other"]
    urgency: Literal["low", "normal", "high"]
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str
