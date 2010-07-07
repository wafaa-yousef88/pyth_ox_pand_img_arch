# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008
import gzip
import hashlib
import os
import StringIO
import time
import urlparse
import urllib2
import sqlite3

import chardet
import simplejson

import net
from net import DEFAULT_HEADERS, getEncoding


cache_timeout = 30*24*60*60 # default is 30 days


def status(url, data=None, headers=DEFAULT_HEADERS, timeout=cache_timeout):
    '''
      >>> status('http://google.com')
      200
      >>> status('http://google.com/mysearch')
      404
    '''
    headers = getHeaders(url, data, headers)
    return int(headers['status'])

def exists(url, data=None, headers=DEFAULT_HEADERS, timeout=cache_timeout):
    '''
      >>> exists('http://google.com')
      True
      >>> exists('http://google.com/mysearch')
      False
    '''
    s = status(url, data, headers, timeout)
    if s >= 200 and s < 400:
        return True
    return False

def getHeaders(url, data=None, headers=DEFAULT_HEADERS, timeout=cache_timeout):
    url_headers = _readUrlCache(url, data, headers, timeout, "headers")
    if url_headers:
        url_headers = simplejson.loads(url_headers)
    else:
        url_headers = net.getHeaders(url, data, headers)
        _saveUrlCache(url, data, -1, url_headers)
    return url_headers

class InvalidResult(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, result, headers):
        self.result = result
        self.headers = headers

def readUrl(url, data=None, headers=DEFAULT_HEADERS, timeout=cache_timeout, valid=None):
    '''
        url     - url to load
        data    - possible post data
        headers - headers to send with request
        timeout - get from cache if cache not older than given seconds, -1 to get from cache
        valid   - function to check if result is ok, its passed result and headers
                  if this function fails, InvalidResult will be raised deal with it in your code 
    '''
    #FIXME: send last-modified / etag from cache and only update if needed
    if isinstance(url, unicode):
        url = url.encode('utf-8')
    result = _readUrlCache(url, data, headers, timeout)
    if not result:
        #print "get data", url
        try:
            url_headers, result = net.readUrl(url, data, headers, returnHeaders=True)
        except urllib2.HTTPError, e:
            e.headers['Status'] = "%s" % e.code
            url_headers = dict(e.headers)
            result = e.read()
            if url_headers.get('content-encoding', None) == 'gzip':
                result = gzip.GzipFile(fileobj=StringIO.StringIO(result)).read()
        if not valid or valid(result, url_headers):
            _saveUrlCache(url, data, result, url_headers)
        else:
            raise InvalidResult(result, url_headers)
    return result

def readUrlUnicode(url, data=None, headers=DEFAULT_HEADERS, timeout=cache_timeout, _readUrl=readUrl, valid=None):
    data = _readUrl(url, data, headers, timeout, valid)
    encoding = getEncoding(data)
    if not encoding:
        encoding = 'latin-1'
    return unicode(data, encoding)

def saveUrl(url, filename, overwrite=False):
    if not os.path.exists(filename) or overwrite:
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        data = readUrl(url)
        f = open(filename, 'w')
        f.write(data)
        f.close()

def _getCacheBase():
    'cache base is eather ~/.ox/cache or can set via env variable oxCACHE'
    return os.environ.get('oxCACHE', os.path.expanduser('~/.ox/cache'))

def _getCacheDB():
    path = _getCacheBase()
    if not os.path.exists(path):
        os.makedirs(path)
    return os.path.join(path, "cache.sqlite")

def _connectDb():
    conn = sqlite3.connect(_getCacheDB(), timeout=10)
    conn.text_factory = str
    return conn

def _createDb(c):
    # Create table and indexes 
    c.execute('''CREATE TABLE IF NOT EXISTS cache (url_hash varchar(42) unique, domain text, url text,
                      post_data text, headers text, created int, data blob, only_headers int)''')
    c.execute('''CREATE INDEX IF NOT EXISTS cache_domain ON cache (domain)''')
    c.execute('''CREATE INDEX IF NOT EXISTS cache_url ON cache (url)''')
    c.execute('''CREATE INDEX IF NOT EXISTS cache_url_hash ON cache (url_hash)''')


def _readUrlCache(url, data, headers=DEFAULT_HEADERS, timeout=-1, value="data"):
    r = None
    if timeout == 0:
        return r

    if data:
        url_hash = hashlib.sha1(url + '?' + data).hexdigest()
    else:
        url_hash = hashlib.sha1(url).hexdigest()

    conn = _connectDb()
    c = conn.cursor()
    _createDb(c)

    sql = 'SELECT %s FROM cache WHERE url_hash=?' % value
    if timeout > 0:
        now = time.mktime(time.localtime())
        t = (url_hash, now-timeout)
        sql += ' AND created > ?'
    else:
        t = (url_hash, )
    if value != "headers":
        sql += ' AND only_headers != 1 '
    c.execute(sql, t)
    for row in c:
        r = row[0]
        if value == 'data':
            r = str(r)
        break

    c.close()
    conn.close()
    return r

def _saveUrlCache(url, post_data, data, headers):
    if post_data:
        url_hash = hashlib.sha1(url + '?' + post_data).hexdigest()
    else:
        url_hash = hashlib.sha1(url).hexdigest()

    domain = ".".join(urlparse.urlparse(url)[1].split('.')[-2:])

    conn = _connectDb()
    c = conn.cursor()

    # Create table if not exists
    _createDb(c)

    # Insert a row of data
    if not post_data: post_data=""
    only_headers = 0
    if data == -1:
        only_headers = 1
        data = ""
    created = time.mktime(time.localtime())
    t = (url_hash, domain, url, post_data, simplejson.dumps(headers), created, sqlite3.Binary(data), only_headers)
    c.execute(u"""INSERT OR REPLACE INTO cache values (?, ?, ?, ?, ?, ?, ?, ?)""", t)

    # Save (commit) the changes and clean up
    conn.commit()
    c.close()
    conn.close()

def migrate_to_db():
    import re
    import os
    import sqlite3
    import glob

    conn = _connectDb()
    c = conn.cursor()
    _createDb(c)

    files = glob.glob(_getCacheBase() + "/*/*/*/*/*")
    _files = filter(lambda x: not x.endswith(".headers"), files)

    for f in _files:
        info = re.compile("%s/(.*?)/../../../(.*)" % _getCacheBase()).findall(f)
        domain = url = info[0][0]
        url_hash = info[0][1]
        post_data = ""
        created = os.stat(f).st_ctime
        fd = open(f, "r")
        data = fd.read()
        fd.close()
        fd = open(f + ".headers", "r")
        headers = fd.read()
        fd.close()
        t = (url_hash, domain, url, post_data, headers, created, sqlite3.Binary(data), 0)
        c.execute(u"""INSERT OR REPLACE INTO cache values (?, ?, ?, ?, ?, ?, ?, ?)""", t)

    conn.commit()
    c.close()
    conn.close()

