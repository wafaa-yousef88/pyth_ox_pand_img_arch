# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008
from __future__ import division
import os
import hashlib
import sys
import struct 


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
'''
def oshash(filename): 
    try: 
        longlongformat = 'q'  # long long 
        bytesize = struct.calcsize(longlongformat) 
            
        f = open(filename, "rb") 
            
        filesize = os.path.getsize(filename) 
        hash = filesize 
            
        if filesize < 65536: 
           return "SizeError" 
         
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

