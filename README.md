# FastAPI Simple Cache

[![Tests](https://github.com/sebustam/fastapi-simple-cache/actions/workflows/tests.yaml/badge.svg)](https://github.com/sebustam/fastapi-simple-cache/actions/workflows/tests.yaml)
[![Coverage](https://codecov.io/gh/sebustam/fastapi-simple-cache/branch/main/graph/badge.svg?token=6JPFPOQWX2)](https://codecov.io/gh/sebustam/fastapi-simple-cache)
[![Package version](https://img.shields.io/pypi/v/fastapi-simple-cache?color=%2334D058)](https://pypi.org/project/fastapi-simple-cache)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/fastapi-simple-cache.svg?color=%2334D058)](https://pypi.org/project/fastapi-simple-cache)

FastAPI Simple Cache will cache responses from a decorated endpoint if the response
is [JSON encodable](https://fastapi.tiangolo.com/tutorial/encoder/) or
a [FastAPI `Response`](https://fastapi.tiangolo.com/advanced/response-directly/).

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Quick start](#quick-start)
- [Installation](#installation)
- [Backends](#backends)
  - [In memory](#in-memory)
  - [Redis](#redis)
  - [Firestore](#firestore)
- [Features](#features)
  - [Namespaces](#namespaces)
  - [Valid status codes](#valid-status-codes)
- [License](#license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Quick start

```python
from fastapi import FastAPI, Request

app = FastAPI()

# Initialize in startup event
from fastapi_simple_cache import FastAPISimpleCache
from fastapi_simple_cache.backends.inmemory import InMemoryBackend
@app.on_event("startup")
async def startup():
    backend = InMemoryBackend()
    FastAPISimpleCache.init(backend=backend)
    pass

# Use the @cache decorator
from fastapi_simple_cache.decorator import cache
@app.get("/")
@cache(expire=3600)  # Set expiration in seconds
def root(request: Request):  # Add a Request typed parameter
    return {"datetime": datetime.utcnow()}
```

## Installation

The installation depends on the backend.

- In memory: `pip install fastapi-simple-cache`
- Redis: `pip install "fastapi-simple-cache[redis]"`
- Firestore: `pip install "fastapi-simple-cache[firestore]"`

## Backends

### In memory

The `InMemoryBackend` class implements an in-memory backend.

```python
from fastapi_simple_cache.backends.inmemory import InMemoryBackend

backend = InMemoryBackend()
```

### Redis

The `RedisBackend` class implements a Redis backend.

```python
from redis.asyncio import ConnectionPool, client

pool = ConnectionPool.from_url(url="redis://localhost:6379")
backend = RedisBackend(redis=client.Redis(connection_pool=pool))
```

### Firestore

The `FirestoreBackend` class implements a Google Firestore backend.

```python
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {"projectId": "gcp_project"})
db = firestore.client()
collection = db.collection("cache_collection")
backend = FirestoreBackend(collection=collection)
```

## Features

### Namespaces

You can add the parameter `namespace` on cache initialization
with `FastAPISimpleCache.init` to modify the storage keys. Use this feature
if you need to share same cache environment with other applications but with
different keys.

```python
@app.on_event("startup")
async def startup():
    FastAPISimpleCache.init(
        backend=backend,
        namespace="my-app"
    )
    pass
```

### Valid status codes

Set valid status codes to cache responses in the `@cache` parameter
`status_codes` (defaults to `[200]`).

```python
@app.get("/")
@cache(expire=3600, status_codes=[200, 201])
def root(request: Request):
    return {"datetime": datetime.utcnow()}
```

## License

FastAPI Fire Cache is released under the GNU General Public License v3.0 or later,
see [here](https://choosealicense.com/licenses/gpl-3.0/) for a description of this
license, or see the [LICENSE](./LICENSE) file for the full text.
