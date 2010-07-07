# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
import time

from ox import stripTags, findRe
from ox.cache import readUrlUnicode


def getEpisodeData(url):
    '''
      prases informatin on tvcom episode pages
      returns dict with title, show, description, score
      example:
        getEpisodeData('http://www.tv.com/lost/do-no-harm/episode/399310/summary.html')
    '''
    data = readUrlUnicode(url)
    r = {}
    r['description'] = stripTags(findRe(data, 'div id="main-col">.*?<div>(.*?)</div').split('\r')[0])
    r['show'] = findRe(data, '<h1>(.*?)</h1>')
    r['title'] =  findRe(data, '<title>.*?: (.*?) - TV.com  </title>')
    #episode score
    r['episode score'] = findRe(data, '<span class="f-28 f-bold mt-10 mb-10 f-FF9 db lh-18">(.*?)</span>')

    match = re.compile('Episode Number: (\d*?) &nbsp;&nbsp; Season Num: (\d*?) &nbsp;&nbsp; First Aired: (.*?) &nbsp').findall(data) 
    if match:
        r['season'] = int(match[0][1])
        r['episode'] = int(match[0][0])
        #'Wednesday September 29, 2004' -> 2004-09-29 
        r['air date'] = time.strftime('%Y-%m-%d', time.strptime(match[0][2], '%A %B %d, %Y'))
    return r

