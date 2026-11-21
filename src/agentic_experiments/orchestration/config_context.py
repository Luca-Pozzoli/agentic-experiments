from enum import StrEnum

from agentic_experiments.orchestration.config_source import DOTENV_FILE_PATH
from config import ConfigContext, DotEnvConfigContext, EnvConfigContext


class ConfigSource(StrEnum):
    DOTENV = "dotenv"
    ENV = "env"


def build_config_context(source: ConfigSource) -> ConfigContext:
    match source:
        case ConfigSource.DOTENV:
            return DotEnvConfigContext(path=DOTENV_FILE_PATH)
        case ConfigSource.ENV:
            return EnvConfigContext()
