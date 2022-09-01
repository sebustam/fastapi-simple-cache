from datetime import datetime
from fastapi import FastAPI, Request
from fastapi_simple_cache import FastAPISimpleCache
from fastapi_simple_cache.backends.inmemory import InMemoryBackend
from fastapi_simple_cache.decorator import cache

app = FastAPI()


@app.on_event("startup")
async def startup():
    backend = InMemoryBackend()
    FastAPISimpleCache.init(backend=backend)


@app.get("/")
@cache(expire=10)
def root(request: Request):
    return {"datetime": datetime.utcnow()}
