from typing import NoReturn

from agentic_experiments.facade.a2a import expose_a2a_facade


def expose_facade() -> NoReturn:
    expose_a2a_facade("127.0.0.1", 8000)
