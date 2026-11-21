from agentic_experiments.facade import expose_facade
from agentic_experiments.orchestration.composition_root import CompositionRoot
from config import ConfigContext


def start_app(config_context: ConfigContext) -> None:
    _activate_inversion_of_control(config_context)
    _run()


def _activate_inversion_of_control(
    config_context: ConfigContext,
) -> None:
    composition_root: CompositionRoot = CompositionRoot()
    composition_root.config_context.override(config_context)
    composition_root.init_resources()


def _run() -> None:
    expose_facade()
