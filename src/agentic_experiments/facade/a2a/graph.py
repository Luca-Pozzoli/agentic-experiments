from typing import Any, Final

from langchain_core.language_models import BaseChatModel
from langchain_openai.chat_models.base import BaseChatOpenAI, ChatOpenAI
from langgraph.constants import END, START
from langgraph.graph import MessagesState
from langgraph.graph.state import CompiledStateGraph, StateGraph

# TODO inject config values
local_llm: Final[BaseChatOpenAI] = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="EMPTY",
    model="Qwen3.5:2b",
    extra_body={"reasoning_effort": "none"},
)


def build_graph(model: BaseChatModel) -> CompiledStateGraph:
    async def call_model(state: MessagesState) -> dict[str, Any]:
        return {"messages": [await model.ainvoke(state["messages"])]}

    builder: StateGraph = StateGraph(MessagesState)  # ty: ignore[invalid-argument-type]
    builder.add_node("model", call_model)
    builder.add_edge(START, "model")
    builder.add_edge("model", END)
    return builder.compile()


def get_compiled_graph() -> CompiledStateGraph:
    return build_graph(local_llm)
