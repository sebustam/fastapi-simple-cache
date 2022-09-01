# FastAPI Simple Cache

[![Tests](https://github.com/sebustam/fastapi-simple-cache/actions/workflows/tests.yaml/badge.svg)](https://github.com/sebustam/fastapi-simple-cache/actions/workflows/tests.yaml)
[![Known Vulnerabilities](https://snyk-widget.herokuapp.com/badge/pip/fastapi-simple-cache/badge.svg)](https://snyk.io/test/github/sebustam/fastapi-simple-cache)
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
- [Features](#features)
  - [Namespaces](#namespaces)
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

## License

FastAPI Fire Cache is released under the GNU General Public License v3.0 or later,
see [here](https://choosealicense.com/licenses/gpl-3.0/) for a description of this
license, or see the [LICENSE](./LICENSE) file for the full text.
