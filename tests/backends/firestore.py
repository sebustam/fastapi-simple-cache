from typing import Mapping, Optional, Any


class Document:
    def __init__(
        self,
        data: Optional[Mapping] = None,
        collection: Optional[Any] = None,
        key: Optional[str] = None,
    ):
        if data is None:
            data = {}
        self.data = data
        self.collection = collection
        self.key = key

    def get(
        self,
        key: Optional[str] = None,
    ):
        if key is None:
            return self
        return self.data.get(key)

    def set(
        self,
        data: Mapping,
    ):
        self.collection.data[self.key] = data

    def to_dict(self):
        return self.data

    @property
    def exists(self):
        return len(self.data) > 0


class CollectionReference:
    def __init__(
        self,
        data: Optional[Mapping] = None,
    ):
        if data is None:
            data = {}
        self.data = data

    def document(self, key: str) -> Document:
        return Document(
            data=self.data.get(key),
            collection=self,
            key=key,
        )
