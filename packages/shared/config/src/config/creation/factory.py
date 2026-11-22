from pathlib import Path

from pydantic_settings import DotEnvSettingsSource, EnvSettingsSource

from config.creation.context import ConfigContext, DotEnvConfigContext, EnvConfigContext
from config.model import AppConfig


class ConfigFactory:
    @staticmethod
    def build(context: ConfigContext) -> AppConfig:
        match context:
            case DotEnvConfigContext(path=dotenv_file_path):
                return ConfigFactory._from_dotenv_source(dotenv_path=dotenv_file_path)
            case EnvConfigContext():
                return ConfigFactory._from_env_source()

    @staticmethod
    def _from_dotenv_source(dotenv_path: Path) -> AppConfig:
        dotenv_source = DotEnvSettingsSource(
            settings_cls=AppConfig, env_file=dotenv_path
        )
        return AppConfig(**dotenv_source())

    @staticmethod
    def _from_env_source() -> AppConfig:
        env_source = EnvSettingsSource(settings_cls=AppConfig)
        return AppConfig(**env_source())
