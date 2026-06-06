import logging
from typing import Sequence

from langchain.tools import BaseTool, tool
from langchain_community.tools import TavilySearchResults

from agent.config import Settings

logger = logging.getLogger(__name__)


def build_tools(settings: Settings) -> Sequence[BaseTool]:
    tavily = TavilySearchResults(
        max_results=settings.tavily_max_results,
        search_depth="basic",
        tavily_api_key=settings.tavily_api_key.get_secret_value(),
    )

    @tool
    def search_web(query: str) -> str:
        """Search the web for current information on a given topic."""
        try:
            return str(tavily.invoke({"query": query}))
        except Exception:
            logger.exception("Web search failed for query: %r", query)
            return "Search is temporarily unavailable."


    return [search_web]
