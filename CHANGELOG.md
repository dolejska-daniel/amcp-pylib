# Changelog

## 0.3.0 - Unreleased

### Added

- Modern `pyproject.toml` packaging metadata with PEP 517 builds.
- GitHub Actions CI for supported Python versions and package build validation.
- Contributor and security reporting guidance.
- Regression tests for scanner, parser, and command-call state isolation.
- Tag-derived package versions with `setuptools-scm`.
- Public API and consumer compatibility documentation.
- Minimal Ruff lint configuration.

### Changed

- Declared Python 3.9+ support in package metadata.
- Updated release publishing to validate artifacts before upload.
- Documented PEP 440-compatible release tag conventions.
- Expanded the README quickstart and installation guidance.
- Added CI linting, built-wheel smoke testing, and distribution artifact upload.

### Fixed

- Prevent command factory calls from reusing arguments from earlier calls.
- Reset scanner position and returned-token state for each `Scanner` instance.
