#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="amcp_pylib",
    url="https://github.com/dolejska-daniel/amcp-pylib",
    version="0.1.2",
    author="Daniel Dolejska",
    author_email="dolejskad@gmail.com",
    description="AMCP (Advanced Media Control Protocol) Client Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        # Development
        "Development Status :: 4 - Beta",
        # Audience
        "Intended Audience :: Developers",
        # License
        "License :: OSI Approved :: MIT License",
        # Language
        "Natural Language :: English",
        # Topics
        "Topic :: Multimedia :: Video",
        # OS
        "Operating System :: OS Independent",
        # Programming language
        "Programming Language :: Python :: 3",
    ],
)
