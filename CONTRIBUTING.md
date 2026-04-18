# Contributing

## Development setup

Create and activate a virtual environment, then install the package with its test tools:

```shell
python -m pip install -e ".[dev]"
```

## Common tasks

Run the test suite:

```shell
python -m pytest
```

Build source and wheel distributions:

```shell
python -m build
```

Validate distribution metadata before publishing:

```shell
python -m twine check dist/*
```

## Release policy

The project uses static versions in `pyproject.toml`. Update the version, tag the release, and publish from a GitHub Release so the PyPI workflow can use trusted publishing instead of long-lived API tokens.

Until a formal deprecation policy is added, avoid removing public imports from `amcp_pylib.core`, `amcp_pylib.module`, or `amcp_pylib.response` without a compatibility alias and release notes.
