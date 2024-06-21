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
    def update_logs(self, *args, **kwargs) -> Any:
        input: str = method.__qualname__ + ':inputs'
        output: Any = method.__qualname__ + ':outputs'
        result = method(self, args) # return value of the method, the key
        self._redis.rpush(output, result)
        value: Any = self._redis.get(result)
        self._redis.rpush(input, str(args))
        return result
    return update_logs

def replay(method: Callable) -> None:
    """ replay the history of calls """
    method_name: str = method.__qualname__
    # get the number of times the method was called
    count: Any = method.__self__._redis.get(method_name)
    count = count.decode('utf-8')
    if count:
        count = int(count)
        print(f"{method_name} was called {count} times:")
        # get the inputs and outputs
        inputs = method.__self__._redis.lrange(f"{method_name}:inputs", 0, -1)
        outputs = method.__self__._redis.lrange(f"{method_name}:outputs", 0, -1)
        # convert the inputs and outputs to utf-8 strings
        inputs = [i.decode('utf-8') for i in inputs]
        outputs = [o.decode('utf-8') for o in outputs]
        # zip the inputs and outputs
        zipped = zip(inputs, outputs)
        # print the inputs and outputs
        for i, o in zipped:
            print(f"{method_name}(*{i}) -> {o}")


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



