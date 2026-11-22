from collections.abc import Iterator

import pytest
from pytest import MonkeyPatch

from agentic_experiments.composition_root import CompositionRoot
from config import EnvConfigContext, FacadeKind, LLMProviderKind


@pytest.fixture
def env_vars_setup_fixture(monkeypatch: MonkeyPatch) -> Iterator[None]:
    _inject_env_vars(
        {
            "facade": {
                "kind": FacadeKind.A2A,
                "host": "127.0.0.1",
                "port": 8000,
                "llm": {
                    "kind": LLMProviderKind.OpenAICompatible,
                    "api_token": "EMPTY",
                    "url": "http://127.0.0.1:11434/v1",
                    "model": "MODEL",
                },
            }
        },
        monkeypatch,
    )

    yield


@pytest.fixture
def composition_root_fixture(env_vars_setup_fixture: None) -> Iterator[CompositionRoot]:
    root: CompositionRoot = CompositionRoot()
    root.config_context.override(provider=EnvConfigContext)
    root.init_resources()
    root.apply_container_providers_overridings()

    yield root


def _inject_env_vars(starting_content: dict, monkeypatch: MonkeyPatch) -> None:
    flattened_dict: dict = _flatten_dictionary(dictionary=starting_content)
    for key, value in flattened_dict.items():
        monkeypatch.setenv(f"APP_{key.upper()}", str(value))


def _flatten_dictionary(dictionary: dict, parent_key: str = "") -> dict:
    items: list = []
    separator: str = "__"
    for key, value in dictionary.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(_flatten_dictionary(value, new_key).items())
        else:
            items.append((new_key, value))
    return dict(items)
