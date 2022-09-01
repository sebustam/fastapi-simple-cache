from datetime import datetime
from fastapi import FastAPI, Request
from fastapi_simple_cache import FastAPISimpleCache
from fastapi_simple_cache.backends.redis import RedisBackend
from fastapi_simple_cache.decorator import cache
from redis.asyncio import ConnectionPool, client

app = FastAPI()


@app.on_event("startup")
async def startup():
    pool = ConnectionPool.from_url(url="redis://localhost:6379")
    backend = RedisBackend(redis=client.Redis(connection_pool=pool))
    FastAPISimpleCache.init(backend=backend)


@app.get("/")
@cache(expire=10)
def root(request: Request):
    return {"datetime": datetime.utcnow()}
