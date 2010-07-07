# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
from urllib import quote

from ox.cache import readUrl, readUrlUnicode
from ox import findRe, decodeHtml, stripTags


def getMetacriticShowUrl(title):
    title = quote(title)
    url = "http://www.metacritic.com/search/process?ty=6&ts=%s&tfs=tvshow_title&x=0&y=0&sb=0&release_date_s=&release_date_e=&metascore_s=&metascore_e=" % title
    data = readUrl(url)
    return findRe(data, '(http://www.metacritic.com/tv/shows/.*?)\?')

def getData(title, url=None):
  if not url:
    url = getMetacriticShowUrl(title)
  if not url:
    return None
  data = readUrlUnicode(url)
  score = findRe(data, 'ALT="Metascore: (.*?)"')
  if score: 
    score = int(score)
  else: 
    score = -1

  reviews = re.compile(
            '<div class="scoreandreview"><div class="criticscore">(.*?)</div>'
            '.*?<span class="publication">(.*?)</span>'
            '.*?<span class="criticname">(.*?)</span></div>'
            '.*?<div class="quote">(.*?)<br>'
            '.*?<a href="(.*?)" ', re.DOTALL).findall(data)

  metacritics = []
  for review in reviews:
    metacritics.append({
        'score': int(review[0]),
        'publication':review[1],
        'critic':decodeHtml(review[2]),
        'quote': stripTags(review[3]).strip(),
        'link': review[4],
    })
  return dict(score = score, critics = metacritics, url = url)

