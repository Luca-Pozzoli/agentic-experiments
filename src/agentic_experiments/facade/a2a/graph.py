from typing import Any

from langchain_core.language_models import BaseChatModel
from langgraph.constants import END, START
from langgraph.graph import MessagesState
from langgraph.graph.state import CompiledStateGraph, StateGraph


def build_graph(model: BaseChatModel) -> CompiledStateGraph:
    async def call_model(state: MessagesState) -> dict[str, Any]:
        return {"messages": [await model.ainvoke(state["messages"])]}

    builder: StateGraph = StateGraph(MessagesState)  # ty: ignore[invalid-argument-type]
    builder.add_node("model", call_model)
    builder.add_edge(START, "model")
    builder.add_edge("model", END)
    return builder.compile()
