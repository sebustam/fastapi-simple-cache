import logging
import asyncio

from fastapi_simple_cache import logger

logger.setLevel(logging.DEBUG)
asyncio.log.logger.setLevel(logging.WARNING)
