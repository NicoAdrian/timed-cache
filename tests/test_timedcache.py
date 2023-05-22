# -*- coding: utf-8 -*-
import asyncio
import io
import sys
import time
import unittest

from context import timedcache


def async_test(f):
    def wrapper(*args, **kwargs):
        asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))

    return wrapper


class BasicTestSuite(unittest.TestCase):
    def test_cache(self):
        d = timedcache.TimedCache(1)
        d["foo"] = "bar"
        self.assertIn("foo", d)
        self.assertEqual(len(d), 1)
        time.sleep(1.1)
        self.assertNotIn("foo", d)
        self.assertEqual(len(d), 0)

    def test_cache_function(self):
        l = []

        @timedcache.TimedCache(1)
        def foo(*args):
            l.append(None)
            return sum(args)

        numbers = [1, 2, 3]
        result = foo(*numbers)
        self.assertEqual(result, sum(numbers))
        self.assertEqual(len(l), 1)
        result2 = foo(*numbers)
        self.assertEqual(result2, sum(numbers))
        self.assertEqual(len(l), 1)

    @async_test
    async def test_cache_async_function(self):
        l = []

        @timedcache.TimedCache(1)
        async def foo(*args):
            l.append(None)
            return sum(args)

        numbers = [1, 2, 3]
        result = await foo(*numbers)
        self.assertEqual(result, sum(numbers))
        self.assertEqual(len(l), 1)
        result2 = await foo(*numbers)
        self.assertEqual(result2, sum(numbers))
        self.assertEqual(len(l), 1)


if __name__ == "__main__":
    try:
        unittest.main()
    except KeyboardInterrupt:
        pass
