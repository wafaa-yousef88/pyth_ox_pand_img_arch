# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
from StringIO import StringIO
import xml.etree.ElementTree as ET

from ox.cache import read_url
from ox import find_string, find_re


def get_data(id):
    url = 'http://www.vimeo.com/moogaloop/load/clip:%s' %id
    xml = read_url(url)
    tree = ET.parse(StringIO(xml))
    request_signature = tree.find('request_signature').text
    request_signature_expires = tree.find('request_signature_expires').text
    
    data = {}
    video_url = "http://www.vimeo.com/moogaloop/play/clip:%s/%s/%s/?q=" % \
                              (id, request_signature, request_signature_expires)
    data['video_sd'] = video_url + 'sd'
    data['video_hd'] = video_url + 'hd'
    video = tree.find('video')
    for key in ('caption', 'width', 'height', 'duration', 'thumbnail'):
        data[key] = video.find(key).text
    return data

