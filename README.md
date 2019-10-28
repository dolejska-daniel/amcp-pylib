# Python AMCP Client Library
> v0.1.0


## Introduction
_TBD_


## Installation
```shell
pip install amcp_pylib
```


## Usage examples
_TBD_

### Connecting to server

```python
from amcp_pylib.core import Client

client = Client()
client.connect("caspar-server.local", 6969)  # defaults to 127.0.0.1, 5250
```

### Sending commands

```python
from amcp_pylib.core import Client
from amcp_pylib.module.query import VERSION, BYE

client = Client()
client.connect()

response = client.send(VERSION(component="server"))
print(response)

response = client.send(BYE())
print(response)
```

```shell
201(VERSION) ['2.0.7.e9fc25a Stable']
0(EMPTY) ['SERVER SENT NO RESPONSE']
```

All supported protocol commands are listed and documented on CasparCG's [wiki pages](https://github.com/CasparCG/help/wiki/AMCP-Protocol#table-of-contents).
