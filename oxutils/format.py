# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import math
import re

def to36(q):
    """
    Converts an integer to base 36 (a useful scheme for human-sayable IDs).

    >>> to36(35)
    'z'
    >>> to36(119292)
    '2k1o'
    >>> int(to36(939387374), 36)
    939387374
    >>> to36(0)
    '0'
    >>> to36(-393)
    Traceback (most recent call last):
        ...
    ValueError: must supply a positive integer
    """
    if q < 0: raise ValueError, "must supply a positive integer"
    letters = "0123456789abcdefghijklmnopqrstuvwxyz"
    converted = []
    while q != 0:
        q, r = divmod(q, 36)
        converted.insert(0, letters[r])
    return "".join(converted) or '0'

def from36(q):
    return int(q, 36)

def intValue(strValue, default=''):
    try:
        val = re.compile('(\d+)').findall(unicode(strValue).strip())[0]
    except:
        val = default
    return val

def test_intValue():
    assert intValue('abc23') == '23'
    assert intValue(' abc23') == '23'
    assert intValue(' abc') == ''

def floatValue(strValue, default=''):
    try:
        val = re.compile('([\d.]+)').findall(unicode(strValue).strip())[0]
    except:
        val = default
    return val

def test_floatValue():
    assert floatValue('abc23.4') == '23.4'
    assert floatValue(' abc23.4') == '23.4'
    assert floatValue(' abc') == ''

def formatNumber(number, longName, shortName):
    """
    Return the number in a human-readable format (23 KB, 23.4 MB, 23.42 GB)
    
    >>> formatNumber(123, 'Byte', 'B')
    '123 Bytes'

    >>> formatNumber(1234, 'Byte', 'B')
    '1 KB'

    >>> formatNumber(1234567, 'Byte', 'B')
    '1.2 MB'

    >>> formatNumber(1234567890, 'Byte', 'B')
    '1.15 GB'

    >>> formatNumber(1234567890123456789, 'Byte', 'B')
    '1,096.5166 PB'

    """
    if number < 1024:
        return '%s %s%s' % (formatThousands(number), longName, number != 1 and 's' or '')
    prefix = ['K', 'M', 'G', 'T', 'P']
    for i in range(5):
        if number < math.pow(1024, i + 2) or i == 4:
            n = number / math.pow(1024, i + 1)
            return '%s %s%s' % (formatThousands('%.*f' % (i, n)), prefix[i], shortName)

def formatThousands(number, separator = ','):
    """
    Return the number with separators (1,000,000)
    
    >>> formatThousands(1)
    '1'
    >>> formatThousands(1000)
    '1,000'
    >>> formatThousands(1000000)
    '1,000,000'
    """
    string = str(number).split('.')
    l = []
    for i, character in enumerate(reversed(string[0])):
        if i and (not (i % 3)):
            l.insert(0, separator)
        l.insert(0, character)
    string[0] = ''.join(l)
    return '.'.join(string)

def formatBits(number):
    return formatNumber(number, 'bit', 'b')

def formatBytes(number):
    return formatNumber(number, 'byte', 'B')

def formatPixels(number):
    return formatNumber(number, 'pixel', 'px')

def formatCurrency(amount, currency="$"):
  if amount:
    temp = "%.2f" % amount
    profile=re.compile(r"(\d)(\d\d\d[.,])")
    while 1:
      temp, count = re.subn(profile,r"\1,\2",temp)
      if not count:
        break
    if temp.startswith('-'):
       return "-"+ currency + temp[1:-3]
    return currency + temp[:-3]
  else:
    return ""

def plural(amount, unit, plural='s'):
    '''
    >>> plural(1, 'unit')
    '1 unit'
    >>> plural(2, 'unit')
    '2 units'
    '''
    if abs(amount) != 1:
        if plural == 's':
            unit = unit + plural
        else: unit = plural
    return "%s %s" % (formatThousands(amount), unit)

def formatDuration(ms, verbosity=0, years=False, hours=False, milliseconds=False):
    '''
        verbosity
            0: D:HH:MM:SS
            1: Dd Hh Mm Ss
            2: D days H hours M minutes S seconds
        years
            False: 366 days are 366 days
            True: 366 days are 1 year 1 day
        hours
            False: 30 seconds are 00:30
            True: 30 seconds are 00:00:30
        milliseconds
            False: never display milliseconds
            True: always display milliseconds
    '''
    if years:
        y = int(ms / 31536000000)
        d = int(ms % 31536000000 / 86400000)
    else:
        d = int(ms / 86400000)
    h = int(ms % 86400000 / 3600000)
    m = int(ms % 3600000 / 60000)
    s = int(ms % 60000 / 1000)
    ms = ms % 1000
    if verbosity == 0:
        if years and y:
            duration = "%d:%03d:%02d:%02d:%02d" % (y, d, h, m, s)
        elif d:
            duration = "%d:%02d:%02d:%02d" % (d, h, m, s)
        elif hours or h:
            duration = "%02d:%02d:%02d" % (h, m, s)
        else:
            duration = "%02d:%02d" % (m, s)
        if milliseconds:
            duration += ".%03d" % ms
    else:
        if verbosity == 1:
            durations = ["%sd" % d, "%sh" % h,  "%sm" % m, "%ss" % s]
            if years:
                durations.insert(0, "%sy" % y)
            if milliseconds:
                durations.append("%sms" % ms)
        else:
            durations = [plural(d, 'day'), plural(h,'hour'),
                plural(m, 'minute'), plural(s, 'second')]
            if years:
                durations.insert(0, plural(y, 'year'))
            if milliseconds:
                durations.append(plural(ms, 'millisecond'))
        durations = filter(lambda x: not x.startswith('0'), durations)
        duration = ' '.join(durations)
    return duration

def ms2runtime(ms, shortenLong=False):
    # deprecated - use formatDuration
    '''
    >>> ms2runtime(5000)
    '5 seconds'
    >>> ms2runtime(500000)
    '8 minutes 20 seconds'
    >>> ms2runtime(50000000)
    '13 hours 53 minutes 20 seconds'
    >>> ms2runtime(50000000-20000)
    '13 hours 53 minutes'
    '''
    y = int(ms / 31536000000)
    d = int(ms % 31536000000 / 86400000)
    h = int(ms % 86400000 / 3600000)
    m = int(ms % 3600000 / 60000)
    s = int(ms % 60000 / 1000)
    if shortenLong and y > 0 or d > 99:
        runtimeString = ("%sy" % y, "%sd" % d, "%sh" % h,  "%sm" % m, "%ss" % s)
    else:
        runtimeString = (plural(y, 'year'), plural(d, 'day'),
                         plural(h,'hour'), plural(m, 'minute'), plural(s, 'second'))
    runtimeString = filter(lambda x: not x.startswith('0'), runtimeString)
    return ' '.join(runtimeString).strip()

def ms2playtime(ms, hours=False):
    # deprecated - use formatDuration
    '''
    >>> ms2playtime(5000)
    '00:05'
    >>> ms2playtime(500000)
    '08:20'
    >>> ms2playtime(50000000)
    '13:53:20'
    '''
    d = int(ms / 86400000)
    h = int(ms % 86400000 / 3600000)
    m = int(ms % 3600000 / 60000)
    s = int(ms % 60000 / 1000)
    if d:
        playtime= "%d:%02d:%02d:%02d" % (d, h, m, s)
    elif h or hours:
        playtime= "%02d:%02d:%02d" % (h, m, s)
    else:
        playtime= "%02d:%02d" % (m, s)
    return playtime

def ms2time(ms):
    # deprecated - use formatDuration
    '''
    >>> ms2time(44592123)
    '12:23:12.123'
    '''
    it = int(ms / 1000)
    ms = ms - it*1000
    ss = it % 60
    mm = ((it-ss)/60) % 60
    hh = ((it-(mm*60)-ss)/3600) % 60
    return "%d:%02d:%02d.%03d" % (hh, mm, ss, ms)

def time2ms(timeString):
    '''
    >>> time2ms('12:23:12.123')
    44592123
    '''
    ms = 0.0
    p = timeString.split(':')
    for i in range(len(p)):
        ms = ms * 60 + float(p[i])
    return int(ms * 1000)

def shiftTime(offset, timeString):
    newTime = time2ms(timeString) + offset
    return ms2time(newTime)

