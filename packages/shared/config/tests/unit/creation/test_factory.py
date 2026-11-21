from collections.abc import Callable
from pathlib import Path

from config.creation import ConfigFactory, DotEnvConfigContext, EnvConfigContext
from config.model import AppConfig, FacadeKind
from hypothesis import HealthCheck, given, settings, strategies


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(data=strategies.data())
def test_given_correct_dotenv_file_when_loading_config_then_expect_correct_settings(
    data: strategies.DataObject,
    facade_kind_fixture: FacadeKind,
    dotenv_file_writer_fixture: Callable[..., Path],
) -> None:
    facade_config: dict = data.draw(
        _create_test_data_strategy_for_facade_config(facade_kind_fixture)
    )
    dotenv_file_path: Path = dotenv_file_writer_fixture(facade_config)

    app_config: AppConfig = ConfigFactory.build(
        context=DotEnvConfigContext(path=dotenv_file_path)
    )

    _assert_config_values_are_correct(
        actual=app_config, expected=AppConfig(**facade_config)
    )


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(data=strategies.data())
def test_given_correct_env_vars_when_loading_config_then_expect_correct_settings(
    data: strategies.DataObject,
    facade_kind_fixture: FacadeKind,
    env_vars_setup_fixture: Callable[..., None],
) -> None:
    facade_config: dict = data.draw(
        _create_test_data_strategy_for_facade_config(facade_kind_fixture)
    )
    env_vars_setup_fixture(facade_config)

    app_config: AppConfig = ConfigFactory.build(context=EnvConfigContext())

    _assert_config_values_are_correct(
        actual=app_config, expected=AppConfig(**facade_config)
    )


def _assert_config_values_are_correct(
    actual: AppConfig,
    expected: AppConfig,
) -> None:
    assert actual.model_dump() == expected.model_dump()


def _create_test_data_strategy_for_facade_config(
    facade_kind: str,
) -> strategies.SearchStrategy[dict]:
    match facade_kind:
        case _ if facade_kind == FacadeKind.A2A:
            return strategies.fixed_dictionaries(
                {
                    "facade": strategies.fixed_dictionaries(
                        {
                            "kind": strategies.just(FacadeKind.A2A),
                            "host": strategies.ip_addresses(),
                            "port": strategies.integers(min_value=1, max_value=65535),
                        }
                    )
                }
            )
        case _:
            raise ValueError(f"Unknown facade kind {facade_kind}")
