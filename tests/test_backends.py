import pytest
import re
import time
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from fastapi_simple_cache import FastAPISimpleCache
from fastapi_simple_cache.decorator import cache
from fastapi_simple_cache.backends.inmemory import InMemoryBackend
from fastapi_simple_cache.backends.firestore import FirestoreBackend
from fastapi_simple_cache.backends.redis import RedisBackend

from .backends.firestore import CollectionReference
from .backends.redis import Redis

app = FastAPI()
client = TestClient(app)


@app.post("/")
@cache(expire=2)
def root(request: Request):
    return {"epoch": time.time()}


@pytest.mark.parametrize(
    "backend",
    [
        InMemoryBackend(),
        RedisBackend(Redis()),
        FirestoreBackend(CollectionReference()),
    ],
)
def test_single_backend(backend):
    FastAPISimpleCache.init(backend)
    response = client.post("/")
    epoch = response.json().get("epoch")
    assert response.headers.get("age") == "0"
    time.sleep(1)
    response = client.post("/")
    assert response.json().get("epoch") == epoch
    assert response.headers.get("age") == "1"
    time.sleep(1)
    response = client.post("/")
    assert response.json().get("epoch") != epoch
    assert response.headers.get("age") == "0"


@pytest.mark.parametrize(
    "backend",
    [
        RedisBackend(Redis()),
        FirestoreBackend(CollectionReference()),
    ],
)
def test_multi_backend(backend, caplog):
    FastAPISimpleCache.init(backend=[InMemoryBackend(), backend])
    backend_name = type(backend).__name__
    response = client.post("/")
    epoch = response.json().get("epoch")
    assert response.headers.get("age") == "0"
    assert re.match("Set .*? to InMemoryBackend", caplog.records[0].message)
    assert re.match(f"Set .*? to {backend_name}", caplog.records[1].message)
    time.sleep(1)
    response = client.post("/")
    assert response.json().get("epoch") == epoch
    assert response.headers.get("age") == "1"
    assert re.match("Get .*? from InMemoryBackend", caplog.records[2].message)
    time.sleep(1)
    response = client.post("/")
    assert response.json().get("epoch") != epoch
    assert response.headers.get("age") == "0"
    assert re.match("Exp .*? from InMemoryBackend", caplog.records[3].message)
    assert re.match("Set .*? to InMemoryBackend", caplog.records[4].message)
    assert re.match(f"Set .*? to {backend_name}", caplog.records[5].message)
