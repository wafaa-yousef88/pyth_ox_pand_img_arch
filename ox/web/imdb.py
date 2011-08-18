# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import urllib2
import urllib
import re
import os
import time
import unicodedata

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
        'aspectratio': {
            'page': 'combined',
            're': 'Aspect Ratio:</h5><div class="info-content">([\d\.]+)',
            'type': 'float',
        },
        'budget': {
            'page': 'business',
            're': [
                '<h5>Budget</h5>(.*?)<br',
                lambda data: findRe(ox.decodeHtml(data).replace(',', ''), '\d+')
            ],
            'type': 'int'
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
        'gross': {
            'page': 'business',
            're': [
                '<h5>Gross</h5>(.*?)\(',
                lambda data: findRe(data.replace(',', ''), '\d+')
            ],
            'type': 'int'
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
            're': '<div class="starbar-meta">.*?<b>([\d,.]+?)/10</b>',
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
            're': '<div class="sodatext">(.*?)<br',
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
       
        url = self.baseUrl + 'combined' 
        if '<title>IMDb: Page not found</title>' in self.readUrlUnicode(url, timeout=-1):
            return
        if "<p>We're sorry, something went wrong.</p>" in self.readUrlUnicode(url, timeout=-1):
            time.sleep(1)
            super(Imdb, self).__init__(0)

        #only list one country per alternative title

        def is_international_title(t):
            if 'working title' in t[1].lower(): return False
            if 'complete title' in t[1].lower(): return False
            if t[1].lower() == 'usa': return True
            if 'international' in t[1].lower(): return True
            if 'english title' in t[1].lower(): return True
            return False
        ititle = filter(is_international_title, self.get('alternative_titles', []))
        if ititle:
            self['english_title'] = ititle[0][0]

        self['title'] = self.get('english_title', self['original_title'])

        for t in ('title', 'english_title', 'original_title'):
            if t in self and self[t].startswith('"') and self[t].endswith('"'):
                self[t] = self[t][1:-1]

        if 'alternative_titles' in self:
            self['alternative_titles'] = [[t[0],
                                           t[1].split(' / ')[0].split('(')[0].strip()]
                                          for t in self['alternative_titles']]

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
                self['title'] = "%s (S01) %s" % (self['series_title'], self['episode_title'])
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

        if 'budget' in self and 'gross' in self:
            self['profit'] = self['gross'] - self['budget']

class ImdbCombined(Imdb):
    def __init__(self, id, timeout=-1):
        _regex = {}
        for key in self.regex:
            if self.regex[key]['page'] == 'combined':
                _regex[key] = self.regex[key]
        self.regex = _regex
        super(ImdbCombined, self).__init__(id, timeout)

def getMovieIdByTitle(title, timeout=-1):
    '''
    This only works for exact title matches from the data dump
    Usually in the format
        Title (Year)
        "Series Title" (Year) {(#Season.Episode)}
        "Series Title" (Year) {Episode Title (#Season.Episode)}

    If there is more than one film with that title for the year
        Title (Year/I)

    >>> getMovieIdByTitle(u'"Father Knows Best" (1954) {(#5.34)}')
    u'1602860'

    >>> getMovieIdByTitle(u'The Matrix (1999)')
    u'0133093'

    >>> getMovieIdByTitle(u'Little Egypt (1951)')
    u'0043748'

    >>> getMovieIdByTitle(u'Little Egypt (1897/I)')
    u'0214882'
    
    >>> getMovieIdByTitle(u'Little Egypt')
    None 

    >>> getMovieIdByTitle(u'"Dexter" (2006) {Father Knows Best (#1.9)}')
    u'0866567'
    '''
    params = {'s':'tt','q': title}
    if isinstance(title, unicode):
        try:
            params['q'] = unicodedata.normalize('NFKC', params['q']).encode('latin-1')
        except:
            params['q'] = params['q'].encode('utf-8')
    params = urllib.urlencode(params)
    url = "http://akas.imdb.com/find?" + params
    data = readUrlUnicode(url, timeout=timeout)
    #if search results in redirect, get id of current page
    r = '<meta property="og:url" content="http://www.imdb.com/title/tt(\d{7})/" />'
    results = re.compile(r).findall(data)    
    if results:
        return results[0]
    return None
 
def getMovieId(title, director='', year='', timeout=-1):
    '''
    >>> getMovieId('The Matrix')
    u'0133093'

    >>> getMovieId('2 or 3 Things I Know About Her', 'Jean-Luc Godard')
    u'0060304'

    >>> getMovieId('2 or 3 Things I Know About Her', 'Jean-Luc Godard', '1967')
    u'0060304'

    >>> getMovieId(u"Histoire(s) du cinema: Le controle de l'univers", 'Jean-Luc Godard')
    u'0179214'

    >>> getMovieId(u"Histoire(s) du cinéma: Le contrôle de l'univers", 'Jean-Luc Godard')
    u'0179214'
    '''
    imdbId = {
        (u'Le jour se l\xe8ve', u'Marcel Carn\xe9'): '0031514',
        (u'Wings', u'Larisa Shepitko'): '0061196',
        (u'The Ascent', u'Larisa Shepitko'): '0075404',
        (u'Fanny and Alexander', u'Ingmar Bergman'): '0083922',
        (u'Torment', u'Alf Sj\xf6berg'): '0036914',
        (u'Crisis', u'Ingmar Bergman'): '0038675',
        (u'To Joy', u'Ingmar Bergman'): '0043048',
        (u'Humain, trop humain', u'Louis Malle'): '0071635',
        (u'Place de la R\xe9publique', u'Louis Malle'): '0071999',
        (u'God\u2019s Country', u'Louis Malle'): '0091125',
        (u'Flunky, Work Hard', u'Mikio Naruse'): '0022036',
        (u'The Courtesans of Bombay', u'Richard Robbins') : '0163591',
        (u'Je tu il elle', u'Chantal Akerman') : '0071690',
        (u'Hotel Monterey', u'Chantal Akerman') : '0068725',
        (u'No Blood Relation', u'Mikio Naruse') : '023261',
        (u'Apart from You', u'Mikio Naruse') : '0024214',
        (u'Every-Night Dreams', u'Mikio Naruse') : '0024793',
        (u'Street Without End', u'Mikio Naruse') : '0025338',
        (u'Sisters of the Gion', u'Kenji Mizoguchi') : '0027672',
        (u'Osaka Elegy', u'Kenji Mizoguchi') : '0028021',
        (u'Blaise Pascal', u'Roberto Rossellini') : '0066839',
        (u'Japanese Girls at the Harbor', u'Hiroshi Shimizu') : '0160535',
        (u'The Private Life of Don Juan', u'Alexander Korda') : '0025681',
        (u'Last Holiday', u'Henry Cass') : '0042665',
        (u'A Colt Is My Passport', u'Takashi  Nomura') : '0330536',
        (u'Androcles and the Lion', u'Chester Erskine') : '0044355',
        (u'Major Barbara', u'Gabriel Pascal') : '0033868',
        (u'Come On Children', u'Allan King') : '0269104',

        (u'Jimi Plays Monterey & Shake! Otis at Monterey', u'D. A. Pennebaker and Chris Hegedus') : '',
        (u'Martha Graham: Dance on Film', u'Nathan Kroll') : '',
    }.get((title, director), None)
    if imdbId:
        return imdbId
    params = {'s':'tt','q': title}
    if director:
        params['q'] = u'"%s" %s' % (title, director)
    if year:
        params['q'] = u'"%s (%s)" %s' % (title, year, director)
    google_query = "site:imdb.com %s" % params['q']
    if isinstance(params['q'], unicode):
        try:
            params['q'] = unicodedata.normalize('NFKC', params['q']).encode('latin-1')
        except:
            params['q'] = params['q'].encode('utf-8')
    params = urllib.urlencode(params)
    url = "http://akas.imdb.com/find?" + params
    #print url

    data = readUrlUnicode(url, timeout=timeout)
    #if search results in redirect, get id of current page
    r = '<meta property="og:url" content="http://www.imdb.com/title/tt(\d{7})/" />'
    results = re.compile(r).findall(data)    
    if results:
        return results[0]
    #otherwise get first result
    r = '<td valign="top">.*?<a href="/title/tt(\d{7})/"'
    results = re.compile(r).findall(data)
    if results:
        return results[0]

    #print (title, director), ": '',"
    #print google_query
    results = google.find(google_query)
    if results:
        return findRe(results[0][1], 'title/tt(\d{7})')
    #or nothing
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

def guess(title, director='', timeout=-1):
    return getMovieId(title, director, timeout=timeout)

if __name__ == "__main__":
    import json
    print json.dumps(Imdb('0306414'), indent=2)
    #print json.dumps(Imdb('0133093'), indent=2)

