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
    """Cache responses from endpoint

    Args:
        expire (int, optional): Expiration time in seconds. Defaults to 3600.
        status_codes (List[int], optional): Valid status codes to cache responses. Defaults to [200].
    """

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
            no_cache = (request.headers is not None) and (
                "no-cache" in request.headers.get("cache-control", "")
            )
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
                if no_cache:
                    res.headers["cache-control"] = "no-cache"
                    logger.warning("Not cached: 'no-cache' directive")
                else:
                    FastAPISimpleCache.set(key, res, expire)
                    res.headers["cache-control"] = f"max-age={expire}"
                    res.headers["age"] = "0"
            else:
                logger.warning(f"Not cached: status code {res.status_code}")
            return res

        return inner

    return wrapper
