# -*- coding: utf-8 -*-
# vi:si:et:sw=2:sts=2:ts=2
# 2008
import os
import sha
import time
import urlparse

import net
from net import DEFAULT_HEADERS


cache_timeout = 30*24*60*60 # default is 30 days

def getUrlUnicode(url):
  data = getUrl(url)
  encoding = chardet.detect(data)['encoding']
  if not encoding:
    encoding = 'latin-1'
  return unicode(data, encoding)

def getUrl(url, data=None, headers=DEFAULT_HEADERS, timeout=cache_timeout):
  url_cache_file = getUrlCacheFile(url, data, headers)
  result = loadUrlCache(url_cache_file, timeout)
  if not result:
    result = net.getUrl(url, data, headers)
    saveUrlCache(url_cache_file, result)
  return result

def getCacheBase():
  'cache base is eather ~/.ox/cache or can set via env variable oxCACHE'
  return os.environ.get('oxCACHE', os.path.expanduser('~/.ox/cache'))

def getUrlCacheFile(url, data=None, headers=DEFAULT_HEADERS):
  if data:
    url_hash = sha.sha(url + '?' + data).hexdigest()
  else:
    url_hash = sha.sha(url).hexdigest()
  domain = ".".join(urlparse.urlparse(url)[1].split('.')[-2:])
  return os.path.join(getCacheBase(), domain, url_hash[:2], url_hash[2:4], url_hash[4:6], url_hash)

def loadUrlCache(url_cache_file, data, timeout=cache_timeout):
  if timeout <= 0:
    return None
  if os.path.exists(url_cache_file):
    ctime = os.stat(url_cache_file).st_ctime
    now = time.mktime(time.localtime())
    file_age = now-ctime
    if file_age < timeout:
      f = open(url_cache_file)
      data = f.read()
      f.close()
      return data
  return None

def saveUrlCache(url_cache_file, data):
  folder = os.path.dirname(url_cache_file)
  if not os.path.exists(folder):
    os.makedirs(folder)
  f = open(url_cache_file, 'w')
  f.write(data)
  f.close()

