#!/usr/bin/env python3
"""
Learn how to use redis for basic operations
Learn how to use redis as a simple cache
"""

import redis
import uuid
from functools import wraps
# import json
from typing import Union, Callable, Any


def count_calls(method: Callable) -> Callable:
    """decorator to count numer of times a func is called"""
    @wraps(method)
    def wrapper(self, key):
        """returns a modified function"""
        if not self._redis.get(method.__qualname__):
            self._redis.set(method.__qualname__, 1)
        else:
            self._redis.incr(method.__qualname__)
        return method(self, key)
    return wrapper


def call_history(method: Callable) -> Callable:
    """stores input and output history of method calls"""
    @wraps(method)
    def wrapper(self, *args):
        """wrapper funtion to store"""
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        output = method(self, str(args))
        self._redis.rpush(f"{method.__qualname__}:outputs", output)
        return output
    return wrapper


class Cache:
    """
    Basic redis operations
    simple cache with redis
    """

    def __init__(self) -> None:
        """creates an instance of reddis with empty data"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores a data to redis and returns the key"""
        key = str(uuid.uuid4())
        new_insert = {key: data}
        self._redis.mset(new_insert)
        return key

    def get(self, key: str, fn: Callable[[Any], Any] = None) -> Any:
        """gets data stored by key and returns the data"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is None:
            return data
        return fn(data)

    def get_str(self, key: str) -> str:
        """returns a stringed get"""
        data = self._redis.get(key)
        if data is None:
            return None
        return str(data)

    def get_int(self, key: str) -> int:
        """returnis int value"""
        data = self._redis.get(key)
        if data is None:
            return None
        return int(data)


def replay(obj: Callable) -> None:
    """return replay of cache called history"""
    c = redis.Redis()
    inputs = c.lrange("{}:inputs".format(obj.__qualname__), 0, -1)
    outputs = c.lrange("{}:outputs".format(obj.__qualname__), 0, -1)
    inout = zip(inputs, outputs)
    print("{} was called {} times:".format(obj.__qualname__, len(inputs)))
    for ins, outs in inout:
        outta = outs.decode('utf-8')
        print(f"Cache.store(*{ins.decode('utf-8')}) -> {outta}")
