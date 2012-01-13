# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4


def getId(url):
    return url.split("/")[-1]

def getUrl(id):
    return "http://www.archive.org/details/%s" % id

