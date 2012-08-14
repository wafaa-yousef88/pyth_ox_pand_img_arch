# vi:si:et:sw=4:sts=4:ts=4
# encoding: utf-8
import re
import urllib

from ox.cache import read_url
from ox.html import decodeHtml, strip_tags
from ox.text import findRe
from ox.text import findString


# to sniff itunes traffic, use something like
# sudo tcpdump -i en1 -Avs 8192 host appleglobal.112.2o7.net

# http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZSearch.woa/wa/advancedSearch?media=music&songTerm=&genreIndex=1&flavor=0&mediaType=2&composerTerm=&allArtistNames=Arcadia&ringtone=0&searchButton=submit
# http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZSearch.woa/wa/advancedSearch?media=movie&movieTerm=The%20Matrix&descriptionTerm=&ratingIndex=1&mediaType=3&directorProducerName=Andy%20Wachowski&flavor=0&releaseYearTerm=1999&closedCaption=0&actorTerm=&searchButton=submit

ITUNES_HEADERS = {
    'X-Apple-Tz': '0',
    'X-Apple-Storefront': '143441-1',
    'User-Agent': 'iTunes/7.6.2 (Macintosh; U; Intel Mac OS X 10.5.2)',
    'Accept-Language': 'en-us, en;q=0.50',
    'Accept-Encoding': 'gzip',
    'Connection': 'close',
}

def composeUrl(request, parameters):
    if request == 'advancedSearch':
        url = 'http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZSearch.woa/wa/advancedSearch?'
        if parameters['media'] == 'music':
            url += urllib.urlencode({
              'albumTerm': parameters['title'],
              'allArtistNames': parameters['artist'],
              'composerTerm': '',
              'flavor': 0,
              'genreIndex': 1,
              'media': 'music',
              'mediaType': 2,
              'ringtone': 0,
              'searchButton': 'submit',
              'songTerm': ''
            })
        elif parameters['media'] == 'movie':
            url += urllib.urlencode({
              'actorTerm': '',
              'closedCaption': 0,
              'descriptionTerm': '',
              'directorProducerName': parameters['director'],
              'flavor': 0,
              'media': 'movie',
              'mediaType': 3,
              'movieTerm': parameters['title'],
              'ratingIndex': 1,
              'releaseYearTerm': '',
              'searchButton': 'submit'
            })
    elif request == 'viewAlbum':
        url = 'http://phobos.apple.com/WebObjects/MZStore.woa/wa/viewAlbum?id=%s' % parameters['id']
    elif request == 'viewMovie':
        url = 'http://phobos.apple.com/WebObjects/MZStore.woa/wa/viewMovie?id=%s&prvw=1' % parameters['id']
    return url

def parseXmlDict(xml):
    values = {}
    strings = xml.split('<key>')
    for string in strings:
        if string.find('</key>') != -1:
            key = findRe(string, '(.*?)</key>')
            type = findRe(string, '</key><(.*?)>')
            if type == 'true/':
                value = True
            else:
                value = findRe(string, '<%s>(.*?)</%s>' % (type, type))
                if type == 'integer':
                  value = int(value)
                elif type == 'string':
                  value = decodeHtml(value)
            values[key] = value
    return values

def parseCast(xml, title):
    list = []
    try:
        strings = findRe(xml, '<SetFontStyle normalStyle="textColor">%s(.*?)</VBoxView>' % title[:-1].upper()).split('</GotoURL>')
        strings.pop()
        for string in strings:
            list.append(findRe(string, '<SetFontStyle normalStyle="textColor">(.*?)</SetFontStyle>'))
        return list
    except:
        return list

def parseMovies(xml, title):
    list = []
    try:
        strings = findRe(xml, '<SetFontStyle normalStyle="outlineTitleFontStyle"><b>%s(.*?)</Test>' % title[:-1].upper()).split('</GotoURL>')
        strings.pop()
        for string in strings:
            list.append({
              'id': findRe(string, 'viewMovie\?id=(.*?)&'),
              'title': findRe(string, '<SetFontStyle normalStyle="outlineTextFontStyle"><b>(.*?)</b></SetFontStyle>')
            })
        return list
    except:
        return list

class ItunesAlbum:
    def __init__(self, id = '', title = '', artist = ''):
        self.id = id
        self.title = title
        self.artist = artist
        if not id:
            self.id = self.getId()

    def getId(self):
        url = composeUrl('advancedSearch', {'media': 'music', 'title': self.title, 'artist': self.artist})
        xml = read_url(url, headers = ITUNES_HEADERS)
        id = findRe(xml, 'viewAlbum\?id=(.*?)&')
        return id

    def getData(self):
        data = {'id': self.id}
        url = composeUrl('viewAlbum', {'id': self.id})
        xml = read_url(url, None, ITUNES_HEADERS)
        data['albumName'] = findRe(xml, '<B>(.*?)</B>')
        data['artistName'] = findRe(xml, '<b>(.*?)</b>')
        data['coverUrl'] = findRe(xml, 'reflection="." url="(.*?)"')
        data['genre'] = findRe(xml, 'Genre:(.*?)<')
        data['releaseDate'] = findRe(xml, 'Released(.*?)<')
        data['review'] = strip_tags(findRe(xml, 'REVIEW</b>.*?<SetFontStyle normalStyle="textColor">(.*?)</SetFontStyle>'))
        data['tracks'] = []
        strings = findRe(xml, '<key>items</key>.*?<dict>(.*?)$').split('<dict>')
        for string in strings:
          data['tracks'].append(parseXmlDict(string))
        data['type'] = findRe(xml, '<key>listType</key><string>(.*?)<')
        return data

class ItunesMovie:
    def __init__(self, id = '', title = '', director = ''):
        self.id = id
        self.title = title
        self.director = director
        if not id:
            self.id = self.getId()

    def getId(self):
        url = composeUrl('advancedSearch', {'media': 'movie', 'title': self.title, 'director': self.director})
        xml = read_url(url, headers = ITUNES_HEADERS)
        id = findRe(xml, 'viewMovie\?id=(.*?)&')
        return id

    def getData(self):
        data = {'id': self.id}
        url = composeUrl('viewMovie', {'id': self.id})
        xml = read_url(url, None, ITUNES_HEADERS)
        f = open('/Users/rolux/Desktop/iTunesData.xml', 'w')
        f.write(xml)
        f.close()
        data['actors'] = parseCast(xml, 'actors')
        string = findRe(xml, 'Average Rating:(.*?)</HBoxView>')
        data['averageRating'] = string.count('rating_star_000033.png') + string.count('&#189;') * 0.5
        data['directors'] = parseCast(xml, 'directors')
        data['format'] = findRe(xml, 'Format:(.*?)<')
        data['genre'] = decodeHtml(findRe(xml, 'Genre:(.*?)<'))
        data['plotSummary'] = decodeHtml(findRe(xml, 'PLOT SUMMARY</b>.*?<SetFontStyle normalStyle="textColor">(.*?)</SetFontStyle>'))
        data['posterUrl'] = findRe(xml, 'reflection="." url="(.*?)"')
        data['producers'] = parseCast(xml, 'producers')
        data['rated'] = findRe(xml, 'Rated(.*?)<')
        data['relatedMovies'] = parseMovies(xml, 'related movies')
        data['releaseDate'] = findRe(xml, 'Released(.*?)<')
        data['runTime'] = findRe(xml, 'Run Time:(.*?)<')
        data['screenwriters'] = parseCast(xml, 'screenwriters')
        data['soundtrackId'] = findRe(xml, 'viewAlbum\?id=(.*?)&')
        data['trailerUrl'] = findRe(xml, 'autoplay="." url="(.*?)"')
        return data

if __name__ == '__main__':
    from ox.utils import json
    data = ItunesAlbum(title = 'So Red the Rose', artist = 'Arcadia').getData()
    print json.dumps(data, sort_keys = True, indent = 4)
    data = ItunesMovie(title = 'The Matrix', director = 'Wachowski').getData()
    print json.dumps(data, sort_keys = True, indent = 4)
    for v in data['relatedMovies']:
        data = ItunesMovie(id = v['id']).getData()
        print json.dumps(data, sort_keys = True, indent = 4)
    data = ItunesMovie(id='272960052').getData()
    print json.dumps(data, sort_keys = True, indent = 4)

