# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2011
from __future__ import division

import os
import hashlib 

from normalize import normalizeName
from text import get_sort_name, findRe

__all__ = ['parse_movie_path', 'create_movie_path', 'get_oxid']

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
    else:
        title = parts[1]
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
    fileparts = parts[-1].split('.')
    extension = fileparts[-1]

    if len(fileparts[-2]) == 2:
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

    if episode:
        episodeTitle = fileparts.index('Episode %d' % episode) + 1
        episodeTitle = fileparts[episodeTitle]
        if episodeTitle == extension or episodeTitle.startswith('Part'):
            episodeTitle = None
    if season:
        seriesTitle = title
        title = u'%s (S%02d)' % (seriesTitle, season)
        if episode:
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
    if not episode:
        oxid = get_hash(director)[:8] + get_hash('\n'.join([title, str(year)]))[:8]
    else:
        oxid = get_hash('\n'.join([director, title, str(year), str(season)]))[:8] + \
               get_hash('\n'.join([str(episode), episode_director, episode_title, str(episode_year)]))[:8]
    return u'0x' + oxid

