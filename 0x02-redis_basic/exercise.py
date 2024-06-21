#!/usr/bin/env python3
import redis
import uuid
from typing import Union


class Cache:
    """class"""

    def __init__(self):
        """initalize the cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float,]) -> str:
        """store data in redis"""

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
