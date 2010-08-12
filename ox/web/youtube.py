# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from urllib import quote, unquote
import httplib
import xml.etree.ElementTree as ET
import re
from urlparse import parse_qs

import feedparser
from ox.cache import readUrl, readUrlUnicode
from ox import findString, findRe

def getVideoKey(youtubeId):
    for el_type in ['&el=embedded', '&el=detailpage', '&el=vevo', '']:
        video_info_url = 'http://www.youtube.com/get_video_info?&video_id=%s%s&ps=default&eurl=&gl=US&hl=en' % (youtubeId, el_type)
        try:
            data = readUrl(video_info_url)
            video_info = parse_qs(data)
            if 'token' in video_info:
                return video_info['token'][0]
        except (urllib2.URLError, httplib.HTTPException, socket.error), err:
            return
    return False
 
def getVideoUrl(youtubeId, format='mp4'):
    youtubeKey = getVideoKey(youtubeId)

    fmt = None
    if format == 'webm':
        fmt=45
    if format == '1080p':
        fmt=37
    if format == '720p':
        fmt=22
    elif format == 'mp4':
        fmt=18
    elif format == 'high':
        fmt=35
    url_template = "http://www.youtube.com/get_video?video_id=%s&t=%s=&eurl=&el=&ps=&asv="
    url = url_template % (youtubeId, youtubeKey)
    if fmt:
        url += "&fmt=%d"%fmt

    return url

def getMovieInfo(youtubeId, video_url_base=None):
    url = "http://gdata.youtube.com/feeds/api/videos/%s" % youtubeId
    data = readUrl(url)
    fd = feedparser.parse(data)
    return getInfoFromAtom(fd.entries[0], video_url_base)

def getInfoFromAtom(entry, video_url_base=None):
    info = dict()
    info['title'] = entry['title']
    info['description'] = entry['description']
    info['author'] = entry['author']
    #info['published'] = entry['published_parsed']
    if 'media_keywords' in entry:
        info['keywords'] = entry['media_keywords'].split(', ')
    info['url'] = entry['links'][0]['href']
    info['id'] = findRe(info['url'], r'\?v=(.*?)&') 
    info['thumbnail'] = "http://img.youtube.com/vi/%s/0.jpg" % info['id']
    if video_url_base:
        info['flv'] = "%s/%s.%s" % (video_url_base, info['id'], 'flv')
        info['mp4'] = "%s/%s.%s" % (video_url_base, info['id'], 'mp4')
    else:
        info['flv'] = getVideoUrl(info['id'], 'flv')
        info['flv_high'] = getVideoUrl(info['id'], 'high')
        info['webm'] = getVideoUrl(info['id'], 'webm')
        info['mp4'] = getVideoUrl(info['id'], 'mp4')
        info['720p'] = getVideoUrl(info['id'], '720p')
        info['1080p'] = getVideoUrl(info['id'], '1080p')
    info['embed'] = '<object width="425" height="355"><param name="movie" value="http://www.youtube.com/v/%s&hl=en"></param><param name="wmode" value="transparent"></param><embed src="http://www.youtube.com/v/%s&hl=en" type="application/x-shockwave-flash" wmode="transparent" width="425" height="355"></embed></object>' % (info['id'], info['id'])
    return info

def find(query, max_results=10, offset=1, orderBy='relevance', video_url_base=None):
    query = quote(query)
    url = "http://gdata.youtube.com/feeds/api/videos?vq=%s&orderby=%s&start-index=%s&max-results=%s" % (query, orderBy, offset, max_results)
    data = readUrlUnicode(url)
    fd = feedparser.parse(data)
    videos = []
    for entry in fd.entries:
        v = getInfoFromAtom(entry, video_url_base)
        videos.append(v)
        if len(videos) >= max_results:
            return videos
    return videos

'''
def find(query, max_results=10, offset=1, orderBy='relevance', video_url_base=None):
  url = "http://youtube.com/results?search_query=%s&search=Search" % quote(query)
  data = readUrlUnicode(url)
  regx = re.compile(' <a href="/watch.v=(.*?)" title="(.*?)" ')
  regx = re.compile('<a href="/watch\?v=(\w*?)" ><img src="(.*?)"  class="vimg120" title="(.*?)" alt="video">')
  id_title = regx.findall(data)
  data_flat = data.replace('\n', ' ')
  videos = {}
  for video in id_title:
    vid = video[0]
    if vid not in videos:
      v = dict()
      v['id'] = vid
      v['link'] = "http//youtube.com/watch.v=%s" % v['id']
      v['title'] = video[2].strip()
      if video_url_base:
        v['video_link'] = "%s/%s" % (video_url_base, v['id'])
      else:
        v['video_url'] = getVideoUrl(v['id'])
      v['description'] = findRe(data, 'BeginvidDesc%s">(.*?)</span>' % v['id']).strip().replace('<b>', ' ').replace('</b>', '')
      v['thumbnail'] = video[1]
    videos[vid] = v
    if len(videos) >= max_results:
        return videos.values()
  return videos.values()
'''

