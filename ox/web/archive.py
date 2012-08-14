# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from .. import cache
from ..utils import json

def getId(url):
    return url.split("/")[-1]

def getUrl(id):
    return "http://www.archive.org/details/%s" % id

def getData(id):
    data = {}
    url = getUrl(id)
    details = cache.readUrl('%s?output=json' % url)
    details = json.loads(details)
    for key in ('title', 'description', 'runtime'):
        data[key] = details['metadata'][key]
        if isinstance(data[key], list):
            data[key] = data[key][0]
    data['url'] = url
    data['image'] = 'http://archive.org/download/%s/format=thumbnail' % id
    data['ogg'] = 'http://archive.org/download/%s/format=Ogg+video' % id
    data['mp4'] = 'http://archive.org/download/%s/format=512Kb+MPEG4' % id
    return data

