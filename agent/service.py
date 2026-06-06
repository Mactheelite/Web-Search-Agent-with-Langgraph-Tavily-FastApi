import json
from collections.abc import AsyncIterator

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph.state import CompiledStateGraph

from agent.config import Settings
from agent.graph import SYSTEM_PROMPT, build_agent


def _escape_json_chunk(text: str) -> str:
    return json.dumps(text, ensure_ascii=False)[1:-1]


class SearchAgentService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._agent: CompiledStateGraph = build_agent(settings)

    @property
    def settings(self) -> Settings:
        return self._settings

    async def stream_search(self, query: str) -> AsyncIterator[str]:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=query),
        ]

        yield '{"answer": "'

        async for message, metadata in self._agent.astream(
            {"messages": messages},
            stream_mode="messages",
        ):
            if metadata.get("langgraph_node") != "agent":
                continue
            if not message.content:
                continue
            if message.tool_calls or getattr(message, "tool_call_chunks", None):
                continue

            yield _escape_json_chunk(message.content)

        yield '"}'
