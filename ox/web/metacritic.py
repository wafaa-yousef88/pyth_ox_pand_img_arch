# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
from urllib import quote
from lxml.html import document_fromstring

from ox.cache import read_url
from ox import find_re, strip_tags

def getUrl(id):
    return 'http://www.metacritic.com/movie/%s' % id

def getId(url):
    return url.split('/')[-1]

def getUrlByImdb(imdb):
    url = "http://www.imdb.com/title/tt%s/criticreviews" % imdb
    data = read_url(url)
    metacritic_url = find_re(data, '"(http://www.metacritic.com/movie/.*?)"')
    return metacritic_url or None

def getMetacriticShowUrl(title):
    title = quote(title)
    url = "http://www.metacritic.com/search/process?ty=6&ts=%s&tfs=tvshow_title&x=0&y=0&sb=0&release_date_s=&release_date_e=&metascore_s=&metascore_e=" % title
    data = read_url(url)
    return find_re(data, '(http://www.metacritic.com/tv/shows/.*?)\?')

def getData(url):
    data = read_url(url, unicode=True)
    doc = document_fromstring(data)
    score = filter(lambda s: s.attrib.get('property') == 'v:average',
                   doc.xpath('//span[@class="score_value"]'))
    if score:
        score = int(score[0].text)
    else:
        score = -1
    authors = [a.text
        for a in doc.xpath('//div[@class="review_content"]//div[@class="author"]//a')]
    sources = [d.text
        for d in doc.xpath('//div[@class="review_content"]//div[@class="source"]/a')]
    reviews = [d.text
        for d in doc.xpath('//div[@class="review_content"]//div[@class="review_body"]')]
    scores = [int(d.text.strip())
        for d in doc.xpath('//div[@class="review_content"]//div[contains(@class, "critscore")]')]
    urls = [a.attrib['href']
        for a in doc.xpath('//div[@class="review_content"]//a[contains(@class, "external")]')]

    metacritics = []
    for i in range(len(authors)):
        metacritics.append({
            'critic': authors[i],
            'url': urls[i],
            'source': sources[i],
            'quote': strip_tags(reviews[i]).strip(),
            'score': scores[i],
        })
        
    return {
        'critics': metacritics,
        'id': getId(url),
        'score': score,
        'url': url,
    }

