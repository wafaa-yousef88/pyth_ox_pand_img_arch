# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2012

from __future__ import division

import hashlib 
import os
import re

from normalize import normalizeName
from text import get_sort_name, findRe

__all__ = ['parse_movie_path', 'create_movie_path', 'get_oxid']

def format_path(data):
    def format_underscores(string):
        return re.sub('^\.|\.$|/|:', '_', string)
    director_sort = data['series_director_sort' if data['is_episode'] else 'director_sort']
    title = data['series_title' if data['is_episode'] else 'title']
    year = data['series_year' if data['is_episode'] else 'year']
    return '/'.join(map(format_underscores, [
        data['directory'],
        '; '.join(director_sort),
        '%s%s' % (title, ' (%s)' % year if year else ''),
        '%s%s%s%s%s%s' % (
            data['title'],
            '.%s' % data['version'] if data['version'] else '',
            '.Part %s' % data['part'] if data['part'] else '',
            '.%s' % data['part_title'] if data['part_title'] else '',
            '.%s' % data['language'].replace('/', '.') if data['language'] else '',
            '.%s' % data['extension']
        )
    ]))

def parse_path(path):
    def parse_series(string):
        match = re.search(' \((S\d{2})?(E\d{2}([+-]\d{2})?)?\)(.+)?', string)
        season = int(match.group(1)[1:]) if match and match.group(1) else None
        episode = int(match.group(2)[1:3]) if match and match.group(2) else None
        episode_title = match.group(4)[1:] if match and match.group(4) else None
        return season, episode, episode_title
    def parse_title(string):
        match = re.search(' \(\d{4}(-\d{4})?\)$', string)
        year = match.group(0)[2:-1] if match else None
        title = string[:-len(match.group(0))] if match else string
        return title, year
    def parse_type(string):
        if string in ['aac', 'm4a', 'mp3', 'ogg']:
            type = 'audio'
        elif string in ['idx', 'srt', 'sub']:
            type = 'subtitle'
        elif string in ['avi', 'm4v', 'mkv', 'mov', 'mpg', 'ogv']:
            type = 'video'
        else:
            type = None
        return type
    def parse_underscores(string):
        string = re.sub('^_', '.', string)
        string = re.sub('_$', '.', string)
        string = re.sub('(?=\w)_(?=\w)', '/', string)
        string = re.sub(' _ ', ' / ', string)
        string = re.sub('(?=\w)_ ', ': ', string)
        return string
    data = {}
    parts = map(parse_underscores, path.split('/'))
    # directory
    data['directory'] = parts[0]
    # director_sort
    data['director_sort'] = filter(
        lambda x: x != 'Unknown Director',
        parts[1].split('; ')
    )
    # director
    data['director'] = map(
        lambda x: ' '.join(reversed(x.split(', '))),
        data['director_sort']
    )
    # title, year
    data['title'], data['year'] = parse_title(parts[2])
    parts = re.split('\.(?! )', parts[3])
    # season, episode, episode_title
    data['season'], data['episode'], data['episode_title'] = parse_series(parts.pop(0))
    if data['season'] or data['episode']:
        data['is_episode'] = True
        data['series_director'] = data['director']
        data['director'] = None
        data['series_director_sort'] = data['director_sort']
        data['director_sort'] = None
        data['series_title'] = data['title']
        data['title'] = '%s (%s%s)%s' % (
            data['title'],
            'S%02d' % data['season'] if data['season'] else '',
            'E%02d' % data['episode'] if data['episode'] else '',
            ' %s' % data['episode_title'] if data['episode_title'] else ''
        )
        data['series_year'] = data['year']
        data['year'] = None
    else:
        data['is_episode'] = False
        data['series_director'] = None
        data['series_director_sort'] = None
        data['series_title'] = None
        data['series_year'] = None
    # version
    data['version'] = parts.pop(0) if re.search('^[A-Z0-9]', parts[0]) and not re.search('^Part ', parts[0]) else None        
    # part
    data['part'] = parts.pop(0)[5:] if re.search('^Part ', parts[0]) else None
    # part_title
    data['part_title'] = parts.pop(0) if re.search('^[A-Z0-9]', parts[0]) else None
    # language
    data['language'] = None
    while re.search('^[a-z]{2}$', parts[0]):
        data['language'] = parts.pop(0) if not data['language'] else '%s/%s' % (
            data['language'], parts.pop(0)
        )
    # extension
    data['extension'] = parts.pop()
    # type
    data['type'] = parse_type(data['extension'])
    if data['type'] == 'subtitle' and not data['language']:
        data['language'] = 'en'
    # _unknown
    data['_unknown'] = '.'.join(parts) if len(parts) else None
    return data


def parse_movie_path(path):
    """
        "A/Abrams, J.J.; Lieber, Jeffrey; Lindelof, Damon/Lost (2004)/Lost.Season 3.Episode 21.Greatest Hits.avi"
        "B/Balada, Ivan/Metrum (1967)/Metrum.Part 1.en.srt"
        "N/Nakata, Hideo/L - Change the World (2008)/L - Change the World.Part 2.srt"
        "R/Reitz, Edgar/Heimat (1984-2006)/Heimat.Season 2.Episode 8.The Wedding.Part 2.avi"
        "F/Feuillade, Louis/Les vampires (1915)/Les vampires.Episode 10.Part 2.avi"
            title: 'Les vampires', year: '1915', episode: 10, part: 2

        "G/Godard, Jean-Luc/Histoire(s) du cinema_ Toutes les histoires (1988)/Histoire(s) du cinema_ Toutes les histoires.avi"
        "G/Godard, Jean-Luc/Six fois deux (1976)/Six fois deux.Part 1A.Y a personne.avi"
        "G/Godard, Jean-Luc; Miéville, Anne-Marie/France_tour_detour_deux_enfants (1977)/France_tour_detour_deux_enfants.Part 5.Impression_Dictée.avi"

        "L/Labarthe, André S_/Cinéastes de notre temps (1964-)/Cinéastes de notre temps.Episode.Jean Renoir le patron, première partie_ La Recherche du relatif.avi"
        "S/Scott, Ridley/Blade Runner (1982)/Blade Runner.Directors's Cut.avi"

        or
        
        T/Title (Year)/Title.avi
    """
    episodeTitle = episodeYear = seriesTitle = None
    episodeDirector = []
    parts = path.split('/')

    #title/year
    if len(parts) == 4:
        title = parts[2]
    elif len(parts) > 1:
        title = parts[1]
    else:
        title = parts[0]
    title = title.replace('_ ', ': ')
    if title.endswith('_'):
        title = title[:-1] + '.'

    year = findRe(title, '(\(\d{4}\))')
    if not year:
        year = findRe(title, '(\(\d{4}-\d*\))')
    if year and title.endswith(year):
        title = title[:-len(year)].strip()
        year = year[1:-1]
        if '-' in year:
            year = findRe(year, '\d{4}')

    #director
    if len(parts) == 4:
        director = parts[1]
        if director.endswith('_'):
            director = "%s." % director[:-1]
        director = director.split('; ')
        director = [normalizeName(d).strip() for d in director]
        director = filter(lambda d: d not in ('Unknown Director', 'Various Directors'), director)
    else:
        director = []

    #extension/language
    fileparts = [x.replace('||', '. ') for x in parts[-1].replace('. ', '||').split('.')]
    extension = len(fileparts) > 1 and fileparts[-1] or ''

    if len(fileparts) > 1 and len(fileparts[-2]) == 2:
        language = fileparts[-2]
    else:
        language = ''
    
    #season/episode/episodeTitle
    season = findRe(parts[-1], '\.Season (\d+)\.')
    if season:
        season = int(season)
    else:
        season = None

    episode = findRe(parts[-1], '\.Episode (\d+)\.')
    if episode:
        episode = int(episode)
    else:
        episode = None

    if episode and 'Episode %d'%episode in fileparts:
        episodeTitle = fileparts.index('Episode %d' % episode) + 1
        episodeTitle = fileparts[episodeTitle]
        if episodeTitle == extension or episodeTitle.startswith('Part'):
            episodeTitle = None

    if not season and 'Episode' in fileparts:
        episodeTitle = fileparts.index('Episode') + 1
        episodeTitle = fileparts[episodeTitle]
        if episodeTitle == extension or episodeTitle.startswith('Part'):
            episodeTitle = None
        else:
            season = 1

    if season:
        seriesTitle = title
        title = u'%s (S%02d)' % (seriesTitle, season)
        if isinstance(episode, int):
            title = u'%s (S%02dE%02d)' % (seriesTitle, season, episode)
        if episodeTitle:
            title = u'%s %s' % (title, episodeTitle)

    #part
    part = findRe(parts[-1], '\.Part (\d+)\.')
    if part:
        part = int(part)
    else:
        part = 0

    return {
        'director': director,
        'episodeDirector': episodeDirector,
        'episode': episode,
        'episodeTitle': episodeTitle,
        'episodeYear': episodeYear,
        'extension': extension,
        'language': language,
        'part': part,
        'season': season,
        'seriesTitle': seriesTitle,
        'title': title,
        'year': year,
    }

def create_movie_path(title, director, year,
                      season, episode, episodeTitle, episodeDirector, episodeYear,
                      part, language, extension):
    '''
    {
            title: '', director: [''], year: '',
                    season: int, episode: int, episodeTitle: '', episodeDirector: [''], episodeYear: '',
                            part: int, language: '', extension: '', extra: bool
                                })
    '''
    partTitle = None
    director = '; '.join(map(get_sort_name, director))
    episodeDirector = '; '.join(map(get_sort_name, episodeDirector))
    filename = [title]
    if season:
        filename += ['Season %d' % season]
    if episode:
        filename += ['Episode %d' % episode]
    if episodeTitle:
        filename += [episodeTitle]
    if part:
        filename += ['Part %s' % part]
    if partTitle:
        filename += [partTitle]
    if extension:
        filename += [extension]
    filename = '.'.join(filename)
    path = os.path.join(director[0], director, '%s (%s)' % (title, year), filename)
    return path

def get_oxid(title, director=[], year='',
             season='', episode='', episode_title='', episode_director=[], episode_year=''):
    def get_hash(string):
        return hashlib.sha1(string.encode('utf-8')).hexdigest().upper()
    director = ', '.join(director)
    episode_director = ', '.join(episode_director)
    if not episode and not episode_title:
        oxid = get_hash(director)[:8] + get_hash('\n'.join([title, str(year)]))[:8]
    else:
        oxid = get_hash('\n'.join([director, title, str(year), str(season)]))[:8] + \
               get_hash('\n'.join([str(episode), episode_director, episode_title, str(episode_year)]))[:8]
    return u'0x' + oxid
