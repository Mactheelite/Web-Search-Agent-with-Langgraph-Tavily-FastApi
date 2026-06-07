import logging

from fastapi import APIRouter, HTTPException

from agent.api.dependencies import AgentDep
from agent.schemas import HealthResponse, SearchRequest, SearchResponse
from agent.service import run_search

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@router.post("/search", response_model=SearchResponse)
def search(body: SearchRequest, agent: AgentDep) -> SearchResponse:
    try:
        return run_search(agent, body)
    except Exception:
        logger.exception("Search failed for query: %r", body.query)
        raise HTTPException(status_code=500, detail="Search failed.") from None
