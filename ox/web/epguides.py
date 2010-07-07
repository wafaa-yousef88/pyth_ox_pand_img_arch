# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
import time

from ox import stripTags, findRe
from ox.cache import readUrlUnicode

import google


def getShowUrl(title):
    ''' 
    Search Epguide Url for Show via Show Title.
    Use Google to search the url, this is also done on Epguide.
    '''
    for (name, url, desc) in google.find('allintitle: site:epguides.com %s' % title, 1):
        if url.startswith('http://epguides.com'):
              if re.search(title, name):
                    return url
    return None

def getShowData(url):
    data = readUrlUnicode(url)
    r = {}
    r['title'] = stripTags(findRe(data, '<h1>(.*?)</h1>'))
    r['imdb'] = findRe(data, '<h1><a href=".*?/title/tt(\d.*?)">.*?</a></h1>')
    r['episodes'] = {}
    #1.   1- 1       1001      7 Aug 05   You Can't Miss the Bear
    for episode in re.compile('(\d+?)\..*?(\d+?-.\d.*?) .*?(\d+?) .*?(.*?) <a target="_blank" href="(.*?)">(.*?)</a>').findall(data):
        air_date = episode[3].strip()
        #'22 Sep 04' -> 2004-09-22 
        try:
            air_date = time.strftime('%Y-%m-%d', time.strptime(air_date, '%d %b %y'))
        except:
            pass
        s = episode[1].split('-')[0].strip()
        e = episode[1].split('-')[-1].strip()
        try:
            r['episodes']['S%02dE%02d' % (int(s), int(e))] = {
                'prod code': episode[2],
                'air date': air_date,
                'url': episode[4],
                'title':episode[5],
            }
        except:
            print "oxweb.epguides failed,", url
    return r

