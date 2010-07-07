# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from ox.cache import readUrl
from ox.html import decodeHtml
from ox.text import findRe


def getLyrics(title, artist):
    html = readUrl('http://lyricsfly.com/api/')
    key = findRe(html, '<font color=green><b>(.*?)</b></font>')
    url = 'http://lyricsfly.com/api/api.php?i=%s&a=%s&t=%s' % (key, artist, title)
    xml = readUrl(url)
    lyrics = findRe(xml, '<tx>(.*?)\[br\] Lyrics [a-z]* by lyricsfly.com')
    lyrics = lyrics.replace('\n', '').replace('\r', '')
    lyrics = lyrics.replace('[br]', '\n').strip()
    lyrics.replace('\n\n\n', '\n\n')
    lyrics = decodeHtml(lyrics.replace('&amp;', '&'))
    return lyrics

if __name__ == '__main__':
    print getLyrics('Election Day', 'Arcadia')
