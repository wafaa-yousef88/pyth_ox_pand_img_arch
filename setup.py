#!/usr/bin/env python
# vi:si:et:sw=4:sts=4:ts=4
# encoding: utf-8
try:
    from setuptools import setup
except:
    from distutils.core import setup

def get_bzr_version():
    import os
    import re
    info = os.path.join(os.path.dirname(__file__), '.bzr/branch/last-revision')
    changelog = os.path.join(os.path.dirname(__file__), 'debian/changelog')
    if os.path.exists(info):
        f = open(info)
        rev = int(f.read().split()[0])
        f.close()
        if rev:
            return u'%s' % rev
    elif os.path.exists(changelog):
        f = open(changelog)
        head = f.read().strip().split('\n')[0]
        f.close()
        rev = re.compile('\d+\.\d+\.(\d+)').findall(head)
        if rev:
            return u"%s" % rev[0]
    return u'unknown'

setup(
    name="ox",
    version="2.1.%s" % get_bzr_version() ,
    description="python-ox - the web in a dict",
    author="0x2620",
    author_email="0x2620@0x2620.org",
    url="http://code.0x2620.org/python-ox",
    download_url="http://code.0x2620.org/python-ox/download",
    license="GPLv3",
    packages=['ox', 'ox.django', 'ox.django.api', 'ox.torrent', 'ox.web'],
    install_requires=['chardet', 'feedparser'],
    keywords = [
    ],
    classifiers = [
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

