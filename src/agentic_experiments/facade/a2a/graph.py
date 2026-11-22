from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_openai.chat_models.base import BaseChatOpenAI, ChatOpenAI
from langgraph.constants import END, START
from langgraph.graph import MessagesState
from langgraph.graph.state import CompiledStateGraph, StateGraph

from config import LLMConfig, LLMProviderKind, OpenAICompatibleModelConfig


def build_graph(model: BaseChatModel) -> CompiledStateGraph:
    async def call_model(state: MessagesState) -> dict[str, Any]:
        return {"messages": [await model.ainvoke(state["messages"])]}

    builder: StateGraph = StateGraph(MessagesState)  # ty: ignore[invalid-argument-type]
    builder.add_node("model", call_model)
    builder.add_edge(START, "model")
    builder.add_edge("model", END)
    return builder.compile()


def get_compiled_graph(llm_config: LLMConfig) -> CompiledStateGraph:
    match llm_config.kind:
        case LLMProviderKind.OpenAICompatible:
            return build_graph(_build_openai_compatible_model(llm_config))


def _build_openai_compatible_model(
    config: OpenAICompatibleModelConfig,
) -> BaseChatOpenAI:
    return ChatOpenAI(
        base_url=str(config.url),
        api_key=config.api_key,
        model=config.model,
        extra_body={"reasoning_effort": "none"},
    )
