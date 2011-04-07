# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
from urllib import urlencode

from ox.utils import json
from ox.cache import readUrl, readUrlUnicode
from ox import findRe, decodeHtml


def getId(url):
    return url.split("/")[-1]

def getUrl(id):
    return "http://en.wikipedia.org/wiki/%s" % id


def getMovieId(title, director='', year=''):
    query = '"%s" film %s %s' % (title, director, year)
    result = find(query, 1)
    if result:
        return result[0][1]
    return ''

def getUrlByImdbId(imdbId):
    query = '"%s"'% imdbId
    result = find(query)
    if result:
        url = result[0][1]
        data = getMovieData(url)
        if 'imdb_id' in data:
            return url
    return ""

def getUrlByImdb(imdbId):
    # deprecated, use getUrlByImdbId()
    return getUrlByImdbId(imdbId)

def getUrlByAllmovieId(allmovieId):
    query = '"amg_id = 1:%s"'% allmovieId
    result = find(query)
    if result:
        url = result[0][1]
        return url
    return ''

def getWikiData(wikipediaUrl):
    url = wikipediaUrl.replace('wikipedia.org/wiki/', 'wikipedia.org/w/index.php?title=')
    url = "%s&action=raw" % url
    data = readUrl(url).decode('utf-8')
    return data

def getMovieData(wikipediaUrl):
    if not wikipediaUrl.startswith('http'): wikipediaUrl = getUrl(wikipediaUrl)
    data = getWikiData(wikipediaUrl)
    filmbox_data = findRe(data, '''\{\{[Ii]nfobox.[Ff]ilm(.*?)\n\}\}''')
    filmbox = {}
    _box = filmbox_data.strip().split('\n|')
    if len(_box) == 1:
        _box = _box[0].split('|\n')
    for row in _box:
        d = row.split('=')
        if len(d) == 2:
            key = d[0].strip()
            if key[0] == '|':
                key = key[1:]
            value = d[1].strip()
            filmbox[key.strip()] = value

    if 'Allmovie movie' in data:
        filmbox['amg_id'] = findRe(data, 'Allmovie movie\|.*?(\d+)')
    elif 'amg_id' in filmbox and filmbox['amg_id'].startswith('1:'):
        filmbox['amg_id'] = filmbox['amg_id'][2:]

    r = re.compile('{{IMDb title\|(\d{7})', re.IGNORECASE).findall(data)
    if r:
        filmbox['imdb_id'] = r[0]
    r = re.compile('{{mojo title\|(.*?)\|', re.IGNORECASE).findall(data)
    if r:
        filmbox['mojo_id'] = r[0]

    r = re.compile('{{rotten-tomatoes\|(.*?)\|', re.IGNORECASE).findall(data)
    if r:
        filmbox['rottentomatoes_id'] = r[0]
    if 'google video' in data:
        filmbox['google_video_id'] = findRe(data, 'google video\|.*?(\d*?)\|')
    if 'DEFAULTSORT' in data:
        filmbox['title_sort'] = findRe(data, '''\{\{DEFAULTSORT:(.*?)\}\}''')
    return filmbox

def getImageUrl(name):
    data = readUrlUnicode('http://en.wikipedia.org/wiki/Image:' + name)
    url = findRe(data, 'href="(http://upload.wikimedia.org/.*?)"')
    return url

def getPosterUrl(wikipediaUrl):
    if not wikipediaUrl.startswith('http'): wikipediaUrl = getUrl(wikipediaUrl)
    data = getMovieData(wikipediaUrl)
    if 'image' in data:
        return getImageUrl(data['image'])
    return ''

def getMoviePoster(wikipediaUrl):
    # deprecated, use getPosterUrl()
    return getPosterUrl(wikipediaUrl)

def getAllmovieId(wikipediaUrl):
    data = getMovieData(wikipediaUrl)
    return data.get('amg_id', '')

def find(query, max_results=10):
    query = {'action': 'query', 'list':'search', 'format': 'json',
             'srlimit': max_results, 'srwhat': 'text', 'srsearch': query.encode('utf-8')}
    url = "http://en.wikipedia.org/w/api.php?" + urlencode(query)
    data = readUrl(url)
    if not data:
        data  = readUrl(url, timeout=0)
    result = json.loads(data)
    results = []
    if result and 'query' in result:
        for r in result['query']['search']:
            title = r['title']
            url = "http://en.wikipedia.org/wiki/%s" % title.replace(' ', '_')
            results.append((title, url, ''))
    return results

