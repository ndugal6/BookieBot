from pathlib import Path

import pandas as pd
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
# this glorious api has documentation here https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/examples.md
from nba_api.stats.static import teams

from source.Data.TeamData import add_opponent_data


class TooManyPlayers(Exception): pass


class NoPlayersFound(Exception): pass


DATA_FOLDER = Path(".").resolve()
all_teams = teams.get_teams()


def main_player_data() -> pd.DataFrame:
    ad_data = get_playercareerstats('203076')
    sc_data = get_playercareerstats('201939')
    return [ad_data, sc_data]


def make_average(_df: pd.DataFrame) -> None:
    _df['STL_AVG'] = _df.apply(lambda x: x.loc['STL'] / x.loc['GP'], axis=1)
    _df['PTS_AVG'] = _df.apply(lambda x: x.loc['PTS'] / x.loc['GP'], axis=1)
    _df['REB_AVG'] = _df.apply(lambda x: x.loc['REB'] / x.loc['GP'], axis=1)
    _df['AST_AVG'] = _df.apply(lambda x: x.loc['AST'] / x.loc['GP'], axis=1)


def average_per_min(df: pd.DataFrame) -> None:
    average_list = ['STL', 'PTS', 'REB', 'AST', 'BLK', 'FGM', 'FGA', 'FG3A', 'FG3_PCT', 'OREB', 'DREB', 'TOV', 'FTM',
                    'FTA', 'FG3M']
    for average in average_list:
        col_name = average + '_AVG'
        df[col_name] = df.apply(lambda x: x.loc[average] / x.loc['MIN'], axis=1)
        df.drop(average, inplace=True, axis=1)


def make_multi_index(name: str, _df: pd.DataFrame) -> pd.DataFrame:
    _df.set_index('SEASON_ID', inplace=True)
    index_list = _df.T.index.to_list()
    index_a = [name] * len(index_list)
    arrays = [index_a, index_list]
    new_index = pd.MultiIndex.from_arrays(arrays, names=('player', 'stats'))
    return _df.T.set_index(new_index)


def combine_and_clean(_df1: pd.DataFrame, _df2: pd.DataFrame) -> pd.DataFrame:
    combo = pd.concat([_df1, _df2], axis=0).fillna(0)
    return combo


def get_playercareerstats(player_id=201939) -> pd.DataFrame:
    assert isinstance(player_id, (int, str))
    # ! check this workflow for a player that was traded mid season - how're his stats impacted
    return playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]


def get_all_years_data_for_player(player: pd.DataFrame) -> pd.DataFrame:
    player_id = player.loc[:,'PERSON_ID'][0]
    data = pd.DataFrame()
    for year in range(player.FROM_YEAR[0], player.TO_YEAR[0] + 1):
        year = str(year)
        season = year + '-' + str(int(year[-2:]) + 1)
        data = pd.concat([data, playergamelog.PlayerGameLog(player_id=player_id, season=season).get_data_frames()[0]],
                         axis=0).fillna(0)
    data['GAME_DATE'] = pd.to_datetime(data.loc[:,'GAME_DATE'])
    data['NAME'] = player.DISPLAY_FIRST_LAST[0]
    data.sort_values(by="GAME_DATE", inplace=True)
    normalize(data)
    return data


def create_save_all_years_data_for_player(player_id: int or str) -> None:
    player_data = commonplayerinfo.CommonPlayerInfo(player_id).get_data_frames()[0]
    all_player_data = get_all_years_data_for_player(player_data)
    all_player_data.set_index('GAME_ID', drop=True, inplace=True)
    add_opponent_data(all_player_data)
    file_path = DATA_FOLDER / 'DetailedPlayerStats' / (str(player_id) + '_all_years.csv')
    all_player_data.to_csv(file_path)


def get_playerid_from_name(name: str) -> int:
    names = players.find_players_by_full_name(name)
    id = player_id_from_list(names)
    if id is None:
        if name.__contains__(' '):
            regex_name = name.replace(' ', '.*')
            return get_playerid_from_name(regex_name)
        else:
            raise NoPlayersFound(f'name provided {name}')
    return id


def player_id_from_list(players: list) -> int:
    players = list(filter(lambda x: x['is_active'], players))
    if len(players) == 0: return None
    if len(players) > 1: raise TooManyPlayers
    return players[0]['id']


def current_season_for_all_players_averaged() -> pd.DataFrame:
    stats = pd.DataFrame();
    for player in players.get_active_players():
        career_stats = playercareerstats.PlayerCareerStats(player['id']).get_data_frames()[0]
        year_stats = career_stats.loc[career_stats.loc[:,'SEASON_ID'] == '2019-20']
        stats = pd.concat([stats, year_stats], axis=0, )
    file_path = DATA_FOLDER / 'CareerStats/all_players_this_year.csv'
    stats.to_csv(file_path, index=False)
    return stats


def add_player_name(data: pd.DataFrame):
    name = commonplayerinfo.CommonPlayerInfo(data.loc[:, 'PLAYER_ID'][0]).get_data_frames()[0]['DISPLAY_FIRST_LAST']
    data['NAME'] = name


def save_all_players_on_team(team_abr='NOP'):
    assert isinstance(team_abr, str)
    all_players = pd.read_csv(
        DATA_FOLDER / 'CareerStats/all_players_this_year.csv')

    normalize(all_players)

    all_players.reset_index(drop=True, inplace=True)
    team_players = all_players.loc[all_players.TEAM_ABBREVIATION == team_abr]
    for indx, id in enumerate(team_players.PLAYER_ID):
        print('working on #', indx)
        create_save_all_years_data_for_player(id)


def normalize(_df: pd.DataFrame):
    _df.columns = _df.columns.str.upper()


def main():
    save_all_players_on_team('NOP')
    # data = main_player_data()
    # for d in data: make_average(d)
    # ad = make_multi_index('ad', data[0])
    # sc = make_multi_index('sc', data[1])
    # combined = combine_and_clean(ad, sc)


if __name__ == '__main__':
    main()

    # id = get_playerid_from_name('steph curry')
    # create_save_all_years_data_for_player(id)
    # curry_game_stats = playergamelog.PlayerGameLog(player_id=201939, season='2018').get_data_frames()[0]
    # average_per_min(curry_game_stats)
    # all_stats = current_season_for_all_players_averaged()
    #
    # all_stats = pd.read_csv(DATA_FOLDER / 'CareerStats/all_players_this_year.csv')
    # all_stats['name'] = all_stats.apply(
    #     lambda x: commonplayerinfo.CommonPlayerInfo(x['PLAYER_ID']).get_data_frames()[0]['DISPLAY_FIRST_LAST'], axis=1)
    # all_stats.to_csv(DATA_FOLDER / 'CareerStats/all_players_this_year_named.csv')

    # sc_678.plot(x = 'id', y = ['AST'], kind='scatter', color='red', ax=ax)
    # sc_678.plot(x = 'id', y = ['PTS'], kind='scatter', color='blue', ax=ax, legend=True)
    # sc_678.plot(x = 'id', y = 'PTS', z= 'AST', color='blue', ax=ax, legend=True)
    # steph_curry_2018.plot('STL')
    # plt.show()

    # threedee = plt.figure().gca(projection='3d')
    # threedee.scatter(sc_all_years['REB'], sc_all_years['PTS'], sc_all_years['AST'])
    # threedee.set_xlabel('Rebounds')
    # threedee.set_ylabel('Points')
    # threedee.set_zlabel('Assists')
    # plt.show()
