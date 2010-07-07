# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
import time
import urllib
import urllib2
import weakref
import threading
import Queue
import simplejson


import ox
from ox import stripTags


'''
usage:
import google
google.find(query)

for result in google.find(query): result

result is title, url, description

google.find(query, max_results)

FIXME: how search depper than first page?
'''
DEFAULT_MAX_RESULTS = 10
DEFAULT_TIMEOUT = 24*60*60

def readUrl(url, data=None, headers=ox.net.DEFAULT_HEADERS, timeout=DEFAULT_TIMEOUT):
    return ox.cache.readUrl(url, data, headers, timeout)

def quote_plus(s):
    return urllib.quote_plus(s.encode('utf-8'))

def find(query, max_results=DEFAULT_MAX_RESULTS, timeout=DEFAULT_TIMEOUT):
    url = "http://www.google.com/search?q=%s" % quote_plus(query)
    data = readUrl(url, timeout=timeout)
    link_re = r'<a href="(?P<url>[^"]*?)" class=l.*?>(?P<name>.*?)</a>' +  \
              r'.*?(?:<br>|<table.*?>)' +  \
              r'(?P<desc>.*?)' + '(?:<font color=#008000>|<a)'
    results = []
    for match in re.compile(link_re, re.DOTALL).finditer(data):
        (name, url, desc) = match.group('name', 'url', 'desc')
        results.append((stripTags(name), url, stripTags(desc)))
    if len(results) > max_results:
        results = results[:max_results]
    return results

def _find(query):
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s' % quote_plus(query)
    results = simplejson.loads(ox.cache.readUrlUnicode(url))['responseData']['results']
    return results

