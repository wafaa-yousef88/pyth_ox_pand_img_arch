# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from urllib import quote, unquote_plus
import re
from xml.dom.minidom import parseString

import feedparser
from ox.cache import read_url, cache_timeout

 
def video_url(youtubeId, format='mp4', timeout=cache_timeout):
    """
        youtubeId - if of video
        format - video format, options: webm, 1080p, 720p, mp4, high
    """
    def get_url(stream):
        return '%s&signature=%s' % (stream['url'], stream['sig'])
    fmt = None
    if format == '1080p':
        fmt=37
    if format == '720p':
        fmt=22
    elif format == 'mp4':
        fmt=18
    elif format == 'high':
        fmt=35
    elif format == 'webm':
        streams = videos(youtubeId, 'webm')
        return get_url(streams[max(streams.keys())])

    streams = videos(youtubeId)
    if str(fmt) in streams:
        return get_url(streams[str(fmt)])

def find(query, max_results=10, offset=1, orderBy='relevance'):
    query = quote(query)
    url = "http://gdata.youtube.com/feeds/api/videos?vq=%s&orderby=%s&start-index=%s&max-results=%s" % (query, orderBy, offset, max_results)
    data = read_url(url)
    fd = feedparser.parse(data)
    videos = []
    for item in fd.entries:
        id = item['id'].split('/')[-1]
        title = item['title']
        description = item['description']
        videos.append((title, id, description))
        if len(videos) >= max_results:
            return videos
    return videos

def info(id):
    info = {}
    url = "http://gdata.youtube.com/feeds/api/videos/%s?v=2" % id
    data = read_url(url)
    xml = parseString(data)
    info['url'] = 'http://www.youtube.com/watch?v=%s' % id
    info['title'] = xml.getElementsByTagName('title')[0].firstChild.data
    info['description'] = xml.getElementsByTagName('media:description')[0].firstChild.data
    info['date'] = xml.getElementsByTagName('published')[0].firstChild.data.split('T')[0]
    info['author'] = "http://www.youtube.com/user/%s"%xml.getElementsByTagName('name')[0].firstChild.data

    info['categories'] = []
    for cat in xml.getElementsByTagName('media:category'):
        info['categories'].append(cat.firstChild.data)

    info['keywords'] = xml.getElementsByTagName('media:keywords')[0].firstChild.data.split(', ')
    url = "http://www.youtube.com/watch?v=%s" % id
    data = read_url(url)
    match = re.compile('<h4>License:</h4>(.*?)</p>', re.DOTALL).findall(data)
    if match:
        info['license'] = match[0].strip()
        info['license'] = re.sub('<.+?>', '', info['license']).strip()

    url = "http://www.youtube.com/api/timedtext?hl=en&type=list&tlangs=1&v=%s&asrs=1"%id
    data = read_url(url)
    xml = parseString(data)
    languages = [t.getAttribute('lang_code') for t in xml.getElementsByTagName('track')]
    if languages:
        info['subtitles'] = {}
        for language in languages:
            url = "http://www.youtube.com/api/timedtext?hl=en&v=%s&type=track&lang=%s&name&kind"%(id, language)
            data = read_url(url)
            xml = parseString(data)
            subs = []
            for t in xml.getElementsByTagName('text'):
                start = float(t.getAttribute('start'))
                duration = t.getAttribute('dur')
                if not duration:
                    duration = '2'
                end = start + float(duration)
                text = t.firstChild.data
                subs.append({
                    'start': start,
                    'end': end,
                    'value': text,
                })
            info['subtitles'][language] = subs
    return info

def videos(id, format=''):
    stream_type = {
        'flv': 'video/x-flv',
        'webm': 'video/webm',
        'mp4': 'video/mp4'
    }.get(format)
    url = "http://www.youtube.com/watch?v=%s" % id
    data = read_url(url)
    match = re.compile('"url_encoded_fmt_stream_map": "(.*?)"').findall(data)
    streams = {}
    for x in match[0].split(','):
        stream = {}
        for s in x.split('\\u0026'):
            key, value = s.split('=')
            value = unquote_plus(value)
            stream[key] = value
        if not stream_type or stream['type'].startswith(stream_type):
            streams[stream['itag']] = stream
    return streams
