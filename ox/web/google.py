# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
import time
import urllib
import urllib2
import weakref
import threading
import Queue

import ox
from ox import stripTags
from ox.utils import json


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
    if not isinstance(s, str):
        s = s.encode('utf-8')
    return urllib.quote_plus(s)

def find(query, max_results=DEFAULT_MAX_RESULTS, timeout=DEFAULT_TIMEOUT):
    """
    Return max_results tuples with title, url, description 

    >>> find("The Matrix site:imdb.com", 1)[0][0]
    u'The Matrix (1999)'

    >>> find("The Matrix site:imdb.com", 1)[0][1]
    u'http://www.imdb.com/title/tt0133093/'
    """
    _results =  _find(query)
    results = []
    for r in _results:
        results.append((r['titleNoFormatting'], r['unescapedUrl'], stripTags(r['content'])))
        if len(results) >= max_results:
            break
    return results

def _find(query, timeout=DEFAULT_TIMEOUT):
    """
    Return parsed json results from google ajax api

    >>> _find("The Matrix site:imdb.com")[0]['titleNoFormatting']
    u'The Matrix (1999)'

    >>> _find("The Matrix site:imdb.com")[0]['url']
    u'http://www.imdb.com/title/tt0133093/'
    """
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s' % quote_plus(query)
    results = json.loads(ox.cache.readUrlUnicode(url, timeout=timeout))['responseData']['results']
    return results

