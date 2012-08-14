# -*- coding: UTF-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import re
from lxml.html import document_fromstring

from ox.cache import read_url
from ox import findRe, strip_tags
from ox.web.imdb import ImdbCombined


def getData(id, timeout=-1):
    '''
    >>> getData('the-matrix')['poster']
    'http://content7.flixster.com/movie/16/90/52/1690525_gal.jpg'

    >>> getData('0133093')['poster']
    'http://content7.flixster.com/movie/16/90/52/1690525_gal.jpg'

    >>> getData('2-or-3-things-i-know-about-her')['poster']
    'http://content6.flixster.com/movie/10/95/43/10954392_gal.jpg'

    >>> getData('0078875')['rottentomatoes_id']
    'http://www.rottentomatoes.com/m/the-tin-drum/'
    '''
    if len(id) == 7:
        try:
            int(id)
            id = getIdByImdb(id)
        except:
            pass
    data = {
        "url": getUrl(id),
    }
    html = read_url(data['url'], timeout=timeout, timeout=True)
    doc = document_fromstring(html)

    props = {
        'og:title': 'title',
        'og:image': 'poster',
        'og:url': 'rottentomatoes_id',
    }
    for meta in doc.head.findall('meta'):
        prop = meta.attrib.get('property', None)
        content = meta.attrib.get('content', '')
        if prop in props and content:
            data[props[prop]] = content

    for p in doc.body.find_class('synopsis'):
        data['synopsis'] = p.text.strip()

    if 'poster' in data and data['poster']:
        data['poster'] = data['poster'].replace('_pro.jpg', '_gal.jpg')
    if not 'title' in data:
        return None
    return data

def getIdByImdb(imdbId):
    '''
    >>> getIdByImdb('0133093')
    u'the-matrix'

    #>>> getIdByImdb('0060304')
    #u'2-or-3-things-i-know-about-her'
    '''
    i = ImdbCombined(imdbId)
    title = i['title']
    return title.replace(' ', '-').lower().replace("'", '')

def getId(url):
    return url.split('/')[-1]

def getUrl(id):
    return "http://www.flixster.com/movie/%s"%id

