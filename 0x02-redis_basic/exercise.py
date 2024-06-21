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
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ decorator to count the number of times a function is called """
    @wraps(method)
    def method_wrapper(self, key: str) -> Any:
        """ method to be called, self is passed because it is an instance method """
        check: Any = self._redis.get(method.__qualname__)
        if check:
            self._redis.incr(method.__qualname__)
        else:
            self._redis.set(method.__qualname__, 1)
        return method(self, key)
    return method_wrapper

def call_history(method: Callable) -> Callable:
    """ update the history of calls """
    @wraps(method)
    def update_logs(self, *args, **kwargs):
        input: str = method.__qualname__ + ':inputs'
        output: Any = method.__qualname__ + ':outputs'
        result = method(self, args) # return value of the method, the key
        self._redis.rpush(output, result)
        value: Any = self._redis.get(result)
        self._redis.rpush(input, str(args))
        return result
    return update_logs

class Cache:
    """ class to create a redis instance and cache data
    """
    def __init__(self) -> None:
        """ create an instance of redis """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store data in redis """
        key = str(uuid4())
        if (isinstance(data, bytes) or isinstance(data, str)):
            self._redis.set(key, data)
        else:
            self._redis.set(key, json.dumps(data))
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """ get data from redis """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        else:
            return data

    def get_str(self, key: str) -> Union[str, None]:
        """ get string data from redis """
        return self.get(key, fn=str)

    def get_int(self, key: str) -> Union[int, None]:
        """ call self.get with right params """
        return self.get(key, fn=int)



