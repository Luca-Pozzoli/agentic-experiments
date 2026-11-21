import string
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Final

import pytest
from a2a.helpers import new_text_message
from a2a.server.agent_execution import RequestContext
from a2a.server.context import ServerCallContext
from a2a.server.events import EventQueue
from a2a.types import Role, SendMessageRequest
from hypothesis import HealthCheck, settings, strategies
from hypothesis.strategies import DrawFn, SearchStrategy
from langchain_core.language_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph

from agentic_experiments.facade.a2a.graph import build_graph

type InvalidTextMessage = str | None

async_settings = settings(
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)

WHITESPACE_CHARS: Final[str] = " \t\n\r\x0b\x0c"
SINGLE_WORD_STRATEGY: Final[SearchStrategy[str]] = strategies.text(
    alphabet=string.ascii_letters, min_size=1, max_size=12
)


@strategies.composite
def random_valid_message(draw: DrawFn) -> str:
    words = draw(strategies.lists(SINGLE_WORD_STRATEGY, min_size=1, max_size=10))
    separators = draw(
        strategies.lists(
            strategies.text(alphabet=WHITESPACE_CHARS, min_size=1, max_size=4),
            min_size=len(words) - 1,
            max_size=len(words) - 1,
        )
    )
    leading = draw(strategies.text(alphabet=WHITESPACE_CHARS, max_size=4))
    trailing = draw(strategies.text(alphabet=WHITESPACE_CHARS, max_size=4))

    body = words[0] + "".join(sep + word for sep, word in zip(separators, words[1:]))
    return leading + body + trailing


@strategies.composite
def random_invalid_message(draw: DrawFn) -> InvalidTextMessage:
    return draw(
        strategies.just(None),
        strategies.text(
            alphabet=strategies.one_of(
                strategies.characters(categories=["Zs"]),
                strategies.sampled_from("\t\n\r\x0b\x0c"),
            )
        ),
    )


@strategies.composite
def random_valid_request_context(draw: DrawFn) -> RequestContext:
    return _make_context(draw(random_valid_message()))


@strategies.composite
def random_invalid_request_context(draw: DrawFn) -> RequestContext:
    return _make_context(draw(random_invalid_message()))


@dataclass
class EventQueueFixture(EventQueue):
    events: list = field(default_factory=list)

    async def enqueue_event(self, event) -> None:
        self.events.append(event)

    def get_events(self) -> list:
        return self.events


@pytest.fixture(scope="session")
def graph_factory_fixture() -> Callable[[BaseChatModel], CompiledStateGraph]:
    return build_graph


@pytest.fixture(scope="session")
def event_queue_factory_fixture() -> Callable[[], EventQueueFixture]:
    return EventQueueFixture


def _make_context(text: str | None) -> RequestContext:
    request = None
    if text is not None:
        message = new_text_message(text, role=Role.ROLE_USER)
        request = SendMessageRequest(message=message)
    return RequestContext(call_context=ServerCallContext(), request=request)
