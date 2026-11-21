from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Final

import pytest
from _pytest.fixtures import SubRequest
from config.model import FacadeKind
from pytest import MonkeyPatch

APP_ENV_PREFIX: Final[str] = "APP_"


@pytest.fixture(params=list(FacadeKind), ids=lambda kind: kind.name)
def facade_kind_fixture(request: SubRequest) -> Iterator[FacadeKind]:
    yield request.param


@pytest.fixture
def dotenv_file_writer_fixture(tmp_path: Path) -> Iterator[Callable[..., Path]]:
    def dotenv_file_writer(*contents: dict) -> Path:
        dotenv_file_path: Path = Path(tmp_path, ".env")
        dotenv_file_path.write_text(
            "\n".join(_setup_dotenv_file_content(c) for c in contents),
            encoding="utf-8",
        )
        return dotenv_file_path

    yield dotenv_file_writer


@pytest.fixture
def env_vars_setup_fixture(monkeypatch: MonkeyPatch) -> Iterator[Callable[..., None]]:
    def setup(*contents: dict) -> None:
        for content in contents:
            _inject_env_vars(content, monkeypatch)

    yield setup


def _setup_dotenv_file_content(starting_content: dict) -> str:
    flattened_dict: dict = _flatten_dictionary(dictionary=starting_content)
    return "\n".join(
        f"{APP_ENV_PREFIX}{key.upper()}={value}"
        for key, value in flattened_dict.items()
    )


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


def _inject_env_vars(starting_content: dict, monkeypatch: MonkeyPatch) -> None:
    flattened_dict: dict = _flatten_dictionary(dictionary=starting_content)
    for key, value in flattened_dict.items():
        monkeypatch.setenv(f"{APP_ENV_PREFIX}{key.upper()}", str(value))
