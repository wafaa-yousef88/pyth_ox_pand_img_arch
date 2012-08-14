# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
import urllib

import ox
from ox import strip_tags, decodeHtml

DEFAULT_MAX_RESULTS = 10
DEFAULT_TIMEOUT = 24*60*60

def read_url(url, data=None, headers=ox.net.DEFAULT_HEADERS, timeout=DEFAULT_TIMEOUT):
    return ox.cache.read_url(url, data, headers, timeout, unicode=True)

def quote_plus(s):
    if not isinstance(s, str):
        s = s.encode('utf-8')
    return urllib.quote_plus(s)

def find(query, max_results=DEFAULT_MAX_RESULTS, timeout=DEFAULT_TIMEOUT):
    """
    Return max_results tuples with title, url, description 

    >>> find("The Matrix site:imdb.com", 1)[0][0]
    u'The Matrix (1999) - IMDb'

    >>> find("The Matrix site:imdb.com", 1)[0][1]
    u'http://www.imdb.com/title/tt0133093/'
    """
    url = 'http://google.com/search?q=%s' % quote_plus(query)
    data = read_url(url, timeout=timeout)
    results = []
    data = re.sub('<span class="f">(.*?)</span>', '\\1', data)
    for a in re.compile(
        '<a href="(\S+?)" class=l .*?>(.*?)</a>.*?<span class="st">(.*?)<\/span>'
    ).findall(data):
        results.append((strip_tags(decodeHtml(a[1])), a[0], strip_tags(decodeHtml(a[2]))))
        if len(results) >= max_results:
            break
    return results

