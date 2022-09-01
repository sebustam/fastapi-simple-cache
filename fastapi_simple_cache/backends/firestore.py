import logging
from datetime import datetime, timedelta
from fastapi import Response
from google.cloud.firestore_v1.collection import CollectionReference
from math import ceil
from typing import Optional, Tuple

from . import Backend

logger = logging.getLogger(__name__)


class FirestoreBackend(Backend):
    def __init__(
        self,
        collection: CollectionReference,
    ):
        self.collection = collection

    async def get(
        self,
        key: str,
    ) -> Tuple[Optional[Response], Optional[int]]:
        doc = self.collection.document(key).get()
        if not doc.exists:
            return None, None
        data = doc.to_dict()
        response = Response(content=data.get("body"), headers=data.get("headers"))
        expire_at = data.get("expire_at").replace(tzinfo=None)
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
        self.collection.document(key).set(data)
        logger.debug(f"Set {key} to {type(self).__name__}")
