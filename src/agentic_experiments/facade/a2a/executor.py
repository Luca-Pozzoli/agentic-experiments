from dataclasses import dataclass
from typing import Any, Final

from a2a.helpers import get_message_text, new_text_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import Message
from langgraph.graph.state import CompiledStateGraph
from returns.future import FutureResult, FutureSuccess
from returns.result import Failure, Result, Success

INVALID_MESSAGE_REPLY: Final[str] = "Please provide a valid message"


@dataclass
class GraphAgentExecutor(AgentExecutor):
    graph: CompiledStateGraph

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        await (
            FutureResult.from_result(self._get_message(context))
            .bind_result(self._get_query)
            .bind_awaitable(self._ask_graph)
            .lash(FutureSuccess)
            .map(new_text_message)
            .bind_awaitable(event_queue.enqueue_event)
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        pass

    @staticmethod
    def _get_message(context: RequestContext) -> Result[Message, str]:
        message: Message | None = context.message
        if message is None:
            return Failure(INVALID_MESSAGE_REPLY)
        return Success(message)

    @staticmethod
    def _get_query(message: Message) -> Result[str, str]:
        query: str = get_message_text(message).strip()
        if not query:
            return Failure(INVALID_MESSAGE_REPLY)
        return Success(query)

    async def _ask_graph(self, query: str) -> str:
        result: dict[str, Any] = await self.graph.ainvoke(
            {"messages": [("user", query)]}
        )
        return result["messages"][-1].content
