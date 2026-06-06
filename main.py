from contextlib import asynccontextmanager

from fastapi import FastAPI

from agent.api.routes import router
from agent.config import get_settings
from agent.service import SearchAgentService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.agent_service = SearchAgentService(get_settings())
    yield


app = FastAPI(title="Search Agent", lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
