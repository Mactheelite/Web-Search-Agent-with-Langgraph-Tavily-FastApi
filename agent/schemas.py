from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SearchRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    query: str = Field(..., min_length=1, max_length=4000, examples=["What is LangGraph?"])


class SearchResponse(BaseModel):
    answer: str = Field(..., description="Answer generated from web search results")


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
