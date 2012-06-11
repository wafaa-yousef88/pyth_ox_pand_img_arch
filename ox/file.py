# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008
from __future__ import division
import os
import hashlib
import re
import sys
import struct
import subprocess

from ox.utils import json

__all__ = ['sha1sum', 'oshash', 'avinfo', 'makedirs']

def cmd(program):
    local = os.path.expanduser('~/.ox/bin/%s' % program)
    if os.path.exists(local):
        program = local
    return program

def sha1sum(filename):
    sha1 = hashlib.sha1()
    file=open(filename)
    buffer=file.read(4096)
    while buffer:
        sha1.update(buffer)
        buffer=file.read(4096)
    file.close()
    return sha1.hexdigest()

'''
    os hash - http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes
    plus modification for files < 64k, buffer is filled with file data and padded with 0
'''
def oshash(filename):
    try:
        longlongformat = 'q'  # long long
        bytesize = struct.calcsize(longlongformat)

        f = open(filename, "rb")

        filesize = os.path.getsize(filename)
        hash = filesize
        if filesize < 65536:
            for x in range(int(filesize/bytesize)):
                buffer = f.read(bytesize)
                (l_value,)= struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number
        else:
            for x in range(int(65536/bytesize)):
                buffer = f.read(bytesize)
                (l_value,)= struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number
            f.seek(max(0,filesize-65536),0)
            for x in range(int(65536/bytesize)):
                buffer = f.read(bytesize)
                (l_value,)= struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF
        f.close()
        returnedhash =  "%016x" % hash
        return returnedhash
    except(IOError):
        return "IOError"

def avinfo(filename):
    if os.path.getsize(filename):
        ffmpeg2theora = cmd('ffmpeg2theora')
        p = subprocess.Popen([ffmpeg2theora], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        info, error = p.communicate()
        version = info.split('\n')[0].split(' - ')[0].split(' ')[-1]
        if version < '0.27':
            raise EnvironmentError('version of ffmpeg2theora needs to be 0.27 or later, found %s' % version)
        p = subprocess.Popen([ffmpeg2theora, '--info', filename],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        info, error = p.communicate()
        try:
            info = json.loads(info)
        except:
            #remove metadata, can be broken
            reg = re.compile('"metadata": {.*?},', re.DOTALL)
            info = re.sub(reg, '', info)
            info = json.loads(info)
        if 'video' in info:
            for v in info['video']:
                if not 'display_aspect_ratio' in v and 'width' in v:
                    v['display_aspect_ratio'] = '%d:%d' % (v['width'], v['height'])
                    v['pixel_aspect_ratio'] = '1:1'
        return info

    return {'path': filename, 'size': 0}

def ffprobe(filename):
    p = subprocess.Popen([
        cmd('ffprobe'),
        '-show_format',
        '-show_streams',
        '-print_format',
        'json',
        '-i', filename

    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info, error = p.communicate()
    ffinfo = json.loads(info)

    def fix_value(key, value):
        if key == 'r_frame_rate':
            value = value.replace('/', ':')
        elif key == 'bit_rate':
            value = float(value) / 1000
        elif key == 'duration':
            value = float(value)
        elif key == 'size':
            value = int(value)
        return value

    info = {}
    for key in ('duration', 'size', 'bit_rate'):
        info[{
            'bit_rate': 'bitrate'
        }.get(key, key)] = fix_value(key, ffinfo['format'][key])
    info['audio'] = []
    info['video'] = []
    info['metadata'] = ffinfo['format'].get('tags', {})
    for s in ffinfo['streams']:
        tags =  s.pop('tags', {})
        for t in tags:
            info['metadata'][t] = tags[t]
        if s.get('codec_type') in ('audio', 'video'):
            stream = {}
            keys = [ 
                'codec_name',
                'width',
                'height',
                'bit_rate',
                'index',
                'display_aspect_ratio',
                'sample_rate',
                'channels',
            ]
            if s['codec_type'] == 'video':
                keys += [
                    'sample_aspect_ratio',
                    'r_frame_rate',
                    'pix_fmt',
                ]

            for key in keys:
                if key in s:
                    stream[{
                        'codec_name': 'codec',
                        'bit_rate': 'bitrate',
                        'index': 'id',
                        'r_frame_rate': 'framerate',
                        'sample_rate': 'samplerate',
                        'pix_fmt': 'pixel_format',
                    }.get(key, key)] = fix_value(key, s[key])
            info[s['codec_type']].append(stream)
        else:
            pass
            #print s
    for v in info['video']:
        if not 'display_aspect_ratio' in v and 'width' in v:
            v['display_aspect_ratio'] = '%d:%d' % (v['width'], v['height'])
            v['pixel_aspect_ratio'] = '1:1'
    info['oshash'] = ox.oshash(filename)
    info['path'] = os.path.basename(filename)
    return info

def makedirs(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError, e:
            if e.errno != 17:
                raise

def copy_file(source, target, verbose=False):
    if verbose:
        print 'copying', source, 'to', target
    write_file(target, read_file(source))

def read_file(file, verbose=False):
    if verbose:
        print 'reading', file
    f = open(file)
    data = f.read()
    f.close()
    return data

def read_json(file, verbose=False):
    return json.loads(read_file(file, verbose=verbose))

def write_file(file, data, verbose=False):
    if verbose:
        print 'writing', file
    write_path(file)
    f = open(file, 'w')
    f.write(data)
    f.close()
    return len(data)

def write_json(file, data, indent=0, sort_keys=False, verbose=False):
    data = json.dumps(data, indent=indent, sort_keys=sort_keys)
    write_file(file, data, verbose=verbose)

def write_link(source, target, verbose=False):
    if verbose:
        print 'linking', source, 'to', target
    write_path(target)
    if os.path.exists(target):
        os.unlink(target)
    os.symlink(source, target)

def write_path(file):
    path = os.path.split(file)[0]
    if path and not os.path.exists(path):
        os.makedirs(path)
