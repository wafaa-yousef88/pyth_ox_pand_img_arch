# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
import time

from ox import stripTags, findRe
from ox.cache import readUrlUnicode


def getId(url):
    return url.split("/")[-2]

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
    data = {
        "url": getUrl(id)
    }
    html = readUrlUnicode(data["url"])
    data['aka'] = parseList(html, 'AKA')
    data['category'] = findRe(html, 'http://allmovie.com/explore/category/.*?">(.*?)</a>')
    data['countries'] = parseList(html, 'Countries')
    data['director'] = parseEntry(html, 'Director')
    data['genres'] = parseList(html, 'Genres')
    data['keywords'] = parseList(html, 'Keywords')
    data['posters'] = [findRe(html, '<img src="(http://image\..*?)"')]
    data['produced'] = parseList(html, 'Produced by')
    data['rating'] = findRe(html, 'Stars" title="(.*?) Stars"')
    data['released'] = parseEntry(html, 'Released by')
    data['releasedate'] = parseEntry(html, 'Release')[0:10].replace(' ', '-')
    data['runtime'] = findRe(html, '<td class="formed-sub" style="width: 86px;">(\d+) min.</td>')
    data['set'] = parseEntry(html, 'Set In')
    data['synopsis'] = parseText(html, 'Plot Synopsis')
    data['themes'] = parseList(html, 'Themes')
    data['types'] = parseList(html, 'Types')
    data['year'] = findRe(html, '"http://allmovie.com/explore/year/(.*?)"')
    html = readUrlUnicode("http://allmovie.com/work/%s/cast" % id)
    data['cast'] = parseTable(html)
    html = readUrlUnicode("http://allmovie.com/work/%s/credits" % id)
    data['credits'] = parseTable(html)
    html = readUrlUnicode("http://allmovie.com/work/%s/review" % id)
    data['review'] = parseText(html, 'Review')
    return data

def getUrl(id):
    return "http://allmovie.com/work/%s/" % id

def parseEntry(html, title):
    return stripTags(findRe(html, '<span>%s</span>(.*?)</table>' % title)).strip()

def parseList(html, title):
    html = findRe(html, '<span>%s</span>(.*?)</table>' % title)
    return map(lambda x: stripTags(x), re.compile('<li>(.*?)</li>', re.DOTALL).findall(html))

def parseTable(html):
    return map(
        lambda x: map(
            lambda x: stripTags(x).strip().replace('&nbsp;', ''),
            x.split('<td width="305">-')
        ),
        findRe(html, '<div id="results-table">(.*?)</table>').split('</tr>')[:-1]
    )

def parseText(html, title):
    return stripTags(findRe(html, '%s</td>.*?<td colspan="2"><p>(.*?)</td>' % title)).strip()

if __name__ == '__main__':
    print getData('129689')
    # print getData('177524')

