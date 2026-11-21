from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Resource

from config.creation import ConfigContext, ConfigFactory
from config.model import AppConfig


class ConfigurationInversionOfControl(DeclarativeContainer):
    config_context: Dependency[ConfigContext] = Dependency()

    app_config: Resource[AppConfig] = Resource(
        provides=ConfigFactory.build, context=config_context
    )
