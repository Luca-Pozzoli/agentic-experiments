# Agentic experiments

This project is a showcase for agentic workflows.

## Development

Project dependencies are managed with [uv](https://docs.astral.sh/uv/).

### Setup

Interpreter version is specified in the `.python-version` file.

The [virtual environment](https://docs.python.org/3/library/venv.html) can be managed with
[uv](https://docs.astral.sh/uv/) as well. The IDE must be configured to use it:

- [PyCharm venv setup](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)

### Project scripts

Scripts, such as code quality tools, are managed with `poethepoet`, whose scripts are defined inside the
`pyproject.toml` file.

In order to execute them, use the command `uv run poe <command_name>`. Some tasks allow the usage of arguments. For
example, the formatter can be invoked as

```
uv run poe format
```

while the following command checks whether files should be formatted

```
uv run poe format --check
```

### Testing

At the time of writing, the tests are run using the [pytest framework](https://docs.pytest.org/en/stable/)

Each package has its own `tests` folder which is further divided into test categories (e.g. `unit` and `integration`).
Tests groups can be executed using the corresponding [code quality command](#project-scripts), for example

```
uv run poe unit-test
```

All test groups can be sequentially executed with the following command

```
uv run poe test
```
