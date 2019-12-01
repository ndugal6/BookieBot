import pandas as pd

# this glorious api has documentation here https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/examples.md
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from pathlib import Path


class TooManyTeams(Exception): pass


class NoTeamsFound(Exception): pass


DATA_FOLDER = Path(".").resolve()

all_teams = teams.get_teams()

def get_team_meta_data(identifier: str):
    meta_data = teams.find_team_name_by_id(identifier)
    is_multi_found = False
    if meta_data is None:
        meta_data = teams.find_teams_by_full_name(identifier)
    else: return meta_data
    if len(meta_data) == 0:
        meta_data = teams.find_team_by_abbreviation(identifier)
    elif len(meta_data) > 1: is_multi_found = True
    else: return meta_data[0]
    if len(meta_data) == 0:
        meta_data = teams.find_teams_by_nickname(identifier)
    elif len(meta_data) > 1: is_multi_found = True
    else: return meta_data[0]
    if len(meta_data) == 0:
        meta_data = teams.find_teams_by_state(identifier)
    elif len(meta_data) > 1: is_multi_found = True
    else: return meta_data[0]
    if len(meta_data) == 0:
        meta_data = teams.find_teams_by_city(identifier)
    elif len(meta_data) > 1: is_multi_found = True
    else: return meta_data[0]

    if is_multi_found: raise TooManyTeams
    else: raise NoTeamsFound




def get_team_game_stats_by_year(team: object, year='2019'):
    return teamgamelog.TeamGameLog(team['id'], year).get_data_frames()[0]


def get_all_years_data_for_team(team: object):
    df = pd.DataFrame()
    for year in range(team['year_founded'], 2020):
        yearly_data = get_team_game_stats_by_year(team, year)
        df = pd.concat([df, yearly_data], axis=0)
    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
    df.sort_values(by="GAME_DATE", inplace=True)
    return df

def add_opponent_data(df: pd.DataFrame):
    df['HOME'] = df.apply(lambda x: 0 if '@' in x['MATCHUP'] else 1, axis=1)
    df['OPP'] = df.apply(lambda x: x['MATCHUP'].split(' ')[-1], axis=1)
    df['OPP_ID'] = df.apply(lambda x: team_id_from_abbrev(x['OPP']), axis=1)
    df.astype({'OPP_ID': 'int64'})

def team_id_from_abbrev(abbrev: str):
    matched_team = list(filter(lambda x: x['abbreviation'] == abbrev, all_teams))
    return 0 if len(matched_team) != 1 else matched_team[0]['id']


def create_save_all_years_data_for_team(team: object):
    all_years = get_all_years_data_for_team(team)
    add_opponent_data(all_years)
    file_path = DATA_FOLDER / 'DetailedTeamStats' / (team['nickname'] + '_all_years.csv')
    all_years.to_csv(file_path)


if __name__ == '__main__':

    # pelicans_data = get_team_meta_data('pelicans')
    # create_save_all_years_data_for_team(pelicans_data)
    pelicans_data = pd.read_csv('/Users/nickdugal/Dev/python3/BookieBot/Data/DetailedTeamStats/Pelicans_all_years.csv', index_col=0)
    pelicans_data.reset_index(drop=True, inplace=True)
    add_opponent_data(pelicans_data)
    pelicans_data.to_csv('/Users/nickdugal/Dev/python3/BookieBot/Data/DetailedTeamStats/Pelicans_all_years_opponent_data.csv')