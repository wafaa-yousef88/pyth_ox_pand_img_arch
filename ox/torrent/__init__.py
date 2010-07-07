# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2007-2009

from threading import Event
import hashlib
import os

from bencode import bencode, bdecode

__all__ = ['createTorrent', 'getInfoHash', 'getTorrentInfoFromFile', 'getTorrentInfo', 'getFiles', 'getTorrentSize']

def createTorrent(file, url, params = {}, flag = Event(),
                   progress = lambda x: None, progress_percent = 1):
    "Creates a torrent for a given file, using url as tracker url"
    from makemetafile import make_meta_file
    return make_meta_file(file, url, params, flag, progress, progress_percent)

def getInfoHash(torrentFile):
    "Returns Torrent Info Hash from torrent file"
    metainfo_file = open(torrentFile, 'rb')
    metainfo = bdecode(metainfo_file.read())
    info = metainfo['info']
    return hashlib.sha1(bencode(info)).hexdigest()

def getTorrentInfoFromFile(torrentFile):
    f = open(torrentFile, 'rb')
    data = f.read()
    f.close()
    tinfo = getTorrentInfo(data)
    tinfo['timestamp'] = os.stat(torrentFile).st_ctime
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
    tinfo['hash'] = hashlib.sha1(bencode(info)).hexdigest()
    tinfo['announce'] = metainfo['announce']
    return tinfo

def getFiles(data):
    files = []
    info = getTorrentInfo(data)
    if 'files' in info:
        for f in info['files']:
            path = [info['name'], ]
            path.extend(f['path'])
            files.append(os.path.join(*path))
    else:
        files.append(info['name'])
    return files

def getTorrentSize(torrentFile):
    "Returns Size of files in torrent file in bytes"
    return getTorrentInfo(torrentFile)['size']

