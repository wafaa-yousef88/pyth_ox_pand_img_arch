# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import urllib2
from urllib import quote, unquote
import re
import os
import time

import ox
from ox import findRe, stripTags
from ox.normalize import normalizeTitle, normalizeImdbId
import ox.cache
from ox.cache import readUrl

from siteparser import SiteParser
import google

def readUrl(url, data=None, headers=ox.cache.DEFAULT_HEADERS, timeout=ox.cache.cache_timeout, valid=None):
    headers = headers.copy()
    return ox.cache.readUrl(url, data, headers, timeout)

def readUrlUnicode(url, timeout=ox.cache.cache_timeout):
   return ox.cache.readUrlUnicode(url, _readUrl=readUrl, timeout=timeout)

class Imdb(SiteParser):
    '''
    >>> Imdb('0068646')['title']
    u'The Godfather'

    >>> Imdb('0133093')['title']
    u'The Matrix'
    '''
    regex =  {
        'alternative_titles': {
            'page': 'releaseinfo',
            're': [
                'name="akas".*?<table.*?>(.*?)</table>',
                "td>(.*?)</td>.*?<td>(.*?)</td>"
            ],
            'type': 'list'
        
        },
        'cast': {
            'page': 'combined',
            're': [
                '<td class="nm">.*?>(.*?)</a>.*?<td class="char">(.*?)</td>',
                lambda ll: [stripTags(l) for l in ll]
             ],
            'type': 'list'
        },
        'cinematographers': {
            'page': 'combined',
            're': [
                lambda data: data.split('Series Crew')[0],
                'Cinematography by</a>(.*?)</table>',
                '<a href="/name/.*?/">(.*?)</a>'
            ],
            'type': 'list'
        },
        'connections': {
            'page': 'movieconnections',
            're': '<h5>(.*?)</h5>(.*?)\n\n',
            'type': 'list'
        },
        'countries': {
            'page': 'combined',
            're': [
                '<div class="info"><h5>Country:</h5>.*?<div class="info">',
                #'<a href="/country/.*?">(.*?)</a>', #links changed to work with existing caches, just take all links
                '<a.*?>(.*?)</a>',
            ],
            'type': 'list'
        },
        'creators': {
            'page': 'combined',
            're': [
                '<h5>Creators:</h5>.*?<div class="info-content">(.*?)</div>',
                '<a href="/name/.*?>(.*?)</a>'
            ],
            'type': 'list'
        },
        'directors': {
            'page': 'combined',
            're': [
                lambda data: data.split('Series Crew')[0],
                'Directed by</a>(.*?)</table>',
                '<a href="/name/.*?>(.*?)</a>'
            ],
            'type': 'list'
        },
        'editors': {
            'page': 'combined',
            're': [
                lambda data: data.split('Series Crew')[0],
                'Film Editing by</a>(.*?)</table>',
                '<a href="/name/.*?>(.*?)</a>'
            ],
            'type': 'list'
        },
        'episode_title': {
            'page': 'combined',
            're': '<div id="tn15title">.*?<em>(.*?)</em>',
            'type': 'string'
        },
        'filming_locations': {
            'page': 'locations',
            're': '<a href="/search/title\?locations=.*?">(.*?)</a>',
            'type': 'list'
        },
        'genres': {
            'page': 'combined',
            're': '<a href="/Sections/Genres/.*?/">(.*?)</a>',
            'type': 'list'
        },
        'keywords': {
            'page': 'keywords',
            're': '<a href="/keyword/.*?/">(.*?)</a>',
            'type': 'list'
        },
        'languages': {
            'page': 'combined',
            're': [
                '<div class="info"><h5>Language:</h5>.*?<div class="info">',
                #'<a href="/language/.*?">(.*?)</a>', #links changed to work with existing caches, just take all links
                '<a.*?>(.*?)</a>',
            ],
            'type': 'list'
        },
        'plot': {
            'page': 'plotsummary',
            're': '</div>.*?<p class="plotpar">(.*?)<i>',
            'type': 'string'
        },
        'poster_id': {
            'page': 'combined',
            're': '/primary-photo/media/rm(.*?)/tt',
            'type': 'string'
        },
        'poster_ids': {
            'page': 'posters',
            're': '/unknown-thumbnail/media/rm(.*?)/tt',
            'type': 'list'
        },
        'producers': {
            'page': 'combined',
            're': [
                lambda data: data.split('Series Crew')[0],
                'Produced by</a>(.*?)</table>',
                '<a href="/name/.*?/">(.*?)</a>'
            ],
            'type': 'list'
        },
        'rating': {
            'page': 'combined',
            're': '<div class="starbar-meta">.*?<b>([\d,.]?)/10</b>',
            'type': 'float'
        },
        'release date': {
            'page': 'releaseinfo',
            're': '<a href="/date/(\d{2})-(\d{2})/">.*?</a> <a href="/year/(\d{4})/">',
            'type': 'date'
        },
        'reviews': {
            'page': 'externalreviews',
            're': [
                '<ol>(.*?)</ol>',
                '<li><a href="(http.*?)".*?>(.*?)</a></li>'
            ],
            'type': 'list'
        },
        'runtime': {
            'page': 'combined',
            're': '<h5>Runtime:</h5><div class="info-content">.*?([0-9]+ sec|[0-9]+ min).*?</div>',
            'type': 'string'
        },
        'season': {
            'page': 'combined',
            're': [
                '<h5>Original Air Date:</h5>.*?<div class="info-content">(.*?)</div>',
                '\(Season (\d+), Episode \d+\)',
             ],
            'type': 'int'
        },
        'episode': {
            'page': 'combined',
            're': [
                '<h5>Original Air Date:</h5>.*?<div class="info-content">(.*?)</div>',
                '\(Season \d+, Episode (\d+)\)',
             ],
            'type': 'int'
        },
        'series': {
            'page': 'combined',
            're': '<h5>TV Series:</h5>.*?<a href="/title/tt(\d{7})',
            'type': 'string'
        },
        'original_title': {
            'page': 'combined',
            're': '<h1>(.*?) <span>',
            'type': 'string'
        },
        'trivia': {
            'page': 'trivia',
            're': '<div class="sodatext">(.*?)<br>',
            'type': 'list',
        },
        'votes': {
            'page': 'combined',
            're': '<a href="ratings" class="tn15more">([\d,]*?) votes</a>',
            'type': 'string'
        },
        'writers': {
            'page': 'combined',
            're': [
                lambda data: data.split('Series Crew')[0],
                'Writing credits</a>(.*?)</table>',
                '<a href="/name/.*?/">(.*?)</a>'
            ],
            'type': 'list'
        },
        'year': {
            'page': 'combined',
            're': '="og:title" content=".*?\((\d{4})\).*?"',
            'type': 'int'
        }
    }

    def readUrlUnicode(self, url, timeout):
        return readUrlUnicode(url, timeout)

    def __init__(self, id, timeout=-1):
        #use akas.imdb.com to always get original title:
        #http://www.imdb.com/help/show_leaf?titlelanguagedisplay
        self.baseUrl = "http://akas.imdb.com/title/tt%s/" % id
        super(Imdb, self).__init__(timeout)

        def is_international_title(t):
            if 'usa' in t[1].lower(): return True
            if 'international' in t[1].lower(): return True
            return False
        ititle = filter(is_international_title, self['alternative_titles'])
        if ititle:
            self['english_title'] = ititle[0][0]

        self['title'] = self.get('english_title', self['original_title'])

        if 'title' in self and self['title'].startswith('"') and self['title'].endswith('"'):
            self['title'] = self['title'][1:-1]
        if 'runtime' in self and self['runtime']:
            if 'min' in self['runtime']: base=60
            else: base=1
            self['runtime'] = int(findRe(self['runtime'], '([0-9]+)')) * base
        if 'runtime' in self and not self['runtime']:
            del self['runtime']
        if 'votes' in self: self['votes'] = self['votes'].replace(',', '')
        if 'connections' in self:
            cc={}
            if len(self['connections']) == 2 and isinstance(self['connections'][0], basestring):
                self['connections'] = [self['connections']]
            for rel, data in self['connections']:
                cc[unicode(rel)] = re.compile('<a href="/title/tt(\d{7})/">').findall(data)
            self['connections'] = cc

        for key in ('countries', 'genres'):
            if key in self:
                self[key] = filter(lambda x: x.lower() != 'home', self[key])

        if 'creators' in self:
            self['directors'] = self['creators']
            del self['creators']
        if 'series' in self:
            if 'episode_title' in self:
                self['series_title'] = self['title']
                self['title'] = "%s: %s" % (self['series_title'], self['episode_title'])
            if 'episode_title' in self and 'season' in self and 'episode' in self:
                self['title'] = "%s (S%02dE%02d) %s" % (
                        self['series_title'], self['season'], self['episode'], self['episode_title'])
            for key in ('directors', 'year'):
                if key in self:
                    self['episode_%s'%key] = self[key]
            series = Imdb(self['series'])
            for key in ['directors', 'year']:
                if key in series:
                    self[key] =series[key]
        else:
            for key in ('series_title', 'episode_title', 'season', 'episode'):
                if key in self:
                    del self[key]

class ImdbCombined(Imdb):
    def __init__(self, id, timeout=-1):
        _regex = {}
        for key in self.regex:
            if self.regex[key]['page'] == 'combined':
                _regex[key] = self.regex[key]
        self.regex = _regex
        super(ImdbCombined, self).__init__(id, timeout)

def getMovieId(title, director='', year=''):
    '''
    >>> getMovieId('The Matrix')
    u'0133093'

    >>> getMovieId('2 or 3 Things I Know About Her', 'Jean-Luc Godard')
    u'0060304'

    >>> getMovieId('2 or 3 Things I Know About Her', 'Jean-Luc Godard', '1967')
    u'0060304'
    '''
    if director:
        query = 'site:imdb.com %s "%s" ' % (director, title)
    else:
        query = 'site:imdb.com "%s" ' % title
    if year:
        query += year
    for (name, url, desc) in google.find(query, 5, timeout=-1):
        if url.startswith('http://www.imdb.com/title/tt'):
            return url[28:35]
    return ''

def getMoviePoster(imdbId):
    '''
    >>> getMoviePoster('0133093')
    'http://ia.media-imdb.com/images/M/MV5BMjEzNjg1NTg2NV5BMl5BanBnXkFtZTYwNjY3MzQ5._V1._SX338_SY475_.jpg'

    >>> getMoviePoster('0994352')
    'http://ia.media-imdb.com/images/M/MV5BMjA3NzMyMzU1MV5BMl5BanBnXkFtZTcwNjc1ODUwMg@@._V1._SX594_SY755_.jpg'
    '''
    info = ImdbCombined(imdbId)
    if 'poster_id' in info:
        url = "http://www.imdb.com/rg/action-box-title/primary-photo/media/rm%s/tt%s" % (info['poster_id'], imdbId)
        data = readUrl(url)
        poster = findRe(data, 'img id="primary-img".*?src="(.*?)"')
        return poster
    elif 'series' in info:
        return getMoviePoster(info['series'])
    return ''

def guess(title, director='', timeout=google.DEFAULT_TIMEOUT):
    #FIXME: proper file -> title
    '''
    //this is not needed
    title = title.split('-')[0]
    title = title.split('(')[0]
    title = title.split('.')[0]
    title = title.strip()
    '''
    imdb_url = 'http://www.imdb.com/find?q=%s' % quote(title.encode('utf-8'))
    return_url = ''

    #lest first try google
    #i.e. site:imdb.com Michael Stevens "Sin"
    if director:
        search = 'site:imdb.com %s "%s"' % (director, title)
    else:
        search = 'site:imdb.com "%s"' % title

    for (name, url, desc) in google.find(search, 2, timeout=timeout):
        if url.startswith('http://www.imdb.com/title/tt'):
             return normalizeImdbId(int(ox.intValue(url)))

    try:
        req = urllib2.Request(imdb_url, None, ox.net.DEFAULT_HEADERS)
        u = urllib2.urlopen(req)
        data = u.read()
        return_url = u.url
        u.close()
    except:
        return None
    if return_url.startswith('http://www.imdb.com/title/tt'):
        return return_url[28:35]
    if data:
        imdb_id = findRe(data.replace('\n', ' '), 'Popular Results.*?<ol><li>.*?<a href="/title/tt(.......)')
        if imdb_id:
            return imdb_id

    imdb_url = 'http://www.imdb.com/find?q=%s;s=tt;site=aka' % quote(title.encode('utf-8'))
    req = urllib2.Request(imdb_url, None, ox.net.DEFAULT_HEADERS)
    u = urllib2.urlopen(req)
    data = u.read()
    return_url = u.url
    u.close()
    if return_url.startswith('http://www.imdb.com/title/tt'):
        return return_url[28:35]

    return None

if __name__ == "__main__":
    import json
    print json.dumps(Imdb('0306414'), indent=2)
    #print json.dumps(Imdb('0133093'), indent=2)

