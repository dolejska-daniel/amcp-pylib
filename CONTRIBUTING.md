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

The project uses static versions in `pyproject.toml` and a source distribution plus universal pure-Python wheel for releases.

Before publishing:

1. Update `pyproject.toml`, `README.md`, and `CHANGELOG.md` with the new version.
2. Run `python -m pytest`.
3. Run `python -m build`.
4. Run `python -m twine check dist/*`.
5. Tag the release and create a GitHub Release.

The PyPI project should be configured with a trusted publisher for repository `dolejska-daniel/amcp-pylib`, workflow `python-publish.yml`, and environment `pypi`.
The release workflow uses PyPI trusted publishing and does not require a long-lived PyPI API token.

TestPyPI is optional for this project.
Use it only when changing release automation or package metadata in a way that cannot be adequately checked with `python -m build`, `python -m twine check`, and a local wheel install smoke test.

Until a formal deprecation policy is added, avoid removing public imports from `amcp_pylib.core`, `amcp_pylib.module`, or `amcp_pylib.response` without a compatibility alias and release notes.
