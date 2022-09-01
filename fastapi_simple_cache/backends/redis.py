import json
import logging
from datetime import datetime, timedelta
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from math import ceil
from redis.asyncio.client import Redis
from typing import Optional, Tuple

from . import Backend

logger = logging.getLogger(__name__)


class RedisBackend(Backend):
    def __init__(
        self,
        redis: Redis,
    ):
        self.redis = redis

    async def get(
        self,
        key: str,
    ) -> Tuple[Optional[Response], Optional[int]]:
        async with self.redis.pipeline(transaction=True) as pipe:
            ttl, value = await (pipe.ttl(key).get(key).execute())
        if value is None:
            return None, None
        data = json.loads(value)
        response = Response(content=data.get("body"), headers=data.get("headers"))
        expire_at = datetime.fromisoformat(data.get("expire_at"))
        ttl = (expire_at - datetime.utcnow()).total_seconds()
        if ttl > 0:
            logger.debug(f"Get {key} from {type(self).__name__}")
        else:
            logger.debug(f"Exp {key} from {type(self).__name__}")
        return response, ceil(ttl)

    async def set(
        self,
        key: str,
        response: Response,
        expire: int,
    ) -> None:
        body = response.body
        headers = dict(response.headers)
        expire_at = datetime.utcnow() + timedelta(seconds=expire)
        data = {"body": body, "headers": headers, "expire_at": expire_at}
        value = json.dumps(jsonable_encoder(data), ensure_ascii=False)
        await self.redis.set(key, value, ex=expire)
        logger.debug(f"Set {key} to {type(self).__name__}")
