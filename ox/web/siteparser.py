# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
from datetime import datetime

from ox.cache import readUrlUnicode
from ox import stripTags, decodeHtml


def cleanup(key, data, data_type):
    if data:
        if isinstance(data[0], basestring):
            #FIXME: some types need stripTags
            #data = [stripTags(decodeHtml(p)).strip() for p in data]
            data = [decodeHtml(p).strip() for p in data]
        elif isinstance(data[0], list) or isinstance(data[0], tuple):
            data = [cleanup(key, p, data_type) for p in data]
        while len(data) == 1:
            data = data[0]
        if data_type == 'list' and isinstance(data, basestring):
            data = [data, ]
    elif data_type != 'list':
        data = ''
    return data

class SiteParser(dict):
    baseUrl = ''
    regex = {}

    def getUrl(self, page):
        return "%s%s" % (self.baseUrl, page)

    def __init__(self):
        for key in self.regex:
            url = self.getUrl(self.regex[key]['page'])
            data = readUrlUnicode(url)
            if isinstance(self.regex[key]['re'], basestring):
                data = re.compile(self.regex[key]['re'], re.DOTALL).findall(data)
                data = cleanup(key, data, self.regex[key]['type'])
            else:
                for r in self.regex[key]['re']:
                    if isinstance(data, basestring):
                        data = re.compile(r, re.DOTALL).findall(data)
                    else:
                        data = [re.compile(r, re.DOTALL).findall(d) for d in data]
                        data = cleanup(key, data, self.regex[key]['type'])
            def apply_f(f, data):
                if data and isinstance(data[0], list):
                    data = [f(d) for d in data]
                else:
                    data = f(data)
                return data
            if self.regex[key]['type'] == 'float':
                data = apply_f(float, data)
            elif self.regex[key]['type'] == 'int':
                data = apply_f(int, data)
            elif self.regex[key]['type'] == 'date':
                parse_date = lambda d: d and datetime.strptime('-'.join(d), '%m-%d-%Y').strftime('%Y-%m-%d')
                data = apply_f(parse_date, data)
            self[key] = data

