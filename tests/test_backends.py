import pytest
import time
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from fastapi_simple_cache import FastAPISimpleCache
from fastapi_simple_cache.decorator import cache
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


@pytest.fixture
def firestore_backend():
    backend = FirestoreBackend(collection=CollectionReference())
    FastAPISimpleCache.reset()
    FastAPISimpleCache.init(backend=backend)


@pytest.fixture
def redis_backend():
    backend = RedisBackend(redis=Redis())
    FastAPISimpleCache.reset()
    FastAPISimpleCache.init(backend=backend)


def test_firestore(firestore_backend):
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


def test_redis(redis_backend):
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
