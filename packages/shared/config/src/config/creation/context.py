from pathlib import Path

from pydantic import BaseModel


class DotEnvConfigContext(BaseModel):
    path: Path


class EnvConfigContext:
    pass


type ConfigContext = DotEnvConfigContext | EnvConfigContext
