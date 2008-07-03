#!/usr/bin/env python
# vi:si:et:sw=4:sts=4:ts=4
# encoding: utf-8
from setuptools import setup, find_packages

setup(
    name="oxlib",
    version="0.1",

    description="collection of utils used to work with python",
    author="0x",
    author_email="code@0xdb.org",
    url="http://code.0xdb.org/oxlib",
    download_url="http://code.0xdb.org/oxlib/download",
    license="GPLv3",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
          'chardet',
    ],
    keywords = [
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

