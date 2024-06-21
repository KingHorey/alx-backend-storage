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
        return self.get(key, fn=str)

    def get_int(self, key: str) -> Union[int, None]:
        """ call self.get with right params """
        return self.get(key, fn=int)


cache = Cache()

TEST_CASES = {
    b"foo": int,
    123: str,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn) == value

