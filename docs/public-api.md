# Public API

AMCP PyLib keeps backwards compatibility valuable.
Public imports listed here should not be removed or renamed without a deprecation period and release notes.

## Stable Imports

Core client classes:

```python
from amcp_pylib.core import Client, ClientAsync
```

Command construction:

```python
from amcp_pylib.module.query import VERSION
from amcp_pylib.module.basic import PLAY, STOP
from amcp_pylib.module import BYE, INFO, LOAD, VERSION
```

Responses:

```python
from amcp_pylib.response import ResponseBase, ResponseFactory
```

Concrete response classes are available from `amcp_pylib.response.types`:

```python
from amcp_pylib.response.types import (
    ClientErrorResponse,
    InfoResponse,
    ServerErrorResponse,
    SuccessResponse,
)
```

## Command Categories

Commands are grouped by AMCP protocol area:

- `amcp_pylib.module.basic`
- `amcp_pylib.module.data`
- `amcp_pylib.module.mixer`
- `amcp_pylib.module.query`
- `amcp_pylib.module.template`
- `amcp_pylib.module.thumbnail`

Every command factory returns a `Command` object.
Convert it to `str` to inspect the AMCP command text or pass it to `Client.send()` / `ClientAsync.send()`.

```python
from amcp_pylib.module.query import VERSION

command = VERSION(component="server")
assert str(command) == 'VERSION "server"\r\n'
```

## Advanced APIs

`Command` and `command_syntax` are available from `amcp_pylib.core` for custom command factories:

```python
from amcp_pylib.core import Command, command_syntax
```

The parser/scanner modules under `amcp_pylib.core.syntax` are implementation details for command syntax handling.
Treat them as internal unless you are extending or debugging command parsing.

## Errors

Invalid command arguments currently raise `RuntimeError`.
Socket and connection failures come from Python's standard library networking exceptions.

Future releases may add more specific exception classes.
If that happens, `RuntimeError` compatibility should be preserved for at least one minor release or documented with a migration path.

## Configuration Surface

The library does not currently define CLI commands, configuration files, environment variables, plugin entry points, or serialized file formats.

## Typing

The package contains some type annotations, but it is not currently published as a PEP 561 typed package and does not include `py.typed`.

Downstream users should not rely on complete type-checker coverage yet. Public APIs should be typed first before the package advertises typing support.

## Compatibility Policy

This project uses `0.x` versions, so minor releases may still refine APIs. Even so, consumer-facing imports should remain compatible wherever practical.

Recommended deprecation path for breaking changes:

1. Keep the old import or name as an alias.
2. Emit `DeprecationWarning` from the old path where feasible.
3. Document the replacement and migration example in the changelog.
4. Remove the old path no sooner than the next minor release.
