from typing import Annotated, NoReturn

import typer
from typer import Option

from agentic_experiments.orchestration import (
    ConfigSource,
    build_config_context,
    start_app,
)
from config import ConfigContext


def _start(config_source: Annotated[ConfigSource, Option("--source")]) -> None:
    config_context: ConfigContext = build_config_context(config_source)
    start_app(config_context)


def cli() -> NoReturn:  # ty: ignore[invalid-implicit-return]
    typer.run(_start)


if __name__ == "__main__":
    cli()
