#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="amcp_pylib",
    url="https://github.com/dolejska-daniel/amcp-pylib",
    version="0.2.0",
    author="Daniel Dolejska",
    author_email="dolejskad@gmail.com",
    description="AMCP (Advanced Media Control Protocol) Client Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Multimedia :: Video",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
