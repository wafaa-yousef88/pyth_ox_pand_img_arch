# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008
import os
import gzip
import StringIO
import struct
import urllib
import urllib2

from chardet.universaldetector import UniversalDetector


DEBUG = False
# Default headers for HTTP requests.
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Encoding': 'gzip'
}

def status(url, data=None, headers=DEFAULT_HEADERS):
    try:
        f = open_url(url, data, headers)
        s = f.code
    except urllib2.HTTPError, e:
        s = e.code
    return s

def exists(url, data=None, headers=DEFAULT_HEADERS):
    s = status(url, data, headers)
    if s >= 200 and s < 400:
        return True
    return False

def get_headers(url, data=None, headers=DEFAULT_HEADERS):
    try:
        f = open_url(url, data, headers)
        f.headers['Status'] = "%s" % f.code
        headers = f.headers
        f.close()
    except urllib2.HTTPError, e:
        e.headers['Status'] = "%s" % e.code
        headers = e.headers
    return dict(headers)

def open_url(url, data=None, headers=DEFAULT_HEADERS):
    url = url.replace(' ', '%20')
    req = urllib2.Request(url, data, headers)
    return urllib2.urlopen(req)

def read_url(url, data=None, headers=DEFAULT_HEADERS, return_headers=False, unicode=False):
    if DEBUG:
        print 'ox.net.read_url', url
    f = open_url(url, data, headers)
    result = f.read()
    f.close()
    if f.headers.get('content-encoding', None) == 'gzip':
        result = gzip.GzipFile(fileobj=StringIO.StringIO(result)).read()
    if unicode:
        encoding = detect_encoding(result)
        if not encoding:
            encoding = 'latin-1'
        result = result.decode(encoding)
    if return_headers:
        f.headers['Status'] = "%s" % f.code
        return dict(f.headers), result
    return result

def detect_encoding(data):
    if 'content="text/html; charset=utf-8"' in data or \
        'meta charset="utf-8"' in data.lower():
        return 'utf-8'
    elif 'content="text/html; charset=iso-8859-1"' in data:
        return 'iso-8859-1'
    detector = UniversalDetector()
    for line in data.split('\n'):
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding']

def save_url(url, filename, overwrite=False):
    if not os.path.exists(filename) or overwrite:
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        data = read_url(url)
        f = open(filename, 'w')
        f.write(data)
        f.close()

def oshash(url):
    def get_size(url):
        req = urllib2.Request(url, headers=DEFAULT_HEADERS.copy())
        req.get_method = lambda : 'HEAD'
        u = urllib2.urlopen(req)
        if u.code != 200 or not 'Content-Length' in u.headers:
            raise IOError
        return int(u.headers['Content-Length'])

    def get_range(url, start, end):
        headers = DEFAULT_HEADERS.copy()
        headers['Range'] = 'bytes=%s-%s' % (start, end)
        req = urllib2.Request(url, headers=headers)
        u = urllib2.urlopen(req)
        return u.read() 

    try:
        longlongformat = 'q'  # long long
        bytesize = struct.calcsize(longlongformat)

        filesize = get_size(url)
        hash = filesize
        head = get_range(url, 0, min(filesize, 65536))
        if filesize > 65536:
            tail = get_range(url, filesize-65536, filesize)
        if filesize < 65536:
            for offset in range(0, filesize, bytesize):
                buffer = head[offset:offset+bytesize]
                (l_value,)= struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF #cut off 64bit overflow
        else:
            for offset in range(0, 65536, bytesize):
                buffer = head[offset:offset+bytesize]
                (l_value,)= struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF #cut of 64bit overflow
            for offset in range(0, 65536, bytesize):
                buffer = tail[offset:offset+bytesize]
                (l_value,)= struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF
        returnedhash =  "%016x" % hash
        return returnedhash
    except(IOError):
        return "IOError"

