# -*- coding: UTF-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re

from ox.cache import getHeaders, readUrl, readUrlUnicode
from ox import findRe, stripTags


def getUrlByImdb(imdb):
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

def get_og(data, key):
    return findRe(data, '<meta property="og:%s".*?content="(.*?)"' % key)

def getData(url):
    data = readUrl(url)
    r = {}
    r['title'] = findRe(data, '<h1 class="movie_title">(.*?)</h1>')
    if '(' in r['title']:
        r['year'] = findRe(r['title'], '\((\d*?)\)')
        r['title'] = stripTags(re.sub('\((\d*?)\)', '', r['title'])).strip()
    r['summary'] = stripTags(findRe(data, '<p id="movieSynopsis" class="movie_synopsis" itemprop="description">(.*?)</p>')).strip()
    r['summary'] = r['summary'].replace('\t', ' ').replace('\n', ' ').replace('  ', ' ').replace('  ', ' ')
    if not r['summary']:
        r['summary'] = get_og(data, 'description')

    meter = re.compile('<span id="all-critics-meter" class="meter(.*?)">(.*?)</span>').findall(data)
    meter = filter(lambda m: m[1].isdigit(), meter)
    if meter:
        r['tomatometer'] = meter[0][1]
    r['rating'] = findRe(data, 'Average Rating: <span>([\d.]+)/10</span>')
    r['user_score'] = findRe(data, '<span class="meter popcorn numeric ">(\d+)</span>')
    r['user_rating'] = findRe(data, 'Average Rating: ([\d.]+)/5')
    poster = get_og(data, 'image')
    if poster and not 'poster_default.gif' in poster:
        r['posters'] = [poster]
    for key in r.keys():
        if not r[key]:
            del r[key]
    return r

