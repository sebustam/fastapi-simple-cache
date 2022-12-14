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
  - [Multi backends](#multi-backends)
  - [Valid status codes](#valid-status-codes)
  - [No cache](#no-cache)
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

# Use the @cache decorator
from fastapi_simple_cache.decorator import cache

@app.get("/")
@cache(expire=3600)  # Set expiration in seconds
def root(request: Request):  # Add a Request typed parameter
    return {"datetime": datetime.utcnow()}
```

Check [here](examples/) for FastAPI application examples with
different [backends](#backends) and [features](#features).

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

@app.on_event("startup")
async def startup():
    backend = InMemoryBackend()
    FastAPISimpleCache.init(backend=backend)
```

### Redis

The `RedisBackend` class implements a Redis backend.

```python
from redis.asyncio import ConnectionPool, client
from fastapi_simple_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    pool = ConnectionPool.from_url(url="redis://localhost:6379")
    backend = RedisBackend(redis=client.Redis(connection_pool=pool))
    FastAPISimpleCache.init(backend=backend)
```

### Firestore

The `FirestoreBackend` class implements a Google Firestore backend.

```python
import firebase_admin
from firebase_admin import firestore, credentials
from fastapi_simple_cache.backends.firestore import FirestoreBackend

@app.on_event("startup")
async def startup():
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {"projectId": "gcp_project"})
    db = firestore.client()
    collection = db.collection("cache_collection")
    backend = FirestoreBackend(collection=collection)
    FastAPISimpleCache.init(backend=backend)
```

## Features

### Namespaces

You can add the parameter `namespace` on cache initialization to modify
the storage keys. Use this feature if you need to share same cache
environment with other applications but with different keys.

```python
@app.on_event("startup")
async def startup():
    backend = InMemoryBackend()
    FastAPISimpleCache.init(
        backend=backend,
        namespace="my-app"
    )
```

### Multi backends

Use more than one backend to cache responses with the `backend` parameter
on cache initialization. This feature is useful if you want to check an
in-memory cache before an external cache.

```python
from fastapi_simple_cache.backends.inmemory import InMemoryBackend
from fastapi_simple_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    inmem_backend = InMemoryBackend()
    redis_backend = RedisBackend(...)
    FastAPISimpleCache.init(
        backend=[inmem_backend, redis_backend]
    )
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

### No cache

Avoid storing a request/response by adding the header
`cache-control: no-cache` to the request. This works both for the client
and the server.

## License

FastAPI Fire Cache is released under the GNU General Public License v3.0 or
later, see [here](https://choosealicense.com/licenses/gpl-3.0/) for a
description of this license, or see the [LICENSE](./LICENSE) file for
the full text.
