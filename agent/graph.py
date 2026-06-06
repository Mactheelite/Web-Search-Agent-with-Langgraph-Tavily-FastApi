from typing import Literal

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode

from agent.config import Settings
from agent.tools import build_tools

SYSTEM_PROMPT = (
    "You are a helpful research assistant. "
    "Use the search_web tool to find current, accurate information. "
    "Use the add tool only for arithmetic. "
    "Be concise and cite sources when possible."
)


def build_llm(settings: Settings) -> BaseChatModel:
    return init_chat_model(
        model=settings.llm_model,
        model_provider="openai",
        api_key=settings.openai_api_key.get_secret_value(),
        temperature=0,
    )


def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    return "__end__"


def build_agent(settings: Settings) -> CompiledStateGraph:
    tools = list(build_tools(settings))
    llm_with_tools = build_llm(settings).bind_tools(tools)

    def call_model(state: MessagesState) -> dict:
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    tools_node = ToolNode(tools)

    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tools_node)
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {"tools": "tools", "__end__": END},
    )
    workflow.add_edge("tools", "agent")
    return workflow.compile()
