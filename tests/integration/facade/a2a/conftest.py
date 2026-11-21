import pytest
from a2a.server.agent_execution import AgentExecutor
from a2a.types import AgentCard
from langchain_core.language_models.fake_chat_models import FakeChatModel
from starlette.testclient import TestClient

from agentic_experiments.facade.a2a.executor import build_executor
from agentic_experiments.facade.a2a.graph import build_graph
from agentic_experiments.facade.a2a.server import (
    _build_asgi_app,
    _build_orchestrator_card,
)


@pytest.fixture
def model_card_fixture() -> AgentCard:
    return _build_orchestrator_card("http://localhost:8080")


@pytest.fixture
def agent_executor_fixture() -> AgentExecutor:
    return build_executor(build_graph(FakeChatModel()))


@pytest.fixture
def client_fixture(
    agent_executor_fixture: AgentExecutor, model_card_fixture: AgentCard
) -> TestClient:
    return TestClient(_build_asgi_app(agent_executor_fixture, model_card_fixture))
