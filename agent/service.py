from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph.state import CompiledStateGraph

from agent.config import Settings
from agent.graph import SYSTEM_PROMPT, build_agent
from agent.schemas import SearchRequest, SearchResponse


def create_agent(settings: Settings) -> CompiledStateGraph:
    return build_agent(settings)


def run_search(agent: CompiledStateGraph, request: SearchRequest) -> SearchResponse:
    result = agent.invoke(
        {
            "messages": [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=request.query),
            ]
        }
    )
    return SearchResponse(answer=result["messages"][-1].content)
