import json
from datetime import datetime, timedelta
from typing import Mapping, Optional


class Pipeline:
    def __init__(
        self,
        redis,
    ):
        self.redis = redis
        self.key = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        self.key = None

    def ttl(self, key):
        return self

    def get(self, key):
        self.key = key
        return self

    async def execute(self):
        value = self.redis.data.get(self.key)
        if value is None:
            return None, None
        data = json.loads(value)
        expire_at = datetime.fromisoformat(data.get("expire_at"))
        ttl = (expire_at - datetime.utcnow()).total_seconds()
        return ttl, value


class Redis:
    def __init__(
        self,
        data: Optional[Mapping] = None,
    ):
        if data is None:
            data = {}
        self.data = data

    def pipeline(
        self,
        **kwargs,
    ):
        return Pipeline(redis=self)

    async def set(self, key: str, value: str, ex: int):
        data = json.loads(value)
        data["expire_at"] = (datetime.utcnow() + timedelta(seconds=ex)).isoformat()
        value = json.dumps(data)
        self.data[key] = value
