# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
from ox import cache
from ox.html import stripTags
from ox.text import findRe

import auth


def readUrl(url, data=None, headers=cache.DEFAULT_HEADERS, timeout=cache.cache_timeout, valid=None):
    headers = headers.copy()
    headers["Cookie"] = auth.get("karagarga.cookie")
    return cache.readUrl(url, data, headers, timeout)

def readUrlUnicode(url, timeout=cache.cache_timeout):
   return cache.readUrlUnicode(url, _readUrl=readUrl, timeout=timeout)

def getData(id):
    data = {
        "url": getUrl(id)
    }
    html = readUrlUnicode("%s%s" % (data["url"], "&filelist=1"))
    if 'No torrent with ID' in html:
        return False
    data['added'] = stripTags(parseTable(html, 'Added'))
    data['country'] = findRe(html, 'title="([\w ]*?)" border="0" width="32" height="20"')
    # data['description'] = parseTable(html, 'Description')
    data['director'] = stripTags(parseTable(html, 'Director / Artist'))
    data['files'] = []
    result = findRe(html, '<table class=main border="1" cellspacing=0 cellpadding="5">(.*?)</table>')
    results = re.compile('<td>(.*?)</td><td align="right">(.*?)</td>', re.DOTALL).findall(result)
    for name, size in results:
        data['files'].append({
            'name': name,
            'size': '%s %s' % (size[:-2], size[-2:].strip().upper())
        })
    data['format'] = ''
    if html.find('genreimages/dvdr.png') != -1:
        data['format'] = 'DVD'
    elif html.find('genreimages/hdrip.png') != -1:
        data['format'] = 'HD'
    data['genre'] = []
    result = parseTable(html, 'Genres')
    for string in result.split('\n'):
        string = stripTags(findRe(string, '<a href="browse.php\?genre=.*?">(.*?)</a>'))
        if string:
            data['genre'].append(string)
    data['id'] = id
    data['imdbId'] = findRe(html, 'imdb.com/title/tt(\d{7})')
    data['language'] = stripTags(parseTable(html, 'Language'))
    data['leechers'] = int(findRe(html, 'seeder\(s\), (.*?) leecher\(s\)'))
    data['link'] = stripTags(parseTable(html, 'Internet Link'))
    data['links'] = []
    results = re.compile('<a href="(.*?)">(.*?)</a>', re.DOTALL).findall(parseTable(html, 'Description'))
    for (url, title) in results:
        if url.find('javascript') == -1:
            data['links'].append({
                'title': title,
                'url': url.replace('http://anonym.to/?', '')
            })
    data['people'] = 0
    result = stripTags(findRe(html, '<a href="top10others.php.*?>(.*?) people')).strip()
    if result:
        data['people'] = int(result)
    data['posters'] = []
    results = re.compile('<img border=0 src="(http://.*?)"', re.DOTALL).findall(html)
    for result in results:
        data['posters'].append(result)
    data['seeders'] = int(findRe(html, '#seeders" class="sublink".*?colspan=2>(.*?) seeder\(s\)'))
    data['size'] = int(findRe(parseTable(html, 'Size'), '\((.*?) ').replace(',', ''))
    data['snatched'] = int(findRe(html, '<a name="snatchers">.*?colspan=2>(.*?) '))
    data['subtitle'] = findRe(parseTable(html, 'Subtitles'), '>(.*?)<hr>').replace('included: ', '')
    data['subtitles'] = []
    results = re.compile('<a href="(.*?)">(.*?)</a>', re.DOTALL).findall(parseTable(html, 'Subtitles'))
    for (url, language) in results:
        data['subtitles'].append({
            'language': language.replace('click here for ', ''),
            'url': url
        })
    data['torrent'] = 'http://karagarga.net/%s' % findRe(html, '(down.php/.*?)"')
    data['year'] = stripTags(parseTable(html, 'Year'))
    data['title'] = stripTags(findRe(html, '<h1>(.*?)</h1>')).strip()
    data['title'] = re.sub('^%s - ' % re.escape(data['director']), '', data['title'])
    data['title'] = re.sub(' \(%s\)$' % re.escape(data['year']), '', data['title'])    
    return data

def getId(url):
    return url.split("=")[-1]

def getTorrent(id):
    return readUrl(getData(id)['torrent'])

def getIds(lastId = 20):
    lastId = '%s' % lastId
    ids = []
    page = 0
    while True:
        for id in getIdsByPage(page):
            if not id in ids:
                ids.append(id)
        if lastId in ids:
            break
        page += 1
    return map(lambda id: str(id), sorted(map(lambda id: int(id), set(ids))))

def getIdsByPage(page):
    ids = []
    url = 'http://karagarga.net/browse.php?page=%s&cat=1&sort=added&d=DESC' % page
    html = readUrlUnicode(url, timeout = 23*60*60) #get new ids once per day
    strings = html.split('<td width="42" style="padding:0px;">')
    strings.pop(0)
    for string in strings:
        ids.append(findRe(string, '"details.php\?id=(.*?)"'))
    return ids

def getUrl(id):
    return "http://karagarga.net/details.php?id=%s" % id

def parseTable(html, title):
    if title == 'Genres':
        return findRe(html, '<td class="heading" [\w=" ]*?>%s</td>(.*?)</table>' % title)
    else:
        return findRe(html, '<td class="heading" [\w=" ]*?>%s</td>(.*?)</td>' % title)

if __name__ == "__main__":
    print getIds("79317")
    print getData("79317")
