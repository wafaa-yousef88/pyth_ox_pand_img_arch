import json
import re

from ox.cache import readUrlUnicode

HEADERS = {
    'User-Agent': 'iTunes/10.4 (Macintosh; Intel Mac OS X 10.7) AppleWebKit/534.48.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us, en;q=0.50',
    'X-Apple-Store-Front': '143441-1,12',
    'X-Apple-Tz': '7200',
    'Accept-Encoding': 'gzip, deflate'
}
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7) '
USER_AGENT += 'AppleWebKit/534.48.3 (KHTML, like Gecko) Version/5.1 Safari/534.48.3'

def getMovieData(title, director):
    data = {}
    # itunes section (preferred source for link)
    url = 'http://ax.search.itunes.apple.com/WebObjects/MZSearch.woa/wa/advancedSearch'
    url += '?media=movie&movieTerm=' + title
    url += '&actorNames=&directorProducerName=' + director
    url += '&releaseYearTerm=&descriptionTerm=&genreIndex=1&ratingIndex=1'
    HEADERS['Referer'] = url
    html = readUrlUnicode(url, headers=HEADERS)
    regexp = '<a href="(http://itunes.apple.com/us/movie/.*?)" class="artwork-link"><div class="artwork">'
    regexp += '<img width=".*?" height=".*?" alt=".*?" class="artwork" src="(.*?)" /></div></a>'
    results = re.compile(regexp).findall(html)
    if results:
        data['link'] = results[0][0]
        data['poster'] = results[0][1].replace('140x140', '600x600')
        html = readUrlUnicode(data['link'], headers=HEADERS)
        results = re.compile('video-preview-url="(.*?)"').findall(html)
        if results:
            data['trailer'] = results[0]
    # trailers section (preferred source for poster and trailer)
    host = 'http://trailers.apple.com'
    url = host + '/trailers/home/scripts/quickfind.php?callback=searchCallback&q=' + title
    js = json.loads(readUrlUnicode(url)[16:-4])
    results = js['results']
    if results:
        url = host + results[0]['location']
        if not 'link' in data:
            data['link'] = url
        headers = {
            'User-Agent': USER_AGENT
        }
        html = readUrlUnicode(url, headers=headers)
        results = re.compile('"(' + host + '.*?poster\.jpg)"').findall(html)
        if results:
            data['poster'] = results[0].replace('poster.jpg', 'poster-xlarge.jpg')
        html = readUrlUnicode(url + 'includes/playlists/web.inc', headers=headers)
        results = re.compile('"(' + host + '\S+\.mov)"').findall(html)
        if results:
            data['trailer'] = results[-1]
    return data

if __name__ == '__main__':
    print getMovieData('Alphaville', 'Jean-Luc Godard')
    print getMovieData('Sin City', 'Roberto Rodriguez')
    print getMovieData('Breathless', 'Jean-Luc Godard')
    print getMovieData('Capitalism: A Love Story', 'Michael Moore')
    print getMovieData('Film Socialisme', 'Jean-Luc Godard')
