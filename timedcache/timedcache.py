# -*- coding: utf-8 -*-
import collections
import functools
import inspect
import time


class TimedCache(collections.abc.MutableMapping):
    def __init__(self, timeout):
        self.timeout = timeout
        self._mapping = {}

    def __call__(self, func):
        sentinel = object()
        cache_get = self.get

        class _HashedSeq(list):
            __slots__ = "hashvalue"

            def __init__(self, tup):
                self[:] = tup
                self.hashvalue = hash(tup)

            def __hash__(self):
                return self.hashvalue

        def _make_key(args, kwargs, mark=(object(),), fasttypes={str, int}):
            key = args
            if kwargs:
                key += mark
                for item in kwargs.items():
                    key += item
            if len(key) == 1 and type(key[0]) in fasttypes:
                return key[0]
            return _HashedSeq(key)

        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                key = _make_key(args, kwargs)
                res = cache_get(key, sentinel)
                if res is not sentinel:
                    return res
                res = await func(*args, **kwargs)
                self[key] = res
                return res

        else:

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = _make_key(args, kwargs)
                res = cache_get(key, sentinel)
                if res is not sentinel:
                    return res
                res = func(*args, **kwargs)
                self[key] = res
                return res

        return wrapper

    def __setitem__(self, k, v):
        self._mapping[k] = (v, time.time())

    def __getitem__(self, k):
        v, t = self._mapping[k]
        if time.time() - t > self.timeout:
            del self[k]
            raise KeyError(k)
        return v

    def __delitem__(self, k):
        del self._mapping[k]

    def __iter__(self):
        for k, (_, t) in self._mapping.items():
            if time.time() - t <= self.timeout:
                yield k

    def __len__(self):
        return sum(1 for _ in self)
