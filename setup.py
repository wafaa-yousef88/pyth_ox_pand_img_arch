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
    name="ox",
    version="2.0.%s" % get_bzr_version() ,
    description="python-ox - the web in a dict",
    author="0x",
    author_email="code@0x2620.org",
    url="http://code.0x2620.org/python-ox",
    download_url="http://code.0x2620.org/python-ox/download",
    license="GPLv3",
    packages=['ox', 'ox.torrent', 'ox.web'],
    keywords = [
    ],
    classifiers = [
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

