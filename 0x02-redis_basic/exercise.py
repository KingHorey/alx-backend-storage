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
        key: Any = self._redis.get(key)
        if fn:
           return fn(key)
        elif isinstance(key, bytes):
            return key.decode('utf-8')


