#!/usr/bin/env python
# vi:si:et:sw=2:sts=2:ts=2
# encoding: utf-8
from setuptools import setup, find_packages

setup(
  name="oxutils",
  version="0.1",

  description="collection of utils used to work with python",
  author="ox",
  author_email="utils@0xdb.org",
  url="http://code.0xdb.org/python-oxutils",
  download_url="http://code.0xdb.org/python-oxutils/download",
  license="GPL",
  packages=find_packages(),
  zip_safe=False,
  keywords = [
  ],
  classifiers = [
      'Development Status :: 3 - Alpha',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
  ],
  )

