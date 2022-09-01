"""FastAPI Simple Cache"""

__version__ = "0.1.0"

import asyncio
import logging
from fastapi import Response
from typing import List, Optional, Tuple, Union

from .backends import Backend

logger = logging.getLogger(__name__)


class FastAPISimpleCache:
    backends = None
    namespace = None

    @classmethod
    def init(
        cls,
        backend: Union[Backend, List[Backend]],
        namespace: Optional[str] = None,
    ) -> None:
        if isinstance(backend, Backend):
            backend = [backend]
        cls.backends = backend
        cls.namespace = namespace
        pass

    @classmethod
    async def get(
        cls,
        key: str,
    ) -> Tuple[Optional[Response], Optional[int]]:
        cls._check_init()
        for backend in cls.backends:
            response, ttl = await backend.get(key)
            if response:
                return response, ttl
        return None, None

    @classmethod
    def set(
        cls,
        key: str,
        response: Response,
        expire: int,
    ) -> None:
        cls._check_init()
        loop = asyncio.get_running_loop()
        for backend in cls.backends:
            loop.create_task(backend.set(key, response, expire))
        pass

    @classmethod
    def _check_init(cls):
        if cls.backends is None:
            raise Exception("You must call init first")
        pass

    @classmethod
    def reset(cls):
        cls.backends = None
        cls.namespace = None
        pass
