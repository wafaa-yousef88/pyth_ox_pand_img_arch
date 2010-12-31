# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
import urllib
import ox
from ox import stripTags, decodeHtml
from ox.utils import json
from ox.cache import readUrlUnicode


def find(query, timeout=ox.cache.cache_timeout):
    params = urllib.urlencode({'q': query})
    if isinstance(query, unicode):
        query = query.encode('utf-8')
    url = 'http://duckduckgo.com/html/?' + params
    data = readUrlUnicode(url, timeout=timeout)
    results = []
    regex = '<a .*?class="l le" href="(.+?)">(.*?)</a>.*?<div class="cra">(.*?)</div>'
    for r in re.compile(regex, re.DOTALL).findall(data):
        results.append((stripTags(decodeHtml(r[1])), r[0], stripTags(decodeHtml(r[2]))))
    return results
    
