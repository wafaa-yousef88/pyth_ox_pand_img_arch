# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import ox.cache
from ox.cache import exists


def getPosterUrl(id):
    url = "http://piratecinema.org/posters/%s/%s.jpg" % (id[:4], id)
    if ox.cache.exists(url):
        return url
    return ''

