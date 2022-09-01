import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_simple_cache.backends import Backend
from fastapi_simple_cache.decorator import cache
from fastapi_simple_cache import FastAPISimpleCache

app = FastAPI()
client = TestClient(app)


def test_no_request_param():
    with pytest.raises(TypeError) as e:

        @app.post("/no_request_param")
        @cache(expire=1)
        async def async_post(message: str):
            return {"message": message}

        assert e.value.startswith("No Request parameter in")


@pytest.mark.asyncio
async def test_no_init_get():
    FastAPISimpleCache.reset()
    with pytest.raises(Exception) as e:
        await FastAPISimpleCache.get(key="test")
        assert e.value == "You must call init first"


@pytest.mark.asyncio
async def test_no_init_set():
    FastAPISimpleCache.reset()
    with pytest.raises(Exception) as e:
        await Backend().set(key="test", response="test", expire=1)
        assert e.value == "You must call init first"


@pytest.mark.asyncio
async def test_abs_backend_get():
    with pytest.raises(NotImplementedError):
        await Backend().get(key="test")


@pytest.mark.asyncio
async def test_abs_backend_set():
    with pytest.raises(NotImplementedError):
        await Backend().set(key="test", response="test", expire=1)
