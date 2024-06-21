#!/usr/bin/env python3
""" get_page module to get the page of a URL """
from typing import Callable
from functools import wraps
import requests
import redis

# Initialize Redis client
redis_client = redis.Redis()


def count(method: Callable) -> Callable:
    """ Count the number of times a method is called """
    @wraps(method)
    def wrapper(url: str) -> str:
        """ Wrapper for counting and caching """
        # Increment the count for this URL
        redis_client.incr(f"count:{url}")

        # Check if the URL content is cached
        cached = redis_client.get(f"cached:{url}")
        if cached:
            return cached.decode('utf-8')

        # Get the URL content and cache it
        res = method(url)
        redis_client.setex(f"cached:{url}", 10, res)
        return res

    return wrapper


@count
def get_page(url: str) -> str:
    """ Get the page content of a URL """
    return requests.get(url).text
