# timed-cache

Pure Python timed-cache that behaves like a regular `dict`.
Can also be used as a decorator to cache function calls (works for async functions as well).

## Installation

`pip install py-timed-cache`

## Example

```python
from timedcache import TimedCache

my_cache = TimedCache(1) # 1 second cache
my_cache["foo"] = "bar" # all dict methods works as if it was a normal dict
for k, v in my_cache.items():
    print(k, v) # will print foo bar

# Also works for functions

@TimedCache(5)
def foo(number):
    # some expensive compute...
    print("begin computation...")
    result = number * 10**30
    print("end computation")
    return res

big_number = foo(42) # cache MISS ==> this will print both statements above

big_number_again = foo(42) # Called with same argument(s) ==> cache HIT, returns immediately
```

## Python versions

Python >= 3.6 are supported

## Tests

This project uses `unittest`.

Run `python tests/test_timedcache.py`
