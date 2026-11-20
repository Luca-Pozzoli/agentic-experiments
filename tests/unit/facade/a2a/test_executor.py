from collections.abc import Callable

import pytest
from a2a.helpers import get_message_text
from a2a.server.agent_execution import RequestContext
from hypothesis import given
from langchain_core.language_models import (
    BaseChatModel,
    ParrotFakeChatModel,
)
from langgraph.graph.state import CompiledStateGraph

from agentic_experiments.facade.a2a.executor import (
    INVALID_MESSAGE_REPLY,
    GraphAgentExecutor,
)
from tests.unit.facade.a2a.conftest import (
    EventQueueFixture,
    async_settings,
    random_invalid_request_context,
    random_valid_request_context,
)


@pytest.mark.asyncio
@async_settings
@given(valid_request_context=random_valid_request_context())
async def test_given_valid_message_expect_model_response(
    graph_factory_fixture: Callable[[BaseChatModel], CompiledStateGraph],
    event_queue_fixture: EventQueueFixture,
    valid_request_context: RequestContext,
) -> None:
    queue = EventQueueFixture()
    executor = GraphAgentExecutor(graph=graph_factory_fixture(ParrotFakeChatModel()))
    expected_message: str = get_message_text(valid_request_context.message).strip()  # ty: ignore[invalid-argument-type]

    await executor.execute(valid_request_context, queue)

    assert [get_message_text(e) for e in queue.get_events()] == [expected_message]


@pytest.mark.asyncio
@async_settings
@given(invalid_request_context=random_invalid_request_context())
async def test_given_invalid_message_then_expect_default_model_response(
    graph_factory_fixture: Callable[[BaseChatModel], CompiledStateGraph],
    event_queue_fixture: EventQueueFixture,
    invalid_request_context: RequestContext,
) -> None:
    executor = GraphAgentExecutor(graph=graph_factory_fixture(ParrotFakeChatModel()))

    await executor.execute(invalid_request_context, event_queue_fixture)

    assert [get_message_text(e) for e in event_queue_fixture.get_events()] == [
        INVALID_MESSAGE_REPLY
    ]
