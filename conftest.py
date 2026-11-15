from pathlib import Path

import pytest


def pytest_collection_modifyitems(items: list[pytest.Function]):
    for item in items:
        test_path: Path = Path(item.fspath)
        path_parts: tuple[str, ...] = test_path.parts
        tests_index: int = path_parts.index("tests")
        marker_subfolder: str = path_parts[tests_index + 1]

        match marker_subfolder:
            case "integration":
                item.add_marker("integration")
            case "unit":
                item.add_marker("unit")
            case _:
                raise pytest.UsageError(
                    f"Unknown test subfolder {marker_subfolder} for {test_path}"
                )
