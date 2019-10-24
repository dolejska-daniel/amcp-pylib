#!/usr/bin/env python3

from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="amcp_pylib",
    url="https://github.com/dolejska-daniel/amcp-pylib",
    version="0.1.0",
    author="Daniel Dolejska",
    author_email="dolejskad@gmail.com",
    description="AMCP (Advanced Media Control Protocol) Client Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=[
        "core",
        "core.syntax",
        "module",
        "response",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia :: Video",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
