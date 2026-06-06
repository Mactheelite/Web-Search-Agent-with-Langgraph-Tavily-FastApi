from typing import Annotated

from fastapi import Depends, Request

from agent.service import SearchAgentService


def get_agent_service(request: Request) -> SearchAgentService:
    return request.app.state.agent_service


AgentServiceDep = Annotated[SearchAgentService, Depends(get_agent_service)]
