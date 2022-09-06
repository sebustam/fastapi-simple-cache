import time
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from fastapi_simple_cache import FastAPISimpleCache
from fastapi_simple_cache.decorator import cache
from fastapi_simple_cache.backends.inmemory import InMemoryBackend

app = FastAPI()
client = TestClient(app)


@app.get("/")
@cache(expire=2)
def root(request: Request):
    return {"time": time.time()}


def test_max_age():
    FastAPISimpleCache.init(backend=InMemoryBackend())
    response = client.get("/")
    first_time = response.json().get("time")
    assert response.headers.get("cache-control") == "max-age=2"
    assert response.headers.get("age") == "0"
    time.sleep(1)
    response = client.get("/")
    second_time = response.json().get("time")
    assert first_time == second_time
    assert response.headers.get("cache-control") == "max-age=2"
    assert response.headers.get("age") == "1"
    time.sleep(1)
    response = client.get("/")
    third_time = response.json().get("time")
    assert first_time < third_time - 2
    assert response.headers.get("cache-control") == "max-age=2"
    assert response.headers.get("age") == "0"


def test_no_cache():
    FastAPISimpleCache.init(backend=InMemoryBackend())
    response = client.get("/", headers={"cache-control": "no-cache"})
    assert response.headers.get("cache-control") == "no-cache"
