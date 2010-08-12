# vi:si:et:sw=4:sts=4:ts=4
# encoding: utf-8
import re

from ox.cache import readUrlUnicode
from ox.html import stripTags
from ox.text import findRe

import imdb

def getData(id):
    '''
    >>> getData('1991/silence_of_the_lambs')['imdbId']
    u'0102926'

    >>> getData('1991/silence_of_the_lambs')['posters'][0]
    u'http://www.impawards.com/1991/posters/silence_of_the_lambs_ver1_xlg.jpg'

    >>> getData('1991/silence_of_the_lambs')['url']
    u'http://www.impawards.com/1991/silence_of_the_lambs_ver1.html'
    '''
    data = {
        'url': getUrl(id)
    }
    html = readUrlUnicode(data['url'])
    data['imdbId'] = findRe(html, 'imdb.com/title/tt(\d{7})')
    data['title'] = stripTags(findRe(html, '<p class="name white">(.*?) \(<a href="alpha1.html">'))
    data['year'] = findRe(html, '\(<a href="alpha1.html">(.*?)</a>\)')
    data['posters'] = []
    poster = findRe(html, '<img src="(posters.*?)" alt=')
    if poster:
        poster = 'http://www.impawards.com/%s/%s' % (data['year'], poster)
        data['posters'].append(poster)
    results = re.compile('<a href = (%s.*?html)' % id[5:], re.DOTALL).findall(html)
    for result in results:
        result = result.replace('_xlg.html', '.html')
        url = 'http://www.impawards.com/%s/%s' % (data['year'], result)
        html = readUrlUnicode(url)
        result = findRe(html, '<a href = (\w*?_xlg.html)')
        if result:
            url = 'http://www.impawards.com/%s/%s' % (data['year'], result)
            html = readUrlUnicode(url)
            poster = 'http://www.impawards.com/%s/%s' % (data['year'], findRe(html, '<img SRC="(.*?)"'))
        else:
            poster = 'http://www.impawards.com/%s/%s' % (data['year'], findRe(html, '<img src="(posters.*?)" alt='))
        data['posters'].append(poster)
    return data

def getId(url):
    split = url.split('/')
    year = split[3]
    split = split[4][:-5].split('_')
    if split[-1] == 'xlg':
        split.pop()
    if findRe(split[-1], 'ver\d+$'):
        split.pop()
    id = '%s/%s' % (year, '_'.join(split))
    return id

def getIds():
    ids = []
    html = readUrlUnicode('http://www.impawards.com/archives/latest.html', timeout = 60*60)
    pages = int(findRe(html, '<a href= page(.*?).html>')) + 1
    for page in range(pages, 0, -1):
        for id in getIdsByPage(page):
            if not id in ids:
                ids.append(id)
    return ids

def getIdsByPage(page):
    ids = []
    html = readUrlUnicode('http://www.impawards.com/archives/page%s.html' % page, timeout = -1)
    results = re.compile('<a href = \.\./(.*?)>', re.DOTALL).findall(html)
    for result in results:
        url = 'http://impawards.com/%s' % result
        ids.append(getId(url))
    return set(ids)

def getUrl(id):
    url = "http://www.impawards.com/%s.html" % id
    html = readUrlUnicode(url)
    if findRe(html, "No Movie Posters on This Page"):
        url = "http://www.impawards.com/%s_ver1.html" % id
    return url

if __name__ == '__main__':
    ids = getIds()
    print sorted(ids), len(ids)
