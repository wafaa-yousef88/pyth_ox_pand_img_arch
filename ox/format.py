# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import math
import re
import string

def to32(q):
    """
    Converts an integer to base 32
    We exclude 4 of the 26 letters: I L O U.
    http://www.crockford.com/wrmg/base32.html

    >>> for i in range(0, 1000): assert from32(to32(i)) == i
    
    >>> to32(0)
    '0'

    >>> to32(347485647)
    'ABCDEF'

    >>> to32(555306645)
    'GHJKMN'

    >>> to32(800197332334559L)
    'PQRSTVWXYZ'

    >>> to32(32)
    '10'

    >>> to32(119292)
    '3MFW'

    >>> to32(939387374)
    'VZVTFE'

    >>> to32(-1)
    Traceback (most recent call last):
        ...
    ValueError: must supply a positive integer
    """

    if q < 0: raise ValueError, "must supply a positive integer"
    letters = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
    converted = []
    while q != 0:
        q, r = divmod(q, 32)
        l = letters[r]
        converted.insert(0, l)
    return "".join(converted) or '0'

def from32(q):
    """
    Converts an base 32 string to an integer
    We exclude 4 of the 26 letters: I L O U.
    http://www.crockford.com/wrmg/base32.html

    >>> from32('A')
    10

    >>> from32('i')
    1

    >>> from32('Li1l')
    33825

    >>> from32('10')
    32
    """
    _32map = {
        '0': 0,
        'O': 0,
        '1': 1,
        'I': 1,
        'L': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'A': 10,
        'B': 11,
        'C': 12,
        'D': 13,
        'E': 14,
        'F': 15,
        'G': 16,
        'H': 17,
        'J': 18,
        'K': 19,
        'M': 20,
        'N': 21,
        'P': 22,
        'Q': 23,
        'R': 24,
        'S': 25,
        'T': 26,
        'V': 27,
        'W': 28,
        'X': 29,
        'Y': 30,
        'Z': 31,
    }
    base32 = ('0123456789' +string.ascii_uppercase)[:32]
    q = q.replace('-','')
    q = ''.join([base32[_32map[i.upper()]] for i in q])
    return int(q, 32)

def to36(q):
    """
    Converts an integer to base 36 (a useful scheme for human-sayable IDs
    like 'fuck' (739172), 'shit' (1329077) or 'hitler' (1059538851)).

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

def intValue(strValue, default=u''):
    """
    >>> intValue('abc23')
    u'23'

    >>> intValue(' abc23')
    u'23'

    >>> intValue('ab')
    u''
    """
    try:
        val = re.compile('(\d+)').findall(unicode(strValue).strip())[0]
    except:
        val = default
    return val

def floatValue(strValue, default=u''):
    """
    >>> floatValue('abc23.4')
    u'23.4'

    >>> floatValue(' abc23.4')
    u'23.4'

    >>> floatValue('ab')
    u''
    """
    try:
        val = re.compile('([\d.]+)').findall(unicode(strValue).strip())[0]
    except:
        val = default
    return val

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

    >>> formatNumber(-1234567890123456789, 'Byte', 'B')
    '-1,096.5166 PB'

    """
    if abs(number) < 1024:
        return '%s %s%s' % (formatThousands(number), longName, number != 1 and 's' or '')
    prefix = ['K', 'M', 'G', 'T', 'P']
    for i in range(5):
        if abs(number) < math.pow(1024, i + 2) or i == 4:
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

def formatDuration(ms, verbosity=0, years=True, hours=True, milliseconds=True):
    '''
    verbosity
        0: D:HH:MM:SS
        1: Dd Hh Mm Ss
        2: D days H hours M minutes S seconds
    years
        True: 366 days are 1 year 1 day
        False: 366 days are 366 days
    hours
        True: 30 seconds are 00:00:30
        False: 30 seconds are 00:30
    milliseconds
        True: always display milliseconds
        False: never display milliseconds
    >>> formatDuration(1000 * 60 * 60 * 24 * 366)
    '1:001:00:00:00.000'
    >>> formatDuration(1000 * 60 * 60 * 24 * 366, years=False)
    '366:00:00:00.000'
    >>> formatDuration(1000 * 60 * 60 * 24 * 365 + 2003, verbosity=2)
    '1 year 2 seconds 3 milliseconds'
    >>> formatDuration(1000 * 30, hours=False, milliseconds=False)
    '00:30'
    '''
    if not ms and ms != 0:
        return ''
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
    if shortenLong and ms > 1000 * 60 * 60 * 24 * 464:
        return formatDuration(ms, verbosity=1, milliseconds=False)
    return formatDuration(ms, verbosity=2, milliseconds=False)

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
    return formatDuration(ms, hours=False, years=False, milliseconds=False)

def ms2time(ms):
    # deprecated - use formatDuration
    '''
    >>> ms2time(44592123)
    '12:23:12.123'
    '''
    return formatDuration(ms, years=False)

def time2ms(timeString):
    '''
    >>> time2ms('12:23:12.123')
    44592123
    '''
    ms = 0.0
    p = timeString.split(':')
    for i in range(len(p)):
        _p = p[i]
        if _p.endswith('.'): _p =_p[:-1]
        ms = ms * 60 + float(_p)
    return int(ms * 1000)

def shiftTime(offset, timeString):
    newTime = time2ms(timeString) + offset
    return ms2time(newTime)

