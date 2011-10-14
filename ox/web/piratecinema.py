# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
from ox.cache import readUrlUnicode

def getPosterUrl(id):
    url = 'http://piratecinema.org/posters/'
    html = readUrlUnicode(url)
    results = re.compile('src="(.+)" title=".+\((\d{7})\)"').findall(html)
    for result in results:
        if result[1] == id:
            return url + result[0]
    return ''

if __name__ == '__main__':
    print getPosterUrl('0749451')

