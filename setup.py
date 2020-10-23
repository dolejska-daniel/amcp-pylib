#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="amcp_pylib",
    url="https://github.com/dolejska-daniel/amcp-pylib",
    version="0.2.2",
    author="Daniel Dolejska",
    author_email="dolejskad@gmail.com",
    description="AMCP (Advanced Media Control Protocol) Client Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Video",
        "Topic :: Utilities",
    ],
)


