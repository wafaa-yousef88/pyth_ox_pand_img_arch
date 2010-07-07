# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re

import feedparser
from ox.cache import readUrl, readUrlUnicode
from ox import findRe, stripTags
from ox import langCode2To3, langTo3Code

def findSubtitlesByImdb(imdb, parts = 1, language = "eng"):
    if len(language) == 2:
        language = langCode2To3(language)
    elif len(language) != 3:
        language = langTo3Code(language)
    url = "http://www.opensubtitles.org/en/search/"
    if language:
        url += "sublanguageid-%s/" % language
    url += "subsumcd-%s/subformat-srt/imdbid-%s/rss_2_00" % (parts, imdb)
    data = readUrl(url)
    if "title>opensubtitles.com - search results</title" in data:
        fd = feedparser.parse(data)
        opensubtitleId = None
        if fd.entries:
            link = fd.entries[0]['links'][0]['href']
            opensubtitleId = re.compile('subtitles/(.*?)/').findall(link)
            if opensubtitleId:
                opensubtitleId = opensubtitleId[0]
    else:
        opensubtitleId = findRe(data, '/en/subtitles/(.*?)/')
    return opensubtitleId

def downloadSubtitleById(opensubtitle_id):
    srts = {}
    data = readUrl('http://www.opensubtitles.org/en/subtitles/%s' % opensubtitle_id)
    reg_exp = 'href="(/en/download/file/.*?)">(.*?)</a>'
    for f in re.compile(reg_exp, re.DOTALL).findall(data):
        name = stripTags(f[1]).split('\n')[0]
        url = "http://www.opensubtitles.com%s" % f[0]
        srts[name] = readUrlUnicode(url)
    return srts

