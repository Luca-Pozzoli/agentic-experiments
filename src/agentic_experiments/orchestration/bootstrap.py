from agentic_experiments.composition_root import CompositionRoot
from agentic_experiments.facade import expose_facade
from config import ConfigContext, FacadeConfig


def start_app(config_context: ConfigContext) -> None:
    root: CompositionRoot = _retrieve_activated_composition_root(config_context)
    _run(root.config_container().app_config().facade)


def _retrieve_activated_composition_root(
    config_context: ConfigContext,
) -> CompositionRoot:
    composition_root: CompositionRoot = CompositionRoot()
    composition_root.config_context.override(config_context)
    composition_root.init_resources()
    return composition_root


def _run(facade_config: FacadeConfig) -> None:
    expose_facade(facade_config)
