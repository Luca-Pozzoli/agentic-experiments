from typing import NoReturn

from agentic_experiments.facade.a2a import expose_a2a_facade
from config import FacadeConfig, FacadeKind


def expose_facade(facade_config: FacadeConfig) -> NoReturn:
    match facade_config.kind:
        case FacadeKind.A2A:
            expose_a2a_facade(facade_config)
