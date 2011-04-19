# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008
from __future__ import division
import os
import hashlib
import re
import sys
import struct
import subprocess

from ox.utils import json

__all__ = ['sha1sum', 'oshash', 'avinfo', 'makedirs']

def sha1sum(filename):
    sha1 = hashlib.sha1()
    file=open(filename)
    buffer=file.read(4096)
    while buffer:
        sha1.update(buffer)
        buffer=file.read(4096)
    file.close()
    return sha1.hexdigest()

'''
    os hash - http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes
    plus modification for files < 64k, buffer is filled with file data and padded with 0
'''
def oshash(filename):
    try:
        longlongformat = 'q'  # long long
        bytesize = struct.calcsize(longlongformat)

        f = open(filename, "rb")

        filesize = os.path.getsize(filename)
        hash = filesize
        if filesize < 65536:
            for x in range(int(filesize/bytesize)):
                buffer = f.read(bytesize)
                (l_value,)= struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number
        else:
            for x in range(int(65536/bytesize)):
                buffer = f.read(bytesize)
                (l_value,)= struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number
            f.seek(max(0,filesize-65536),0)
            for x in range(int(65536/bytesize)):
                buffer = f.read(bytesize)
                (l_value,)= struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF
        f.close()
        returnedhash =  "%016x" % hash
        return returnedhash
    except(IOError):
        return "IOError"

def avinfo(filename):
    if os.path.getsize(filename):
        p = subprocess.Popen(['ffmpeg2theora', '--info', filename],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        info, error = p.communicate()
        try:
            info = json.loads(info)
        except:
            #remove metadata, can be broken
            reg = re.compile('"metadata": {.*?},', re.DOTALL)
            info = re.sub(reg, '', info)
            info = json.loads(info)
        if 'video' in info:
            for v in info['video']:
                if not 'display_aspect_ratio' in v and 'width' in v:
                    v['display_aspect_ratio'] = '%d:%d' % (v['width'], v['height'])
                    v['pixel_aspect_ratio'] = '1:1'
        return info

    return {'path': filename, 'size': 0}

def makedirs(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError, e:
            if e.errno != 17:
                raise
