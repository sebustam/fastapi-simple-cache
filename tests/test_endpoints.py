import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from pydantic import BaseModel

from fastapi_simple_cache import FastAPISimpleCache
from fastapi_simple_cache.backends.inmemory import InMemoryBackend
from fastapi_simple_cache.decorator import cache

app = FastAPI()
client = TestClient(app)


@pytest.fixture
def backend():
    backend = InMemoryBackend()
    FastAPISimpleCache.reset()
    FastAPISimpleCache.init(backend=backend)


def test_sync_get(backend):
    @app.get("/sync_get")
    @cache(expire=1)
    def sync_get(message: str, request: Request):
        return {"message": message}

    response = client.get("/sync_get", params={"message": "sync_get"})
    assert response.json().get("message") == "sync_get"


def test_async_get(backend):
    @app.get("/async_get")
    @cache(expire=1)
    async def async_get(message: str, request: Request):
        return {"message": message}

    response = client.get("/async_get", params={"message": "async_get"})
    assert response.json().get("message") == "async_get"


class RequestTest(BaseModel):
    message: str


def test_sync_post(backend):
    @app.post("/sync_post")
    @cache(expire=1)
    def sync_post(message: str, request: Request):
        return {"message": message}

    response = client.post("/sync_post", params={"message": "sync_post"})
    assert response.json().get("message") == "sync_post"


def test_async_post(backend):
    @app.post("/async_post")
    @cache(expire=1)
    async def async_post(message: RequestTest, request: Request):
        return {"message": message.message}

    response = client.post("/async_post", json={"message": "async_post"})
    assert response.json().get("message") == "async_post"
