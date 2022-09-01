import logging
from datetime import datetime, timedelta
from fastapi import Response
from math import ceil
from typing import Optional, Tuple

from . import Backend

logger = logging.getLogger(__name__)


class InMemoryBackend(Backend):
    def __init__(self):
        self.data = {}

    async def get(
        self,
        key: str,
    ) -> Tuple[Optional[Response], Optional[int]]:
        data = self.data.get(key)
        if data is None:
            return None, None
        response = Response(content=data.get("body"), headers=data.get("headers"))
        ttl = (data.get("expire_at") - datetime.utcnow()).total_seconds()
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
        self.data[key] = {"body": body, "headers": headers, "expire_at": expire_at}
        logger.debug(f"Set {key} to {type(self).__name__}")
