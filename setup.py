# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open("README.md") as fd:
    readme = fd.read()

setup(
    name="py-timed-cache",
    version="1.0.2",
    description="Pure Python timed-cache",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Nicolas Adrian",
    author_email="nicolasadrian3@gmail.com",
    url="https://github.com/NicoAdrian/timed-cache",
    license="MIT",
    keywords=["cache", "timed-cache", "timedcache"],
    packages=find_packages(),
)
