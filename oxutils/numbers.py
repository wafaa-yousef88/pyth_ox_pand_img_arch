# -*- coding: utf-8 -*-
# vi:si:et:sw=2:sts=2:ts=2
# Written 2007 by j@mailb.org
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

"""
Format the value like a 'human-readable' file size (i.e. 13 KB, 4.1 MB, 102
bytes, etc).
  number - number to format.
  long_name - long name. i.e. byte
  short - short name, i.e. B
"""
def formatNumber(number, long_name, short):
  if not number:
    return "0 %ss" % long_name
  number = float(number)
  if number < 1024:
    return "%d %s%s" % (number, long_name, number != 1 and 's' or '')
  if number < 1024 * 1024:
    return "%d K%s" % ((number / 1024), short)
  if number < 1024 * 1024 * 1024:
    return "%.1f M%s" % (number / (1024 * 1024), short)
  if number < 1024 * 1024 * 1024 * 1024:
    return "%.2f G%s" % (number / (1024 * 1024 * 1024), short)
  return "%.3f T%s" % (number / (1024 * 1024 * 1024 * 1024), short)

def formatBytes(number):
  return formatNumber(number, 'byte', 'B')

def formatBit(number):
  return formatNumber(number, 'bit', 'b')

'''
seperate number with thousand comma
'''
def numberThousands(n, sep=','):
  if n < 1000:
    return "%s" % n
  ln = list(str(n))
  ln.reverse()
  newn = []
  while len(ln) > 3:
    newn.extend(ln[:3])
    newn.append(sep)
    ln = ln[3:]
    newn.extend(ln)
    newn.reverse()
  return "".join(newn)

def plural(amount, unit, plural='s'):
  if abs(amount) != 1:
    if plural == 's':
      unit = unit + plural
    else: unit = plural
  return "%s %s" % (formatNumber(amount), unit)

