"""FastAPI Simple Cache"""

__version__ = "0.1.5"

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
        """Cache initialization

        Args:
            backend (Union[Backend, List[Backend]]): Backend(s) for cache.
            namespace (Optional[str], optional): Key building modificator. Defaults to None.
        """
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
        """Get cached response from request key

        Args:
            key (str): Request key.

        Returns:
            Tuple[Optional[Response], Optional[int]]: Response and TTL.
        """
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
        """Set response key/response value pair in cache

        Args:
            key (str): Request key.
            response (Response): Response.
            expire (int): Expiration time in seconds.
        """
        cls._check_init()
        loop = asyncio.get_running_loop()
        for backend in cls.backends:
            loop.create_task(backend.set(key, response, expire))
        pass

    @classmethod
    def reset(cls):
        """Resets FastAPISimpleCache"""
        cls.backends = None
        cls.namespace = None
        pass

    @classmethod
    def _check_init(cls):
        """Check cache initialization

        Raises:
            Exception: Raised when no backend has been set.
        """
        if cls.backends is None:
            raise Exception("You must call init first")
        pass
