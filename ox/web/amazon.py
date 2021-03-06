# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
from urllib import quote

from ox import find_re, strip_tags, decode_html
from ox.cache import read_url


def findISBN(title, author):
    q = '%s %s' % (title, author)
    url = "http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dstripbooks&field-keywords=" + "%s&x=0&y=0" % quote(q)
    data = read_url(url, unicode=True)
    links = re.compile('href="(http://www.amazon.com/.*?/dp/.*?)"').findall(data)
    id = find_re(re.compile('href="(http://www.amazon.com/.*?/dp/.*?)"').findall(data)[0], '/dp/(.*?)/')
    data = get_data(id)
    if author in data['authors']:
        return data
    return {}

def get_data(id):
    url = "http://www.amazon.com/title/dp/%s/" % id
    data = read_url(url, unicode=True)


    def find_data(key):
        return find_re(data, '<li><b>%s:</b>(.*?)</li>'% key).strip()

    r = {}
    r['amazon'] = url
    r['title'] = find_re(data, '<span id="btAsinTitle" style="">(.*?)<span')
    r['authors'] = re.compile('<b class="h3color">(.*?)</b>.*?\(Author\)', re.DOTALL).findall(data)
    r['authors'] = filter(lambda x: len(x)>1, [decode_html(a) for a in r['authors']])
    t = re.compile('>(.*?)</a> \(Translator\)').findall(data)
    if t:
        r['translator'] = t
    r['publisher'] = find_data('Publisher')
    r['language'] = find_data('Language')
    r['isbn-10'] = find_data('ISBN-10')
    r['isbn-13'] = find_data('ISBN-13').replace('-', '')
    r['dimensions'] = find_re(data, '<li><b>.*?Product Dimensions:.*?</b>(.*?)</li>')

    r['pages'] = find_data('Paperback')
    if not r['pages']:
        r['pages'] = find_data('Hardcover')

    r['review'] = strip_tags(find_re(data, '<h3 class="productDescriptionSource">Review</h3>.*?<div class="productDescriptionWrapper">(.*?)</div>').replace('<br />', '\n')).strip()

    r['description'] = strip_tags(find_re(data, '<h3 class="productDescriptionSource">Product Description</h3>.*?<div class="productDescriptionWrapper">(.*?)</div>').replace('<br />', '\n')).strip()

    r['cover'] = re.findall('src="(.*?)" id="prodImage"', data)
    if r['cover']:
        r['cover'] = r['cover'][0].split('._BO2')[0]
        if not r['cover'].endswith('.jpg'):
            r['cover'] = r['cover'] + '.jpg'
        if 'no-image-avail-img' in r['cover']:
            del r['cover']
    else:
        del r['cover']
    return r

