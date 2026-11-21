from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, Dependency

from config import ConfigContext, ConfigurationInversionOfControl


class CompositionRoot(DeclarativeContainer):
    config_context: Dependency[ConfigContext] = Dependency()

    config_container: Container[ConfigurationInversionOfControl] = Container(
        container_cls=ConfigurationInversionOfControl,
        config_context=config_context,
    )
