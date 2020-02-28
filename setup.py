"""
Build script for thesaurus
Author: Ryan Sheatsley
Date: Thu Feb 27 2020
"""

from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    author="Ryan Sheatsley",
    author_email="ryan@sheatsley.me",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Terminals",
    ],
    description="A command-line interface thesaurus",
    install_requires=["requests"],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="cli command-line terminal thesaurus",
    name="cli-thesaurus",
    packages=find_packages(),
    python_requires=">=3",
    url="https://github.com/sheatsley/thesaurus",
    version="1.0.0b1",
)
