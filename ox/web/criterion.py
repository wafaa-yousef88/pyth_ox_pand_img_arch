# -*- coding: UTF-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re

import ox.cache
from ox.cache import readUrlUnicode
from ox.html import stripTags
from ox.text import findRe, removeSpecialCharacters

import imdb

def getId(url):
    return url.split("/")[-1]

def getUrl(id):
    return "http://www.criterion.com/films/%s" % id

def getData(id):
    '''
    >>> getData('1333')['imdbId']
    '0060304'

    >>> getData('236')['posters'][0]
    'http://criterion_production.s3.amazonaws.com/release_images/1586/ThirdManReplace.jpg'

    >>> getData('786')['posters'][0]
    'http://criterion_production.s3.amazonaws.com/product_images/185/343_box_348x490.jpg'
    '''
    data = {
        "url": getUrl(id)
    }
    try:
        html = readUrlUnicode(data["url"])
    except:
        html = ox.cache.getUrl(data["url"])
    data["number"] = findRe(html, "<p class=\"spinenumber\">(.*?)</p>")
    data["title"] = findRe(html, "<h2 class=\"movietitle\">(.*?)</h2>")
    data["director"] = findRe(html, "<h2 class=\"director\">(.*?)</h2>")
    results = re.compile("<p><strong>(.*?)</strong></p>").findall(html)
    data["country"] = results[0]
    data["year"] = results[1]
    result = findRe(html, "<div class=\"synopsis contentbox lightgray\">(.*?)</div>")
    data["synopsis"] = findRe(result, "<p>(.*?)</p>")
    result = findRe(html, "<div class=\"editioninfo\">(.*?)</div>")
    if 'Blu-Ray' in result or 'Essential Art House DVD' in result:
        result = re.compile("<div class=\"editioninfo\">(.*?)</div>", re.DOTALL).findall(html)[1]
    result = findRe(result, "<a href=\"(.*?)\">")
    if not "/boxsets/" in result:
        data["posters"] = [result]
    else:
        html_ = readUrlUnicode(result)
        result = findRe(html_, "<a href=\"http://www.criterion.com/films/%s\">(.*?)</a>" % id)
        result = findRe(result, "src=\"(.*?)\"")
        data["posters"] = [result.replace("_w100", "")]
    result = findRe(html, "<img alt=\"Film Still\" height=\"252\" src=\"(.*?)\"")
    if result:
        data["stills"] = [result]
        data["trailers"] = []
    else:
        data["stills"] = [findRe(html, "\"thumbnailURL\", \"(.*?)\"")]
        data["trailers"] = [findRe(html, "\"videoURL\", \"(.*?)\"")]
    data['imdbId'] = imdb.getMovieId(data['title'], data['director'], data['year'])
    return data

def getIds():
    ids = []
    html = readUrlUnicode("http://www.criterion.com/library/dvd")
    results = re.compile("page=(.*?)\"").findall(html)
    pages = int(results[len(results) - 2])
    for page in range(pages, 0, -1):
        for id in getIdsByPage(page):
            ids.append(id)
    return map(lambda id: str(id), sorted(map(lambda id: int(id), set(ids))))

def getIdsByPage(page):
    ids = []
    html = readUrlUnicode("http://www.criterion.com/library/dvd?page=%s" % page)
    results = re.compile("films/(\d+)").findall(html)
    for result in results:
        ids.append(result)
    results = re.compile("boxsets/(.*?)\"").findall(html)
    for result in results:
        html = readUrlUnicode("http://www.criterion.com/boxsets/" + result)
        results = re.compile("films/(\d+)").findall(html)
        for result in results:
            ids.append(result)
    return set(ids)

if __name__ == '__main__':
    print getIds()
