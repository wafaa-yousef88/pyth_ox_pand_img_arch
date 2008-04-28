# -*- coding: utf-8 -*-
# vi:si:et:sw=2:sts=2:ts=2
import gzip
import StringIO
import urllib
import urllib2

import chardet


# Default headers for HTTP requests.
DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9b5) Gecko/2008041514 Firefox/3.0b5'}

def openUrl(url, data=None, headers=DEFAULT_HEADERS):
  url = url.replace(' ', '%20')
  req = urllib2.Request(url, data, headers)
  req.add_header('Accept-Encoding', 'gzip')  
  return urllib2.urlopen(req)

def getUrl(url, data=None, headers=DEFAULT_HEADERS):
  f = openUrl(url, data, headers)
  data = f.read()
  f.close()
  if f.headers.get('content-encoding', None) == 'gzip':
    data = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
  return data

def getUrlUnicode(url):
  data = getUrl(url)
  encoding = chardet.detect(data)['encoding']
  if not encoding:
    encoding = 'latin-1'
  return unicode(data, encoding)

