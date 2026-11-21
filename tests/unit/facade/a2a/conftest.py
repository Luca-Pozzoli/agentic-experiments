from collections.abc import Callable, Iterator
from dataclasses import dataclass, field

import pytest
from a2a.server.events import Event, EventQueue
from a2a.types import Message, Role
from langchain_core.language_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph

from agentic_experiments.facade.a2a.graph import build_graph


@dataclass
class SimpleQueue(EventQueue):
    events: list[Event] = field(default_factory=list)

    async def enqueue_event(self, event: Event) -> None:
        self.events.append(event)

    def get_events(self) -> list[Event]:
        return self.events

    def get_agent_messages(self) -> list[Message]:
        return [
            event
            for event in self.events
            if isinstance(event, Message) and event.role == Role.ROLE_AGENT
        ]


@pytest.fixture(scope="session")
def graph_factory_fixture() -> Iterator[Callable[[BaseChatModel], CompiledStateGraph]]:
    yield build_graph


@pytest.fixture(scope="session")
def event_queue_factory_fixture() -> Iterator[Callable[[], SimpleQueue]]:
    yield SimpleQueue
