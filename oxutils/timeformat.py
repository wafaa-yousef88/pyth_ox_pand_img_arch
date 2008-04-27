# -*- coding: utf-8 -*-
# vi:si:et:sw=2:sts=2:ts=2
from numbers import plural

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

