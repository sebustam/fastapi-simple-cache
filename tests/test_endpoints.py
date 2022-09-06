import pytest
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel

from fastapi_simple_cache import FastAPISimpleCache
from fastapi_simple_cache.backends.inmemory import InMemoryBackend
from fastapi_simple_cache.decorator import cache

app = FastAPI()
client = TestClient(app)


class RequestTest(BaseModel):
    message: str


@pytest.fixture
def init_backend():
    FastAPISimpleCache.init(backend=InMemoryBackend())


def test_status_code(init_backend, caplog):
    FastAPISimpleCache.init(backend=InMemoryBackend())

    @app.get("/status_code")
    @cache(expire=1, status_codes=[200, 201])
    def status_code(status_code: int, request: Request):
        return JSONResponse(
            content={"status_code": status_code}, status_code=status_code
        )

    response = client.get("/status_code", params={"status_code": 404})
    assert caplog.records[0].message == "Not cached: status code 404"
    assert response.json().get("status_code") == 404
    response = client.get("/status_code", params={"status_code": 201})
    assert response.json().get("status_code") == 201
    assert response.headers.get("age") == "0"


def test_sync_get(init_backend):
    @app.get("/sync_get")
    @cache(expire=1)
    def sync_get(message: str, request: Request):
        return {"message": message}

    response = client.get("/sync_get", params={"message": "sync_get"})
    assert response.json().get("message") == "sync_get"


def test_async_get(init_backend):
    @app.get("/async_get")
    @cache(expire=1)
    async def async_get(message: str, request: Request):
        return {"message": message}

    response = client.get("/async_get", params={"message": "async_get"})
    assert response.json().get("message") == "async_get"


def test_sync_post(init_backend):
    @app.post("/sync_post")
    @cache(expire=1)
    def sync_post(message: str, request: Request):
        return {"message": message}

    response = client.post("/sync_post", params={"message": "sync_post"})
    assert response.json().get("message") == "sync_post"


def test_async_post(init_backend):
    @app.post("/async_post")
    @cache(expire=1)
    async def async_post(message: RequestTest, request: Request):
        return {"message": message.message}

    response = client.post("/async_post", json={"message": "async_post"})
    assert response.json().get("message") == "async_post"
