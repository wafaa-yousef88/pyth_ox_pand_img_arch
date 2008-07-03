# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2007 by j@mailb.org

from threading import Event
import sha
from os import stat

from BitTornado.BT1.makemetafile import make_meta_file
from BitTornado.bencode import bencode, bdecode


def createTorrent(file, url, params = {}, flag = Event(),
                   progress = lambda x: None, progress_percent = 1):
    "Creates a torrent for a given file, using url as tracker url"
    return make_meta_file(file, url, params, flag, progress, progress_percent)

def getInfoHash(torrentFile):
    "Returns Torrent Info Hash from torrent file"
    metainfo_file = open(torrentFile, 'rb')
    metainfo = bdecode(metainfo_file.read())
    info = metainfo['info']
    return sha.sha(bencode(info)).hexdigest().upper()

def getTorrentInfoFromFile(torrentFile):
    f = open(torrentFile, 'rb')
    data = f.read()
    f.close()
    tinfo = getTorrentInfo(data)
    tinfo['timestamp'] = stat(torrentFile).st_ctime
    return tinfo

def getTorrentInfo(data):
    "Returns Torrent Info from torrent file"
    tinfo = {}
    metainfo = bdecode(data)
    info = metainfo['info']
    piece_length = info['piece length']
    if info.has_key('length'):
        # let's assume we just have one file
        file_length = info['length']
    else:
        # let's assume we have a directory structure
        file_length = 0;
        for f in info['files']:
            file_length += f['length']
    for key in info:
        if key != 'pieces':
            tinfo[key] = info[key]
    for key in metainfo:
        if key != 'info':
            tinfo[key] = metainfo[key]
    tinfo['size'] = file_length
    tinfo['hash'] = sha.sha(bencode(info)).hexdigest()
    tinfo['announce'] = metainfo['announce']
    return tinfo

def getTorrentSize(torrentFile):
    "Returns Size of files in torrent file in bytes"
    return getTorrentInfo(torrentFile)['size']

