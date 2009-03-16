# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008
import os
import hashlib

def sha1sum(filename):
    sha1 = hashlib.sha1()
    file=open(filename)
    buffer=file.read(4096)
    while buffer:
        sha1.update(buffer)
        buffer=file.read(4096)
    file.close()
    return sha1.hexdigest()


