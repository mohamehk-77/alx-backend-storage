#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """Cache class for Redis"""

    def __init__(self):
        """Initialize the cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key.

        :param data: The data to store, which can be a string, bytes, integer, or float.
        :return: The generated random key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and convert it back to the desired format using the callable fn.

        :param key: The key string to retrieve from Redis.
        :param fn: An optional callable used to convert the data.
        :return: The retrieved data, possibly converted using fn, or None if the key does not exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string from Redis.

        :param key: The key string to retrieve from Redis.
        :return: The retrieved string or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis.

        :param key: The key string to retrieve from Redis.
        :return: The retrieved integer or None if the key does not exist.
        """
        return self.get(key, fn=int)
