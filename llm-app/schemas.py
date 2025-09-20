from typing import Optional

from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    model: Optional[str] = "gpt-4o-mini"
    temperature: Optional[float] = 0.0


class LLMResponse(BaseModel):
    text: str
    model: str
    duration: float
    tokens: Optional[int] = None
