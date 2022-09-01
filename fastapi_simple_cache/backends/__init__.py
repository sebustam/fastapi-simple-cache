import abc
import logging
from fastapi import Response
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class Backend:
    @abc.abstractmethod
    async def get(
        self,
        key: str,
    ) -> Tuple[Optional[Response], Optional[int]]:
        raise NotImplementedError

    @abc.abstractmethod
    async def set(
        self,
        key: str,
        response: Response,
        expire: int,
    ) -> None:
        raise NotImplementedError
