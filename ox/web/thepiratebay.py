# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from datetime import datetime
import re
import socket
from urllib import quote, urlencode
from urllib2 import URLError

from ox.cache import readUrl, readUrlUnicode
from ox import findRe, cache, stripTags, decodeHtml, getTorrentInfo, normalizeNewlines
from ox.normalize import normalizeImdbId
import ox

from torrent import Torrent

cache_timeout = 24*60*60 # cache search only for 24 hours

season_episode = re.compile("S..E..", re.IGNORECASE)


def _readUrl(url, data=None, headers=cache.DEFAULT_HEADERS, timeout=cache.cache_timeout, valid=None):
    headers = headers.copy()
    headers['Cookie'] = 'language=en_EN'
    return cache.readUrl(url, data, headers, timeout)

def _readUrlUnicode(url, timeout=cache.cache_timeout):
   return cache.readUrlUnicode(url, _readUrl=_readUrl, timeout=timeout)

def findMovies(query, max_results=10):
    results = []
    next = ["http://thepiratebay.org/search/%s/0/3/200" % quote(query), ]
    page_count = 1
    while next and page_count < 4:
        page_count += 1
        url = next[0]
        if not url.startswith('http'):
            if not url.startswith('/'):
                url = "/" + url
            url = "http://thepiratebay.org" + url
        data = _readUrlUnicode(url, timeout=cache_timeout)
        regexp = '''<tr.*?<td class="vertTh"><a href="/browse/(.*?)".*?<td><a href="(/torrent/.*?)" class="detLink".*?>(.*?)</a>.*?</tr>'''
        for row in  re.compile(regexp, re.DOTALL).findall(data):
            torrentType = row[0]
            torrentLink = "http://thepiratebay.org" + row[1]
            torrentTitle = decodeHtml(row[2])
            # 201 = Movies , 202 = Movie DVDR, 205 TV Shows
            if torrentType in ['201']:
                results.append((torrentTitle, torrentLink, ''))
            if len(results) >= max_results:
                return results
        next = re.compile('<a.*?href="(.*?)".*?>.*?next.gif.*?</a>').findall(data)
    return results

def findMovieByImdb(imdb):
    return findMovies("tt" + normalizeImdbId(imdb))

def getId(piratebayId):
    if piratebayId.startswith('http://torrents.thepiratebay.org/'):
        piratebayId = piratebayId.split('org/')[1]
    d = findRe(piratebayId, "tor/(\d+)")
    if d:
        piratebayId = d
    d = findRe(piratebayId, "torrent/(\d+)")
    if d:
        piratebayId = d
    return piratebayId

def exists(piratebayId):
    piratebayId = getId(piratebayId)
    return ox.net.exists("http://thepiratebay.org/torrent/%s" % piratebayId)

def getData(piratebayId):
    _key_map = {
      'spoken language(s)': u'language',
      'texted language(s)': u'subtitle language',
      'by': u'uploader',
      'leechers': 'leecher',
      'seeders': 'seeder',
    }
    piratebayId = getId(piratebayId)
    torrent = dict()
    torrent[u'id'] = piratebayId
    torrent[u'domain'] = 'thepiratebay.org'
    torrent[u'comment_link'] = 'http://thepiratebay.org/torrent/%s' % piratebayId

    data = _readUrlUnicode(torrent['comment_link'])
    torrent[u'title'] = findRe(data, '<title>(.*?) \(download torrent\) - TPB</title>')
    if not torrent[u'title']:
        return None
    torrent[u'title'] = decodeHtml(torrent[u'title']).strip()
    torrent[u'imdbId'] = findRe(data, 'title/tt(\d{7})')
    title = quote(torrent['title'].encode('utf-8'))
    torrent[u'torrent_link']="http://torrents.thepiratebay.org/%s/%s.torrent" % (piratebayId, title)
    for d in re.compile('dt>(.*?):</dt>.*?<dd.*?>(.*?)</dd>', re.DOTALL).findall(data):
        key = d[0].lower().strip()
        key = _key_map.get(key, key)
        value = decodeHtml(stripTags(d[1].strip()))
        torrent[key] = value
    torrent[u'description'] = findRe(data, '<div class="nfo">(.*?)</div>')
    if torrent[u'description']:
        torrent['description'] = normalizeNewlines(decodeHtml(stripTags(torrent['description']))).strip()
    t = _readUrl(torrent[u'torrent_link'])
    torrent[u'torrent_info'] = getTorrentInfo(t)
    return torrent

class Thepiratebay(Torrent):
    '''
    >>> Thepiratebay('123')
    {}

    >>> Thepiratebay('3951349')['infohash']
    '4e84415d36ed7b54066160c05a0b0f061898d12b'
    '''
    def __init__(self, piratebayId):
        self.data = getData(piratebayId)
        if not self.data:
            return
        Torrent.__init__(self)
        published =  self.data['uploaded']
        published = published.replace(' GMT', '').split(' +')[0]
        self['published'] =  datetime.strptime(published, "%Y-%m-%d %H:%M:%S")

