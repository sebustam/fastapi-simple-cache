import json
import hashlib
from fastapi.encoders import jsonable_encoder
from typing import Callable


def build_key(
    func: Callable,
    *args,
    **kwargs,
):
    key_dict = {
        "__module__": func.__module__,
        "__name__": func.__name__,
        "__args__": args,
        "__kwargs__": kwargs,
    }
    str2hash = json.dumps(jsonable_encoder(key_dict))
    key = hashlib.sha256(str2hash.encode())
    return key.hexdigest()
