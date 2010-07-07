# -*- coding: UTF-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re

from ox.cache import getHeaders, readUrl, readUrlUnicode
from ox import findRe, stripTags


def readUrlByImdb(imdb):
    #this would also wor but does not cache:
    '''
    from urllib2 import urlopen
    u = urlopen(url)
    return u.url
    '''
    url = "http://www.rottentomatoes.com/alias?type=imdbid&s=%s" % imdb
    data = readUrl(url)
    if "movie_title" in data:
        movies = re.compile('(/m/.*?/)').findall(data)
        if movies:
            return "http://www.rottentomatoes.com" + movies[0]
    return None

def getData(url):
    data = readUrlUnicode(url)
    r = {}
    r['title'] = findRe(data, '<h1 class="movie_title">(.*?)</h1>')
    if '(' in r['title']:
        r['year'] = findRe(r['title'], '\((\d*?)\)')
        r['title'] = re.sub('\((\d*?)\)', '', r['title']).strip()
    r['synopsis'] = findRe(data, '<span id="movie_synopsis_all".*?>(.*?)</span>')
    r['average rating'] = findRe(data, '<div id="bubble_allCritics".*?>(.*?)</div>').strip()
    return r

