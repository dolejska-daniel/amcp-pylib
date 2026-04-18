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

The project uses `setuptools-scm` to derive package versions from Git tags and publishes a source distribution plus universal pure-Python wheel for releases.
Do not edit a static version in `pyproject.toml`; the built package version comes from the release tag.

Use PEP 440-compatible release tags:

- `v0.3.0` for a final release, published as `0.3.0`.
- `v0.3.0rc1` or `v0.3.0-rc1` for a release candidate, published as `0.3.0rc1`.
- `v0.3.0a1` or `v0.3.0b1` for alpha or beta releases.
- `v0.3.0.dev1` for an explicitly tagged development build.

Avoid arbitrary SemVer prerelease suffixes for PyPI releases, such as `v0.3.0-preview.0` or `v0.3.0-feature.0`.
PyPI uses PEP 440, so CI must map those names to a valid package version before building.
If that is ever needed, set `SETUPTOOLS_SCM_PRETEND_VERSION_FOR_AMCP_PYLIB` in the build step to a valid version such as `0.3.0rc0` or `0.3.0.dev4`.

Before publishing:

1. Update `README.md` and `CHANGELOG.md` for the release.
2. Run `python -m pytest`.
3. Run `python -m build`.
4. Run `python -m twine check dist/*`.
5. Tag the release with a PEP 440-compatible tag, for example `v0.3.0`.
6. Create a GitHub Release from that tag.

The PyPI project should be configured with a trusted publisher for repository `dolejska-daniel/amcp-pylib`, workflow `python-publish.yml`, and environment `pypi`.
The release workflow uses PyPI trusted publishing and does not require a long-lived PyPI API token.

TestPyPI is optional for this project.
Use it only when changing release automation or package metadata in a way that cannot be adequately checked with `python -m build`, `python -m twine check`, and a local wheel install smoke test.

Until a formal deprecation policy is added, avoid removing public imports from `amcp_pylib.core`, `amcp_pylib.module`, or `amcp_pylib.response` without a compatibility alias and release notes.
