# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
from urllib import unquote
from ox.cache import readUrl


def getVideoUrl(url):
    '''
    >>> getVideoUrl('http://www.dailymotion.com/relevance/search/priere%2Bpour%2Brefuznik/video/x3opar_priere-pour-refuznik-1-jeanluc-goda_shortfilms').split('?key')[0]
    'http://www.dailymotion.com/get/16/320x240/flv/6191379.flv'

    >>> getVideoUrl('http://www.dailymotion.com/relevance/search/priere%2Bpour%2Brefuznik/video/x3ou94_priere-pour-refuznik-2-jeanluc-goda_shortfilms').split('?key')[0]
    'http://www.dailymotion.com/get/15/320x240/flv/6197800.flv'
    '''
    data = readUrl(url)
    video = re.compile('''video", "(.*?)"''').findall(data)
    for v in video:
       v =  unquote(v).split('@@')[0]
       return "http://www.dailymotion.com" + v
    return ''

