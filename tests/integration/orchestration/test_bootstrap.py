from dependency_injector.providers import Container

from agentic_experiments.composition_root import CompositionRoot


def test_correct_instantiation_of_packages(
    composition_root_fixture: CompositionRoot,
) -> None:
    for item in composition_root_fixture.providers.values():
        if isinstance(item, Container):
            container: Container = item
            container.check_dependencies()
