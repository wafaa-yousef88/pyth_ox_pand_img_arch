# -*- coding: UTF-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import re

from ox.cache import read_url
from ox import findRe

def getData(id):
    '''
    >>> getData('0060304')['posters'][0]
    u'http://www.movieposterdb.com/posters/06_03/1967/0060304/l_99688_0060304_639fdd1e.jpg'
    >>> getData('0123456')['posters']
    []
    '''
    data = {
        "url": getUrl(id)
    }
    data["posters"] = getPostersByUrl(data["url"])
    return data

def getId(url):
    return url.split("/")[-2]

def getPostersByUrl(url, group=True, timeout=-1):
    posters = []
    html = read_url(url, timeout=timeout, unicode=True)
    if url in html:
        if group:
            results = re.compile('<a href="(http://www.movieposterdb.com/group/.+?)\??">', re.DOTALL).findall(html)
            for result in results:
                posters += getPostersByUrl(result, False)
        results = re.compile('<a href="(http://www.movieposterdb.com/poster/.+?)">', re.DOTALL).findall(html)
        for result in results:
            html = read_url(result, timeout=timeout, unicode=True)
            posters.append(findRe(html, '"(http://www.movieposterdb.com/posters/.+?\.jpg)"'))
    return posters

def getUrl(id):
    return "http://www.movieposterdb.com/movie/%s/" % id

if __name__ == '__main__':
    print getData('0060304')
    print getData('0133093')
