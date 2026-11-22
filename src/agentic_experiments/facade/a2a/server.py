from typing import NoReturn

import uvicorn
from a2a.server.agent_execution import AgentExecutor
from a2a.server.request_handlers import DefaultRequestHandler, RequestHandler
from a2a.server.routes import (
    add_a2a_routes_to_fastapi,
    create_agent_card_routes,
    create_rest_routes,
)
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill
from fastapi import FastAPI
from starlette.applications import Starlette

from agentic_experiments.facade.a2a.executor import build_executor
from agentic_experiments.facade.a2a.graph import get_compiled_graph
from config import A2AFacadeConfig


def expose_a2a_facade(a2a_config: A2AFacadeConfig) -> NoReturn:  # ty: ignore[invalid-implicit-return]
    agent_executor = build_executor(get_compiled_graph(a2a_config.llm))
    card = _build_orchestrator_card(f"http://{a2a_config.host}:{a2a_config.port}")
    asgi_app = _build_asgi_app(agent_executor, card)
    uvicorn.run(asgi_app, host=str(a2a_config.host), port=a2a_config.port)


def _build_asgi_app(agent_executor: AgentExecutor, card: AgentCard) -> Starlette:
    app = FastAPI()
    add_a2a_routes_to_fastapi(
        app,
        agent_card_routes=create_agent_card_routes(card),
        rest_routes=create_rest_routes(_build_request_handler(agent_executor, card)),
    )
    return app


def _build_orchestrator_card(base_url: str) -> AgentCard:
    return AgentCard(
        name="Orchestrator",
        description="Application orchestrator",
        version="0.1.0",
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        capabilities=AgentCapabilities(streaming=False),
        supported_interfaces=[
            AgentInterface(
                protocol_binding="HTTP+JSON", url=base_url, protocol_version="1.0"
            )
        ],
        skills=[
            AgentSkill(
                id="chat",
                name="Chat",
                description="Answer a chat message",
                tags=["chat"],
                input_modes=["text/plain"],
                output_modes=["text/plain"],
            )
        ],
    )


def _build_request_handler(
    agent_executor: AgentExecutor, card: AgentCard
) -> RequestHandler:
    return DefaultRequestHandler(
        agent_executor=agent_executor,
        task_store=InMemoryTaskStore(),
        agent_card=card,
    )
