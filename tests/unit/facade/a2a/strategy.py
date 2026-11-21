import string
from typing import Final

from a2a.helpers import new_text_message
from a2a.server.agent_execution import RequestContext
from a2a.server.context import ServerCallContext
from a2a.types import Message, Role, SendMessageRequest
from hypothesis import HealthCheck, settings, strategies
from hypothesis.strategies import DrawFn, SearchStrategy
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

type InvalidTextMessage = str | None

async_pbt_settings = settings(
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)

WHITESPACE_CHARS: Final[str] = " \t\n\r\x0b\x0c"
SINGLE_WORD_STRATEGY: Final[SearchStrategy[str]] = strategies.text(
    alphabet=string.ascii_letters, min_size=1, max_size=12
)


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
def random_valid_message(draw: DrawFn) -> str:
    words: list[str] = draw(
        strategies.lists(SINGLE_WORD_STRATEGY, min_size=1, max_size=10)
    )
    separators: list[str] = draw(
        strategies.lists(
            strategies.text(alphabet=WHITESPACE_CHARS, min_size=1, max_size=4),
            min_size=len(words) - 1,
            max_size=len(words) - 1,
        )
    )
    leading: str = draw(strategies.text(alphabet=WHITESPACE_CHARS, max_size=4))
    trailing: str = draw(strategies.text(alphabet=WHITESPACE_CHARS, max_size=4))

    body = words[0] + "".join(sep + word for sep, word in zip(separators, words[1:]))
    return leading + body + trailing


@strategies.composite
def random_message_list(draw: DrawFn) -> list[BaseMessage]:
    previous_turns: int = draw(strategies.integers(min_value=0, max_value=4))
    history: list[BaseMessage] = []
    for _ in range(previous_turns):
        history.append(HumanMessage(draw(random_valid_message())))
        history.append(AIMessage(draw(random_valid_message())))
    history.append(HumanMessage(draw(random_valid_message())))
    return history


@strategies.composite
def random_valid_request_context(draw: DrawFn) -> RequestContext:
    return _make_context(draw(random_valid_message()))


@strategies.composite
def random_invalid_request_context(draw: DrawFn) -> RequestContext:
    return _make_context(draw(random_invalid_message()))


def _make_context(text: str | None) -> RequestContext:
    request: SendMessageRequest | None = None
    if text is not None:
        message: Message = new_text_message(text, role=Role.ROLE_USER)
        request = SendMessageRequest(message=message)
    return RequestContext(call_context=ServerCallContext(), request=request)
