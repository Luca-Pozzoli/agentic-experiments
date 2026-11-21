from collections.abc import Callable

import pytest
from hypothesis import given
from langchain_core.language_models import BaseChatModel, GenericFakeChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langgraph.graph.state import CompiledStateGraph

from tests.unit.facade.a2a.strategy import async_pbt_settings, random_message_list


@pytest.mark.asyncio
@async_pbt_settings
@given(message_list=random_message_list())
async def test_given_chat_history_then_answer_is_appended(
    graph_factory_fixture: Callable[[BaseChatModel], CompiledStateGraph],
    message_list: list[BaseMessage],
):
    model_reply: str = "Hello there!"
    graph: CompiledStateGraph = graph_factory_fixture(
        GenericFakeChatModel(messages=iter([AIMessage(model_reply)]))
    )

    result = await graph.ainvoke({"messages": message_list})

    assert [m.content for m in result["messages"]] == [
        *(m.content for m in message_list),
        model_reply,
    ]
