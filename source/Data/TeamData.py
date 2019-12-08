from pathlib import Path

import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import teamgamelog
# this glorious api has documentation here https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/examples.md
from nba_api.stats.static import teams


class TooManyTeams(Exception): pass


class NoTeamsFound(Exception): pass


DATA_FOLDER = Path(".").resolve()

all_teams = teams.get_teams()


def get_team_meta_data(identifier: str) -> object:
    meta_data = teams.find_team_name_by_id(identifier)
    is_multi_found = False
    if meta_data is None:
        meta_data = teams.find_teams_by_full_name(identifier)
    else:
        return meta_data
    if len(meta_data) == 0:
        meta_data = teams.find_team_by_abbreviation(identifier)
    elif len(meta_data) > 1:
        is_multi_found = True
    else:
        return meta_data[0]
    if len(meta_data) == 0:
        meta_data = teams.find_teams_by_nickname(identifier)
    elif len(meta_data) > 1:
        is_multi_found = True
    else:
        return meta_data[0]
    if len(meta_data) == 0:
        meta_data = teams.find_teams_by_state(identifier)
    elif len(meta_data) > 1:
        is_multi_found = True
    else:
        return meta_data[0]
    if len(meta_data) == 0:
        meta_data = teams.find_teams_by_city(identifier)
    elif len(meta_data) > 1:
        is_multi_found = True
    else:
        return meta_data[0]

    if is_multi_found:
        raise TooManyTeams
    else:
        raise NoTeamsFound


def get_team_game_stats_by_year(team: object, year='2019') -> pd.DataFrame:
    return teamgamelog.TeamGameLog(team['id'], year).get_data_frames()[0]


def get_all_years_data_for_team(team: object) -> pd.DataFrame:
    df = pd.DataFrame()
    for year in range(team['year_founded'], 2020):
        yearly_data = get_team_game_stats_by_year(team, year)
        df = pd.concat([df, yearly_data], axis=0)
    df['GAME_DATE'] = pd.to_datetime(df.loc[:,'GAME_DATE'])
    df.sort_values(by="GAME_DATE", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def get_all_years_data_for_team_id(team_id: int or str) -> pd.DataFrame:
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
    # The first DataFrame of those returned is what we want.
    games = gamefinder.get_data_frames()[0]
    return games


def add_opponent_data(df: pd.DataFrame):
    df['HOME'] = df.apply(lambda x: 0 if '@' in x.loc['MATCHUP'] else 1, axis=1)
    df['OPP'] = df.apply(lambda x: x.loc['MATCHUP'].split(' ')[-1], axis=1)
    df['OPP_ID'] = df.apply(lambda x: team_id_from_abbrev(x.loc['OPP']), axis=1)
    df.astype({'OPP_ID': 'int64'})


def team_id_from_abbrev(abbrev: str, _all_teams=all_teams) -> int:
    matched_team = list(filter(lambda x: x['abbreviation'] == abbrev, _all_teams))
    return 0 if len(matched_team) != 1 else matched_team[0]['id']


def create_save_all_years_data_for_team(team: object) -> None:
    file_path = DATA_FOLDER / 'DetailedTeamStats' / (team['nickname'] + '_all_years.csv')
    if file_path.exists():
        return
    all_years = get_all_years_data_for_team(team)
    add_opponent_data(all_years)
    all_years.to_csv(file_path, index=False)


def load_all_years_data_for_team(team: object) -> pd.DataFrame:
    file_path = DATA_FOLDER / 'DetailedTeamStats' / (team['nickname'] + '_all_years.csv')
    team_data = pd.read_csv(file_path)
    if 'Unnamed: 0' in team_data.columns:
        team_data = pd.read_csv(file_path, index_col=0)
    team_data.reset_index(drop=True, inplace=True)
    return team_data


def save_all_team_data() -> None:
    for team in all_teams:
        create_save_all_years_data_for_team(team)


def teams_matchup_data(team1: object, team2: object) -> pd.DataFrame:
    t1_df = load_all_years_data_for_team(team1)
    return t1_df.loc[t1_df['OPP_ID'] == team2['id']]


if __name__ == '__main__':
    save_all_team_data()
    # pelicans_data = get_team_meta_data('pelicans')
    # create_save_all_years_data_for_team(pelicans_data)
    # pelicans_data = pd.read_csv('/Users/nickdugal/Dev/python3/BookieBot/Data/DetailedTeamStats/Pelicans_all_years.csv', index_col=0)
    # pelicans_data.reset_index(drop=True, inplace=True)
    # add_opponent_data(pelicans_data)
    # pelicans_data.to_csv('/Users/nickdugal/Dev/python3/BookieBot/Data/DetailedTeamStats/Pelicans_all_years_opponent_data.csv', index=False)


def scratch_work():
    pels = get_team_meta_data('pelicans')
    gsw = get_team_meta_data('GSW')
    matchups = teams_matchup_data(pels, gsw)
    home = matchups.loc[matchups.loc[:, 'HOME'] == 1]
    away = matchups.loc[matchups.loc[:, 'HOME'] == 0]
    wins = len(matchups.loc[matchups.loc[:,'WL'] == 'W']['WL'])
    losses = len(matchups.loc[matchups.loc[:,'WL'] == 'L']['WL'])
    win_percent = wins / (wins / losses)
