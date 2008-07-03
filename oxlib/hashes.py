# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL written 2008 by j@pad.ma
import sha
import os

def sha1sum(filename):
    sha1 = sha.new()
    file=open(filename)
    buffer=file.read(4096)
    while buffer:
        sha1.update(buffer)
        buffer=file.read(4096)
    file.close()
    return sha1.hexdigest()


