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

## Start

The project can be started with

```
uv run poe start
```

For CLI args please follow [Typer](https://typer.tiangolo.com/) instructions.

When starting the application from PyCharm, use the
[script parameters](https://www.jetbrains.com/help/pycharm/run-debug-configuration.html#run-debug-parameters)
to add CLI args.

### Configuration

Application config, at the time of writing, supports two sources:

- environment variables
- `.env` file inside the `config` folder

An example of a `.env` file is the one below

```
APP_FACADE__KIND=a2a
APP_FACADE__HOST=127.0.0.1
APP_FACADE__PORT=8080
APP_FACADE__LLM__KIND=openai-compatible
APP_FACADE__LLM__MODEL=<model_name>
APP_FACADE__LLM__URL=http://localhost:11434/v1
APP_FACADE__LLM__API_KEY=EMPTY
```

please notice the `APP_` variable prefix and the `__` nested limited separator.

Environment variables have the same names of their `.env` counterpart

### External services

Inside the project there is a [docker-compose.yml](https://docs.docker.com/reference/compose-file/) file which
contains containerized versions of external dependencies (such as [Ollama](https://ollama.com/) for local inference).