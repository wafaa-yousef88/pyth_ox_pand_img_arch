#!/usr/bin/env python
# vi:si:et:sw=4:sts=4:ts=4
# encoding: utf-8
from distutils.core import setup

def get_bzr_version():
    import os
    rev = int(os.popen('bzr revno').read())
    if rev:
        return u'%s' % rev
    return u'unknown'

setup(
    name="oxlib",
    version="1.0.%s" % get_bzr_version() ,
    description="python-oxlib some tools to build tools",
    author="0x",
    author_email="code@0xdb.org",
    url="http://code.0xdb.org/python-oxlib",
    download_url="http://code.0xdb.org/python-oxlib/download",
    license="GPLv3",
    packages=['oxlib'],
    zip_safe=False,
    keywords = [
    ],
    classifiers = [
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

