import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from agent.api.dependencies import AgentServiceDep
from agent.schemas import HealthResponse, SearchRequest

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@router.post("/search")
async def search(body: SearchRequest, service: AgentServiceDep) -> StreamingResponse:
    try:
        return StreamingResponse(
            service.stream_search(body.query),
            media_type="application/json",
        )
    except Exception:
        logger.exception("Search failed for query: %r", body.query)
        raise HTTPException(status_code=500, detail="Search failed.") from None
