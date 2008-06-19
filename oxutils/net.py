# -*- coding: utf-8 -*-
# vi:si:et:sw=2:sts=2:ts=2
import gzip
import StringIO
import urllib
import urllib2

from chardet.universaldetector import UniversalDetector


# Default headers for HTTP requests.
DEFAULT_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9) Gecko/2008061015 Firefox/3.0',
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

def getUrl(url, data=None, headers=DEFAULT_HEADERS, returnHeaders=False):
  f = openUrl(url, data, headers)
  data = f.read()
  f.close()
  if f.headers.get('content-encoding', None) == 'gzip':
    data = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
  if returnHeaders:
    f.headers['Status'] = "%s" % f.code
    return dict(f.headers), data
  return data

def getUrlUnicode(url):
  data = getUrl(url)
  encoding = getEncoding(data)
  if not encoding:
    encoding = 'latin-1'
  return unicode(data, encoding)

def getEncoding(data):
  detector = UniversalDetector()
  for line in data.split('\n'):
    detector.feed(line)
    if detector.done:
      break
  detector.close()
  return detector.result['encoding']

