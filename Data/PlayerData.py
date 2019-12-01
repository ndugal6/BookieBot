import pandas as pd

# this glorious api has documentation here https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/examples.md
from nba_api.stats.static import teams
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import commonplayerinfo


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from pathlib import Path


class TooManyPlayers(Exception): pass


class NoPlayersFound(Exception): pass


DATA_FOLDER = Path(".").resolve()


def main_player_data():
    ad_data = get_playercareerstats('203076')
    sc_data = get_playercareerstats('201939')
    return [ad_data, sc_data]


def make_average(_df: pd.DataFrame):
    _df['STL_AVG'] = _df.apply(lambda x: x['STL'] / x['GP'], axis=1)
    _df['PTS_AVG'] = _df.apply(lambda x: x['PTS'] / x['GP'], axis=1)
    _df['REB_AVG'] = _df.apply(lambda x: x['REB'] / x['GP'], axis=1)
    _df['AST_AVG'] = _df.apply(lambda x: x['AST'] / x['GP'], axis=1)
    # _df['SEASON_ID'] = _df['SEASON_ID'].map(lambda x: int(x.split('-')[0]))

def average_per_min(df: pd.DataFrame):
    average_list = ['STL','PTS','REB','AST', 'BLK','FGM','FGA','FG3A','FG3_PCT','OREB','DREB','TOV', 'FTM', 'FTA', 'FG3M']
    for average in average_list:
        col_name = average + '_AVG'
        df[col_name] = df.apply(lambda x: x[average] / x['MIN'], axis=1)
        df.drop(average, inplace=True, axis=1)


def make_multi_index(name: str, _df: pd.DataFrame):
    _df.set_index('SEASON_ID', inplace=True)
    index_list = _df.T.index.to_list()
    index_a = [name] * len(index_list)
    arrays = [index_a, index_list]
    new_index = pd.MultiIndex.from_arrays(arrays, names=('player', 'stats'))
    return _df.T.set_index(new_index)


def combine_and_clean(_df1: pd.DataFrame, _df2: pd.DataFrame):
    combo = pd.concat([_df1, _df2], axis=0).fillna(0)
    return combo


def get_playercareerstats(player_id: str or int):
    return playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]


def get_all_years_data_for_player(player: pd.DataFrame):
    years = player['SEASON_ID'].to_list()
    playerid = player['PLAYER_ID'][0]
    data = playergamelog.PlayerGameLog(player_id=playerid, season=years.pop()).get_data_frames()[0]
    for year in years:
        data = pd.concat([data, playergamelog.PlayerGameLog(player_id=playerid, season=year).get_data_frames()[0]],
                         axis=0).fillna(0)
    data['GAME_DATE'] = pd.to_datetime(data['GAME_DATE'])
    data.sort_values(by="GAME_DATE", inplace=True)
    return data


def create_save_all_years_data_for_player(player_id: int):
    player_data = get_playercareerstats(player_id)
    all_player_data = get_all_years_data_for_player(player_data)
    file_path = DATA_FOLDER / 'DetailedPlayerStats' / (str(player_id) + '_all_years.csv')
    all_player_data.to_csv(file_path)


def get_playerid_from_name(name: str):
    names = players.find_players_by_full_name(name)
    id = player_id_from_list(names)
    if id is None:
        if name.__contains__(' '):
            regex_name = name.replace(' ','.*')
            return get_playerid_from_name(regex_name)
        else:
            raise NoPlayersFound(f'name provided {name}')
    return id


def player_id_from_list(players: list):
    players = list(filter(lambda x: x['is_active'], players))
    if len(players) == 0: return None
    if len(players) > 1: raise TooManyPlayers
    return players[0]['id']

def current_season_for_all_players_averaged():
    stats = pd.DataFrame();
    for player in players.get_active_players():
        career_stats = playercareerstats.PlayerCareerStats(player['id']).get_data_frames()[0]
        year_stats = career_stats.loc[career_stats['SEASON_ID'] == '2019-20']
        stats = pd.concat([stats, year_stats], axis=0,)
        # curry_season_stats
    file_path = DATA_FOLDER / 'CareerStats/all_players_this_year.csv'
    stats.to_csv(file_path)
    return stats



def main():
    data = main_player_data()
    for d in data: make_average(d)
    ad = make_multi_index('ad', data[0])
    sc = make_multi_index('sc', data[1])
    combined = combine_and_clean(ad, sc)


if __name__ == '__main__':
    # pass
    # id = get_playerid_from_name('steph curry')
    # create_save_all_years_data_for_player(id)
    # curry_game_stats = playergamelog.PlayerGameLog(player_id=201939, season='2018').get_data_frames()[0]
    # average_per_min(curry_game_stats)
    # all_stats = current_season_for_all_players_averaged()
    all_stats = pd.read_csv(DATA_FOLDER / 'CareerStats/all_players_this_year.csv')
    all_stats['name'] = all_stats.apply(lambda x: commonplayerinfo.CommonPlayerInfo(x['PLAYER_ID']).get_data_frames()[0]['DISPLAY_FIRST_LAST'], axis=1)
    all_stats.to_csv(DATA_FOLDER / 'CareerStats/all_players_this_year_named.csv')
    # main()

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
