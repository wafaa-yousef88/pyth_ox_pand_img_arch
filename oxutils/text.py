# -*- coding: utf-8 -*-
# vi:si:et:sw=2:sts=2:ts=2
# GPL written 2008 by j@pad.ma
import re


# Capitalizes the first letter of a string.
capfirst = lambda x: x and x[0].upper() + x[1:]

def removeSpecialCharacters(text):
  """
  Removes special characters inserted by Word.
  """
  text = text.replace(u'\u2013', '-')
  text = text.replace(u'\u2026O', "'")
  text = text.replace(u'\u2019', "'")
  text = text.replace(u'', "'")
  text = text.replace(u'', "'")
  text = text.replace(u'', "-")
  return text

def wrap(text, width):
  """
  A word-wrap function that preserves existing line breaks and most spaces in
  the text. Expects that existing line breaks are posix newlines (\n).
  See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061
  """
  return reduce(lambda line, word, width=width: '%s%s%s' %
                (line,
                  ' \n'[(len(line[line.rfind('\n')+1:])
                        + len(word.split('\n',1)[0]
                            ) >= width)],
                  word),
                text.split(' ')
                )

def truncateString(s, num):
  "Truncates a string after a certain number of chacters, but ends with a word"
  length = int(num)
  if len(s) <= length:
    return s
  words = s.split()
  ts = ""
  while words and len(ts) + len(words[0]) < length:
    ts += " " + words.pop(0)
  if words:
    ts += "..."
  return ts
    
def truncateWords(s, num):
  "Truncates a string after a certain number of words."
  length = int(num)
  words = s.split()
  if len(words) > length:
    words = words[:length]
    if not words[-1].endswith('...'):
      words.append('...')
  return ' '.join(words)

def getValidFilename(s):
  """
  Returns the given string converted to a string that can be used for a clean
  filename. Specifically, leading and trailing spaces are removed; 
  all non-filename-safe characters are removed.
  >>> get_valid_filename("john's portrait in 2004.jpg")
  'john_s portrait in 2004.jpg'
  """
  s = s.strip()
  s = s.replace(' ', '_')
  s = re.sub(r'[^-A-Za-z0-9_.\[\]\ ]', '_', s)
  s = s.replace('__', '_').replace('__', '_')
  return s

def getTextList(list_, last_word='or'):
  """
  >>> get_text_list(['a', 'b', 'c', 'd'])
  'a, b, c or d'
  >>> get_text_list(['a', 'b', 'c'], 'and')
  'a, b and c'
  >>> get_text_list(['a', 'b'], 'and')
  'a and b'
  >>> get_text_list(['a'])
  'a'
  >>> get_text_list([])
  ''
  """
  if len(list_) == 0: return ''
  if len(list_) == 1: return list_[0]
  return '%s %s %s' % (', '.join([str(i) for i in list_][:-1]), last_word, list_[-1])

def normalizeNewlines(text):
  return re.sub(r'\r\n|\r|\n', '\n', text)

def recapitalize(text):
  "Recapitalizes text, placing caps after end-of-sentence punctuation."
#  capwords = ()
  text = text.lower()
  capsRE = re.compile(r'(?:^|(?<=[\.\?\!] ))([a-z])')
  text = capsRE.sub(lambda x: x.group(1).upper(), text)
#  for capword in capwords:
#    capwordRE = re.compile(r'\b%s\b' % capword, re.I)
#    text = capwordRE.sub(capword, text)
  return text

def phone2numeric(phone):
  "Converts a phone number with letters into its numeric equivalent."
  letters = re.compile(r'[A-PR-Y]', re.I)
  char2number = lambda m: {'a': '2', 'c': '2', 'b': '2', 'e': '3',
        'd': '3', 'g': '4', 'f': '3', 'i': '4', 'h': '4', 'k': '5',
        'j': '5', 'm': '6', 'l': '5', 'o': '6', 'n': '6', 'p': '7',
        's': '7', 'r': '7', 'u': '8', 't': '8', 'w': '9', 'v': '8',
        'y': '9', 'x': '9'}.get(m.group(0).lower())
  return letters.sub(char2number, phone)

def compressString(s):
  import cStringIO, gzip
  zbuf = cStringIO.StringIO()
  zfile = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
  zfile.write(s)
  zfile.close()
  return zbuf.getvalue()

smart_split_re = re.compile('("(?:[^"\\\\]*(?:\\\\.[^"\\\\]*)*)"|\'(?:[^\'\\\\]*(?:\\\\.[^\'\\\\]*)*)\'|[^\\s]+)')
def smartSplit(text):
  """
  Generator that splits a string by spaces, leaving quoted phrases together.
  Supports both single and double quotes, and supports escaping quotes with
  backslashes. In the output, strings will keep their initial and trailing
  quote marks.
  >>> list(smart_split('This is "a person\'s" test.'))
  ['This', 'is', '"a person\'s"', 'test.']
  """
  for bit in smart_split_re.finditer(text):
      bit = bit.group(0)
      if bit[0] == '"':
          yield '"' + bit[1:-1].replace('\\"', '"').replace('\\\\', '\\') + '"'
      elif bit[0] == "'":
          yield "'" + bit[1:-1].replace("\\'", "'").replace("\\\\", "\\") + "'"
      else:
          yield bit
