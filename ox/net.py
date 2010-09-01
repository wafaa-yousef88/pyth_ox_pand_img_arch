# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008
import os
import gzip
import StringIO
import urllib
import urllib2

from chardet.universaldetector import UniversalDetector


# Default headers for HTTP requests.
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100823 Firefox/4.0.1',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Encoding': 'gzip'
}

def status(url, data=None, headers=DEFAULT_HEADERS):
    try:
        f = openUrl(url, data, headers)
        s = f.code
    except urllib2.HTTPError, e:
        s = e.code
    return s

def exists(url, data=None, headers=DEFAULT_HEADERS):
    s = status(url, data, headers)
    if s >= 200 and s < 400:
        return True
    return False

def getHeaders(url, data=None, headers=DEFAULT_HEADERS):
    try:
        f = openUrl(url, data, headers)
        f.headers['Status'] = "%s" % f.code
        headers = f.headers
        f.close()
    except urllib2.HTTPError, e:
        e.headers['Status'] = "%s" % e.code
        headers = e.headers
    return dict(headers)

def openUrl(url, data=None, headers=DEFAULT_HEADERS):
    url = url.replace(' ', '%20')
    req = urllib2.Request(url, data, headers)
    return urllib2.urlopen(req)

def readUrl(url, data=None, headers=DEFAULT_HEADERS, returnHeaders=False):
    f = openUrl(url, data, headers)
    data = f.read()
    f.close()
    if f.headers.get('content-encoding', None) == 'gzip':
        data = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
    if returnHeaders:
        f.headers['Status'] = "%s" % f.code
        return dict(f.headers), data
    return data

def readUrlUnicode(url):
    data = readUrl(url)
    encoding = getEncoding(data)
    if not encoding:
        encoding = 'latin-1'
    return unicode(data, encoding)

def getEncoding(data):
    if 'content="text/html; charset=utf-8"' in data:
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

def saveUrl(url, filename, overwrite=False):
    if not os.path.exists(filename) or overwrite:
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        data = readUrl(url)
        f = open(filename, 'w')
        f.write(data)
        f.close()

