# -*- Mode: Python; -*-
# -*- coding: utf-8 -*-
# vi:si:et:sw=2:sts=2:ts=2


_articles = ('the', 'la', 'a', 'die', 'der', 'le', 'el',
            "l'", 'il', 'das', 'les', 'o', 'ein', 'i', 'un', 'los', 'de',
            'an', 'una', 'las', 'eine', 'den', 'gli', 'het', 'os', 'lo',
            'az', 'det', 'ha-', 'een', 'ang', 'oi', 'ta', 'al-', 'dem',
            'mga', 'uno', "un'", 'ett', u'\xcf', 'eines', u'\xc7', 'els',
            u'\xd4\xef', u'\xcf\xe9')

# Articles in a dictionary.
_articlesDict = dict([(x, x) for x in _articles])
_spArticles = []
for article in _articles:
  if article[-1] not in ("'", '-'): article += ' '
  _spArticles.append(article)

def canonicalTitle(title):
  """Return the title in the canonic format 'Movie Title, The'."""
  try:
      if _articlesDict.has_key(title.split(', ')[-1].lower()): return title
  except IndexError: pass
  ltitle = title.lower()
  for article in _spArticles:
      if ltitle.startswith(article):
          lart = len(article)
          title = '%s, %s' % (title[lart:], title[:lart])
          if article[-1] == ' ': title = title[:-1]
          break
  ## XXX: an attempt using a dictionary lookup.
  ##for artSeparator in (' ', "'", '-'):
  ##    article = _articlesDict.get(ltitle.split(artSeparator)[0])
  ##    if article is not None:
  ##        lart = len(article)
  ##        # check titles like "una", "I'm Mad" and "L'abbacchio".
  ##        if title[lart:] == '' or (artSeparator != ' ' and
  ##                                title[lart:][1] != artSeparator): continue
  ##        title = '%s, %s' % (title[lart:], title[:lart])
  ##        if artSeparator == ' ': title = title[1:]
  ##        break
  return title

def normalizeTitle(title):
  """Return the title in the normal "The Title" format."""
  stitle = title.split(', ')
  if len(stitle) > 1 and _articlesDict.has_key(stitle[-1].lower()):
      sep = ' '
      if stitle[-1][-1] in ("'", '-'): sep = ''
      title = '%s%s%s' % (stitle[-1], sep, ', '.join(stitle[:-1]))
  return title

