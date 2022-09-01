import inspect
import logging
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse
from functools import wraps
from typing import List

from .. import FastAPISimpleCache
from .key_builder import build_key

logger = logging.getLogger(__name__)


def cache(
    expire: int = 3600,
    status_codes: List[int] = [200],
):
    def wrapper(func):

        anno = func.__annotations__
        desc = f"{func.__module__}.{func.__name__}"
        request_key = next((k for k, v in anno.items() if v == Request), None)
        if request_key is None:
            raise TypeError(f"No Request parameter in {desc}")

        @wraps(func)
        async def inner(*args, **kwargs):
            nonlocal expire
            nonlocal status_codes
            nonlocal request_key
            # Get incoming request
            request = kwargs.get(request_key)
            no_cache = "no-cache" in request.headers.get("cache-control", "")
            # Get info from request
            query_params = dict(request.query_params)
            path_params = dict(request.path_params)
            body = await request.body()
            # Get response from cache
            key = build_key(
                func=func,
                namespace=FastAPISimpleCache.namespace,
                query_params=query_params,
                path_params=path_params,
                body=body,
            )
            if not no_cache:
                res, ttl = await FastAPISimpleCache.get(key=key)
                # Return if valid response exists
                if res and (ttl > 0):
                    res.headers["cache-control"] = f"max-age={expire}"
                    res.headers["age"] = f"{expire - ttl}"
                    return res
            # Get response
            if inspect.iscoroutinefunction(func):
                res = await func(**kwargs)
            else:
                res = func(**kwargs)
            # Return response
            if not isinstance(res, Response):
                res = JSONResponse(content=jsonable_encoder(res))
            if res.status_code in status_codes:
                FastAPISimpleCache.set(key, res, expire)
                if no_cache:
                    res.headers["cache-control"] = "no-cache"
                else:
                    res.headers["cache-control"] = f"max-age={expire}"
                    res.headers["age"] = "0"
            return res

        return inner

    return wrapper
