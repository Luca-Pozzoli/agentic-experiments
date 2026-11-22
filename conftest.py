from pathlib import Path

import pytest

FOLDER_MARKERS: dict[str, str] = {
    "unit": "marks tests as unit tests",
    "integration": "marks tests as integration tests",
}


def pytest_configure(config) -> None:
    for marker, description in FOLDER_MARKERS.items():
        config.addinivalue_line("markers", f"{marker}: {description}")


def pytest_collection_modifyitems(items: list[pytest.Function]) -> None:
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
