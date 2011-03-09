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
    u'0060304'

    >>> getData('236')['posters'][0]
    u'http://criterion_production.s3.amazonaws.com/release_images/1586/ThirdManReplace.jpg'

    >>> getData('786')['posters'][0]
    u'http://criterion_production.s3.amazonaws.com/product_images/185/343_box_348x490.jpg'
    '''
    data = {
        "url": getUrl(id)
    }
    try:
        html = readUrlUnicode(data["url"])
    except:
        html = ox.cache.readUrl(data["url"])
    data["number"] = findRe(html, "<li>Spine #(\d+)")

    data["title"] = findRe(html, "<meta property=['\"]og:title['\"] content=['\"](.*?)['\"]")
    data["title"] = data["title"].split(u' \u2014 The Television Version')[0]
    data["director"] = stripTags(findRe(html, "<h2 class=\"director\">(.*?)</h2>"))
    results = findRe(html, '<div class="left_column">(.*?)</div>')
    results = re.compile("<li>(.*?)</li>").findall(results)
    data["country"] = results[0]
    data["year"] = results[1]
    data["synopsis"] = stripTags(findRe(html, "<p><strong>SYNOPSIS:</strong> (.*?)</p>"))

    result = findRe(html, "<div class=\"purchase\">(.*?)</div>")
    if 'Blu-Ray' in result or 'Essential Art House DVD' in result:
        r = re.compile('<h3 class="section_title first">Other Editions</h3>(.*?)</div>', re.DOTALL).findall(html)
        if r:
            result = r[0]
    result = findRe(result, "<a href=\"(.*?)\"")
    if not "/boxsets/" in result:
        data["posters"] = [result]
    else:
        html_ = readUrlUnicode(result)
        result = findRe(html_, '<a href="http://www.criterion.com/films/%s.*?">(.*?)</a>' % id)
        result = findRe(result, "src=\"(.*?)\"")
        data["posters"] = [result.replace("_w100", "")]
    result = findRe(html, "<img alt=\"Film Still\" height=\"252\" src=\"(.*?)\"")
    if result:
        data["stills"] = [result]
        data["trailers"] = []
    else:
        data["stills"] = filter(lambda x: x, [findRe(html, "\"thumbnailURL\", \"(.*?)\"")])
        data["trailers"] = filter(lambda x: x, [findRe(html, "\"videoURL\", \"(.*?)\"")])

    data['imdbId'] = imdb.getMovieId(data['title'], data['director'], data['year'])
    return data

def getIds():
    ids = []
    html = readUrlUnicode("http://www.criterion.com/library/expanded_view?m=dvd&p=1&pp=50&s=spine")
    results = re.compile("\&amp;p=(\d+)\&").findall(html)
    pages = max(map(int, results))
    for page in range(1, pages):
        for id in getIdsByPage(page):
            ids.append(id)
    return map(lambda id: str(id), sorted(map(lambda id: int(id), set(ids))))

def getIdsByPage(page):
    ids = []
    html = readUrlUnicode("http://www.criterion.com/library/expanded_view?m=dvd&p=%s&pp=50&s=spine" % page)
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
