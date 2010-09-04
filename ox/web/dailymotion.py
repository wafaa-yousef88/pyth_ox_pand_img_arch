# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
from urllib import unquote
from ox.cache import readUrl


def getVideoUrl(url):
    '''
    >>> getVideoUrl('http://www.dailymotion.com/relevance/search/priere%2Bpour%2Brefuznik/video/x3opar_priere-pour-refuznik-1-jeanluc-goda_shortfilms').split('?auth')[0]
    'http://www.dailymotion.com/cdn/FLV-320x240/video/x3opar_priere-pour-refuznik-1-jean-luc-god_shortfilms.flv'

    >>> getVideoUrl('http://www.dailymotion.com/relevance/search/priere%2Bpour%2Brefuznik/video/x3ou94_priere-pour-refuznik-2-jeanluc-goda_shortfilms').split('?auth')[0]
    'http://www.dailymotion.com/cdn/FLV-320x240/video/x3ou94_priere-pour-refuznik-2-jean-luc-god_shortfilms.flv'
    '''
    data = readUrl(url)
    video = re.compile('''video", "(.*?)"''').findall(data)
    for v in video:
       v =  unquote(v).split('@@')[0]
       return v
    return ''
