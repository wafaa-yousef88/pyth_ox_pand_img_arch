# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
import os
import string

from ox import cache
from ox.html import stripTags, decodeHtml
from ox.text import findRe
from ox.normalize import canonicalName
import auth


def readUrl(url, data=None, headers=cache.DEFAULT_HEADERS, timeout=cache.cache_timeout, valid=None):
    headers = headers.copy()
    headers["Cookie"] = auth.get("aaaarg.cookie")
    return cache.readUrl(url, data, headers, timeout)

def readUrlUnicode(url, timeout=cache.cache_timeout):
   return cache.readUrlUnicode(url, _readUrl=readUrl, timeout=timeout)

def downloadText(id, filename=None):
    #FIXME, what about the cache, this keeps all pdfs in oxcache...
    url='http://aaaaarg.org/node/%d/download' % id
    data = readUrl(url, timeout=-1)
    headers = cache.getHeaders(url, timeout=-1)
    if filename:
        with open(filename, "w") as f:
            f.write(data)
        return
    return data

def getTextByLetter(letter):
    texts = []
    url = 'http://aaaaarg.org/library/%s' % letter
    data = readUrlUnicode(url)
    txts = re.compile('<li class="author">(.*?)</li><li class="title"><a href="(.*?)">(.*?)</a></li>').findall(data)
    author = 'Unknown Author'
    for r in txts:
        if r[0] != '&nbsp;':
            author = r[0]
        link = r[1]
        id = findRe(link, '/(\d+)')
        title = decodeHtml(r[2])
        author_foder =  canonicalName(author)
        author_foder = os.path.join(author_foder[0], author_foder)
        filename = os.path.join(author_foder, '%s (aaarg %s).pdf' %  (title.replace('/', '_'), id))
        texts.append({
            'author': author,
            'title': title,
            'id': id,
            'filename': filename,
         })
    return texts

def getData(id):
    url = "http://aaaaarg.org/node/%s"%id
    data=readUrlUnicode(url)

    title = findRe(data, '<h2>(.*?)</h2>')
    author = findRe(data, '<div class="author"><em>written by (.*?)</em></div>')
    links = re.compile('<a href="http://anonym.to/\?(.*?)" class="link-to-text">').findall(data)

    return {
        'aaaaarg': id,
        'links': links,
        'title': title,
        'author': author
    }

def getTexts():
    texts = []
    for letter in string.letters[:26]:
        texts += getTextByLetter(letter)
    texts += getTextByLetter('date')
    return texts

