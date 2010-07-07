# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import urllib2
from urllib import quote, unquote
import re
import os
import time

import ox
from ox import findRe
from ox.normalize import normalizeTitle, normalizeImdbId

from siteparser import SiteParser
import google

class Imdb(SiteParser):
    regex =  {
        'cast': {
            'page': 'combined',
            're': '<td class="nm">.*?>(.*?)</a>.*?<td class="char">(.*?)</td>',
            'type': 'list'
        },
        'cinematographers': {
            'page': 'combined',
            're': [
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
            're': '<a href="/Sections/Countries/.*?/">(.*?)</a>',
            'type': 'list'
        },
        'directors': {
            'page': 'combined',
            're': [
                'Directed by</a>(.*?)</table>',
                '<a href="/name/.*?/">(.*?)</a>'
            ],
            'type': 'list'
        },
        'editors': {
            'page': 'combined',
            're': [
                'Film Editing by</a>(.*?)</table>',
                '<a href="/name/.*?/">(.*?)</a>'
            ],
            'type': 'list'
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
            're': '<a href="/Sections/Languages/.*?/">(.*?)</a>',
            'type': 'list'
        },
        'plot': {
            'page': 'plotsummary',
            're': '<p class="plotpar">(.*?)<i>',
            'type': 'string'
        },
        'poster_id': {
            'page': 'combined',
            're': '/primary-photo/media/rm(.*?)/tt',
            'type': 'list'
        },
        'poster_ids': {
            'page': 'posters',
            're': '/unknown-thumbnail/media/rm(.*?)/tt',
            'type': 'list'
        },
        'producers': {
            'page': 'combined',
            're': [
                'Produced by</a>(.*?)</table>',
                '<a href="/name/.*?/">(.*?)</a>'
            ],
            'type': 'list'
        },
        'rating': {
            'page': 'combined',
            're': '<div class="starbar-meta">.*?<b>(.*?)/10</b>',
            'type': 'float'
        },
        'release_date': {
            'page': 'releaseinfo',
            're': '<a href="/date/(\d{2})-(\d{2})/">.*?</a> <a href="/year/(\d{4})/">',
            'type': 'date'
        },
        'runtime': {
            'page': 'combined',
            're': '<h5>Runtime:</h5><div class="info-content">.*?([0-9]+ sec|[0-9]+ min).*?</div>',
            'type': 'string'
        },
        'title': {
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
            're': '<a href="ratings" class="tn15more">(.*?) votes</a>',
            'type': 'string'
        },
        'writers': {
            'page': 'combined',
            're': [
                'Writing credits</a>(.*?)</table>',
                '<a href="/name/.*?/">(.*?)</a>'
            ],
            'type': 'list'
        },
        'year': {
            'page': 'combined',
            're': '<a href="/year/(\d{4})/">',
            'type': 'int'
        }
    }

    def __init__(self, id):
        self.baseUrl = "http://www.imdb.com/title/tt%s/" % id
        super(Imdb, self).__init__()

        if 'runtime' in self:
            if 'min' in self['runtime']: base=60
            else: base=1
            self['runtime'] = int(findRe(self['runtime'], '([0-9]+)')) * base

        if 'connections' in self:
            cc={}
            for rel, data in self['connections']:
                cc[unicode(rel)] = re.compile('<a href="/title/tt(\d{7})/">').findall(data)
            self['connections'] = cc

def guess(title, director='', timeout=google.DEFAULT_TIMEOUT):
    #FIXME: proper file -> title
    title = title.split('-')[0]
    title = title.split('(')[0]
    title = title.split('.')[0]
    title = title.strip()
    imdb_url = 'http://www.imdb.com/find?q=%s' % quote(title.encode('utf-8'))
    return_url = ''

    #lest first try google
    #i.e. site:imdb.com Michael Stevens Sin
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

