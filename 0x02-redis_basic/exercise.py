#!/usr/bin/env python3
""" import redis for daster caching
    import uuid4 for generating unique keys
    import json for converting data to json format
    import Any for type hinting
"""
import redis
from uuid import uuid4
from typing import Any, Union, Callable, Optional
import json


class Cache:
    """ class to create a redis instance and cache data
    """
    def __init__(self) -> None:
        """ create an instance of redis """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store data in redis """
        key = str(uuid4())
        if (isinstance(data, bytes) or isinstance(data, str)):
            self._redis.set(key, data)
        else:
            self._redis.set(key, json.dumps(data))
        return key

    def get(self, key: str, fn: Optional[Callable]) -> Any:
        """ get data from redis """
        data = self._redis.get(key)
        if data is None:
            return None
        elif fn:
            return fn(data)
        else:
            return data

    def get_str(self, key: str) -> Union[str, None]:
        """ get string data from redis """
        if key is None:
            return None
        else:
            key = self._redis.get(key)
            if key is None:
                return None
            else:
                return str(key)

    def get_int(self, key: str) -> Union[int, None]:
        """ get string data from redis """
        if key is None:
            return None
        else:
            key = self._redis.get(key)
            if key is None:
                return None
            else:
                return int(key)



cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    print(key)
    assert cache.get(key, fn=fn) == value

