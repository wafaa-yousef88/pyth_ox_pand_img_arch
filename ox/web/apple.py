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

def getMovieData(title, director):
    data = None
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
        data = {
            'link': results[0][0],
            'poster': results[0][1].replace('140x140', '600x600')
        }
        html = readUrlUnicode(data['link'], headers=HEADERS)
        regexp = 'video-preview-url="(.*?)"'
        results = re.compile(regexp).findall(html)
        if results:
            data['trailer'] = results[0]
    return data

if __name__ == '__main__':
    print getMovieData('Alphaville', 'Jean-Luc Godard')
    print getMovieData('Sin City', 'Roberto Rodriguez')