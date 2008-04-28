# -*- coding: utf-8 -*-
# vi:si:et:sw=2:sts=2:ts=2
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
    val = re.compile('(\d*)').findall(unicode(strValue))[0]
  except:
    val = default
  return val

def floatValue(strValue, default=''):
  try:
    val = re.compile('([\d.]*)').findall(unicode(strValue))[0]
  except:
    val = default
  return val

def formatNumber(number, longName, shortName):
  """
  Return the number in a human-readable format (23 KB, 23.4 MB, 23.42 GB)
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

def plural(amount, unit, plural='s'):
  if abs(amount) != 1:
    if plural == 's':
      unit = unit + plural
    else: unit = plural
  return "%s %s" % (formatNumber(amount), unit)

def ms2runtime(ms):
  seconds = int(ms / 1000)
  years = 0
  days = 0
  hours = 0
  minutes = 0
  if seconds >= 60:
    minutes = int(seconds / 60)
    seconds = seconds % 60
  if minutes >= 60:
    hours = int(minutes / 60)
    minutes = minutes % 60
  if hours >= 24:
    days = int(hours / 24)
    hours = hours % 24
  if days >= 365:
    years = int(days / 365)
    days = days % 365
  runtimeString = (plural(years, 'year'), plural(days, 'day'),
    plural(hours,'hour'), plural(minutes, 'minute'), plural(seconds, 'second'))
  runtimeString = filter(lambda x: not x.startswith('0'), runtimeString)
  return " ".join(runtimeString).strip()

def ms2playtime(ms):
  it = int(ms / 1000)
  ms = ms - it*1000
  ss = it % 60
  mm = ((it-ss)/60) % 60
  hh = ((it-(mm*60)-ss)/3600) % 60
  if hh:
    playtime= "%02d:%02d:%02d" % (hh, mm, ss)
  else:
    playtime= "%02d:%02d" % (mm, ss)
  return playtime

def ms2time(ms):
  it = int(ms / 1000)
  ms = ms - it*1000
  ss = it % 60
  mm = ((it-ss)/60) % 60
  hh = ((it-(mm*60)-ss)/3600) % 60
  return "%d:%02d:%02d.%03d" % (hh, mm, ss, ms)

def time2ms(timeString):
  ms = 0.0
  p = timeString.split(':')
  for i in range(len(p)):
    ms = ms * 60 + float(p[i])
  return int(ms * 1000)

def shiftTime(offset, timeString):
  newTime = time2ms(timeString) + offset
  return ms2time(newTime)

