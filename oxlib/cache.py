# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008
import gzip
import StringIO
import os
import sha
import time
import urlparse
import urllib2

import chardet
import simplejson

import net
from net import DEFAULT_HEADERS, getEncoding


_cache_timeout = 30*24*60*60 # default is 30 days

def status(url, data=None, headers=DEFAULT_HEADERS, timeout=_cache_timeout):
    '''
      >>> status('http://google.com')
      200
      >>> status('http://google.com/mysearch')
      404
    '''
    headers = getHeaders(url, data, headers)
    return int(headers['status'])

def exists(url, data=None, headers=DEFAULT_HEADERS, timeout=_cache_timeout):
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

def getHeaders(url, data=None, headers=DEFAULT_HEADERS, timeout=_cache_timeout):
    url_cache_file = "%s.headers" % _getUrlCacheFile(url, data, headers)
    url_headers = _loadUrlCache(url_cache_file, timeout)
    if url_headers:
        url_headers = simplejson.loads(url_headers)
    else:
        url_headers = net.getHeaders(url, data, headers)
        _saveUrlHeaders(url_cache_file, url_headers)
    return url_headers

def getUrl(url, data=None, headers=DEFAULT_HEADERS, timeout=_cache_timeout):
    url_cache_file = _getUrlCacheFile(url, data, headers)
    result = _loadUrlCache(url_cache_file, timeout)
    if not result:
        try:
            url_headers, result = net.getUrl(url, data, headers, returnHeaders=True)
        except urllib2.HTTPError, e:
            e.headers['Status'] = "%s" % e.code
            url_headers = dict(e.headers)
            result = e.read()
            if url_headers.get('content-encoding', None) == 'gzip':
                result = gzip.GzipFile(fileobj=StringIO.StringIO(result)).read()
        _saveUrlCache(url_cache_file, result, url_headers)
    return result

def getUrlUnicode(url, data=None, headers=DEFAULT_HEADERS, timeout=_cache_timeout, _getUrl=getUrl):
    data = _getUrl(url, data, headers, timeout)
    encoding = getEncoding(data)
    if not encoding:
        encoding = 'latin-1'
    return unicode(data, encoding)

def _getCacheBase():
    'cache base is eather ~/.ox/cache or can set via env variable oxCACHE'
    return os.environ.get('oxCACHE', os.path.expanduser('~/.ox/cache'))

def _getUrlCacheFile(url, data=None, headers=DEFAULT_HEADERS):
    if data:
        url_hash = sha.sha(url + '?' + data).hexdigest()
    else:
        url_hash = sha.sha(url).hexdigest()
    domain = ".".join(urlparse.urlparse(url)[1].split('.')[-2:])
    return os.path.join(_getCacheBase(), domain, url_hash[:2], url_hash[2:4], url_hash[4:6], url_hash)

def _loadUrlCache(url_cache_file, timeout=_cache_timeout):
    if timeout == 0:
        return None
    if os.path.exists(url_cache_file):
        ctime = os.stat(url_cache_file).st_ctime
        now = time.mktime(time.localtime())
        file_age = now-ctime
        if timeout < 0 or file_age < timeout:
            f = open(url_cache_file)
            data = f.read()
            f.close()
            return data
    return None

def _saveUrlCache(url_cache_file, data, headers):
    folder = os.path.dirname(url_cache_file)
    if not os.path.exists(folder):
        os.makedirs(folder)
    f = open(url_cache_file, 'w')
    f.write(data)
    f.close()
    _saveUrlHeaders("%s.headers" % url_cache_file, headers)

def _saveUrlHeaders(url_cache_file, headers):
    folder = os.path.dirname(url_cache_file)
    if not os.path.exists(folder):
        os.makedirs(folder)
    f = open(url_cache_file, 'w')
    f.write(simplejson.dumps(headers))
    f.close()

