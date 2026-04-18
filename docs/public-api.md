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
from amcp_pylib.module.basic import CLEAR_ALL, PLAY, STOP
from amcp_pylib.module import BYE, INFO, LOAD, VERSION
```

Responses:

```python
from amcp_pylib.response import ResponseBase, ResponseCodeClass, ResponseFactory
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
assert str(command) == "VERSION server\r\n"
```

## Advanced APIs

`Command` and `command_syntax` are available from `amcp_pylib.core` for custom command factories and raw command escape hatches:

```python
from amcp_pylib.core import Command, command_syntax

raw = Command.raw("HELP PLAY")
batched = raw.with_request_id("help-1")
```

`Client.send_raw_command()` and `ClientAsync.send_raw_command()` accept already serialized AMCP command text and append `\r\n` when needed.

The parser/scanner modules under `amcp_pylib.core.syntax` are implementation details for command syntax handling.
Treat them as internal unless you are extending or debugging command parsing.

## Errors

Invalid command arguments continue to raise `RuntimeError` for compatibility.
Socket and connection failures come from Python's standard library networking exceptions, except for client misuse where no connection exists.

Specific AMCP exceptions are available from `amcp_pylib.exceptions`:

```python
from amcp_pylib.exceptions import AMCPConnectionError, AMCPParseError, AMCPResponseError
```

Responses do not raise automatically. Call `response.raise_for_status()` to raise `AMCPResponseError` for 4xx and 5xx replies.

## Configuration Surface

The library does not currently define CLI commands, configuration files, environment variables, plugin entry points, or serialized file formats.

## Typing

The package includes `py.typed` for PEP 561 type-checker discovery. Coverage is intentionally strongest around public command, response, and client objects; the syntax parser internals remain less strict.

## Modern CasparCG Compatibility

Helpers exist for Server 2.4 additions including `CLEAR_ALL`, `CALLBG`, `CLEAR_ON_404`, `OSC_SUBSCRIBE`, `OSC_UNSUBSCRIBE`, and batching helpers `BEGIN`, `COMMIT`, and `DISCARD`.

Request ids can be supplied to every command factory with `request_id="..."`. Responses preserve `response.request_id` when the server returns a `RES <id>` prefix.

Some legacy documented helpers remain available even when current CasparCG source may not register the command in every release line, notably selected `INFO`/`HELP` variants. Use `Command.raw()` or `send_raw_command()` for live-server discovery and forward compatibility.

## Compatibility Policy

This project uses `0.x` versions, so minor releases may still refine APIs. Even so, consumer-facing imports should remain compatible wherever practical.

Recommended deprecation path for breaking changes:

1. Keep the old import or name as an alias.
2. Emit `DeprecationWarning` from the old path where feasible.
3. Document the replacement and migration example in the changelog.
4. Remove the old path no sooner than the next minor release.
