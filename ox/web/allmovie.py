# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
import time

from ox import strip_tags, findRe
from ox.cache import read_url


def getId(url):
    return url.split("/")[-1]

def getData(id):
    '''
    >>> getData('129689')['cast'][1][1]
    u'Marianne'
    >>> getData('129689')['credits'][0][0]
    u'Jean-Luc Godard'
    >>> getData('129689')['posters'][0]
    u'http://image.allmusic.com/00/adg/cov200/dru800/u812/u81260bbffr.jpg'
    >>> getData('129689')['rating']
    u'4.5'
    '''
    if id.startswith('http'):
        id = getId(id)
    data = {
        "url": getUrl(id)
    }
    html = read_url(data["url"], unicode=True)
    data['aka'] = parseList(html, 'AKA')
    data['category'] = findRe(html, '<dt>category</dt>.*?<dd>(.*?)</dd>')
    data['countries'] = parseList(html, 'countries')
    data['director'] = parseEntry(html, 'directed by')
    data['genres'] = parseList(html, 'genres')
    data['keywords'] = parseList(html, 'keywords')
    data['posters'] = [findRe(html, '<img src="(http://cps-.*?)"')]
    data['produced'] = parseList(html, 'produced by')
    data['rating'] = findRe(html, 'Stars" title="(.*?) Stars"')
    data['released'] = parseEntry(html, 'released by')
    data['releasedate'] = parseList(html, 'release date')
    data['runtime'] = parseEntry(html, 'run time').replace('min.', '').strip()
    data['set'] = parseEntry(html, 'set in')
    data['synopsis'] = strip_tags(findRe(html, '<div class="toggle-text" itemprop="description">(.*?)</div>')).strip()
    data['themes'] = parseList(html, 'themes')
    data['types'] = parseList(html, 'types')
    data['year'] = findRe(html, '<span class="year">.*?(\d+)')
    #data['stills'] = [re.sub('_derived.*?/', '', i) for i in re.compile('<a href="#" title="movie still".*?<img src="(.*?)"', re.DOTALL).findall(html)]
    data['stills'] = re.compile('<a href="#" title="movie still".*?<img src="(.*?)"', re.DOTALL).findall(html)
    #html = read_url("http://allmovie.com/work/%s/cast" % id, unicode=True)
    #data['cast'] = parseTable(html)
    #html = read_url("http://allmovie.com/work/%s/credits" % id, unicode=True)
    #data['credits'] = parseTable(html)
    html = read_url("http://allmovie.com/work/%s/review" % id, unicode=True)
    data['review'] = strip_tags(findRe(html, '<div class="toggle-text" itemprop="description">(.*?)</div>')).strip()
    return data

def getUrl(id):
    return "http://allmovie.com/work/%s" % id

def parseEntry(html, title):
    html = findRe(html, '<dt>%s</dt>.*?<dd>(.*?)</dd>' % title)
    return strip_tags(html).strip()

def parseList(html, title):
    html = findRe(html, '<dt>%s</dt>.*?<dd>(.*?)</dd>' % title.lower())
    r = map(lambda x: strip_tags(x), re.compile('<li>(.*?)</li>', re.DOTALL).findall(html))
    if not r and html:
        r = [strip_tags(html)]
    return r

def parseTable(html):
    return map(
        lambda x: map(
            lambda x: strip_tags(x).strip().replace('&nbsp;', ''),
            x.split('<td width="305">-')
        ),
        findRe(html, '<div id="results-table">(.*?)</table>').split('</tr>')[:-1]
    )

def parseText(html, title):
    return strip_tags(findRe(html, '%s</td>.*?<td colspan="2"><p>(.*?)</td>' % title)).strip()

if __name__ == '__main__':
    print getData('129689')
    # print getData('177524')

