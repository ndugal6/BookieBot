# this glorious api has documentation here https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/examples.md

from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playercareerstats
import nba_api.stats.endpoints as endpoints
import matplotlib.pyplot as plt
import pandas as pd

def scratchWork():
    # Find players by full name.
    players.find_players_by_full_name('james')

    # Find players by first name.
    players.find_players_by_first_name('Stephen')

    # Find players by last name.
    players.find_players_by_last_name('^(james|love)$')

    # Get all players.
    players.get_players()

    player_info = commonplayerinfo.CommonPlayerInfo(player_id=2544)
    # print(player_info.get_data_frames())
    # print(player_info.common_player_info.get_data_frame().head())
    # lebron_common_info_df = player_info.common_player_info.get_data_frame()
    # lebron_headline_stats_df = player_info.player_headline_stats.get_data_frame()
    # print(lebron_common_info_df.columns)
    # print(lebron_headline_stats_df.head())

    lebron_career_stats = endpoints.playercareerstats.PlayerCareerStats(player_id=2544).get_data_frames()
    steph_curry_career_stats = endpoints.playercareerstats.PlayerCareerStats(player_id=201939).get_data_frames()
    steph_curry_career_stats[0].to_csv('/Users/nickdugal/Dev/python3/BookieBot/Data/CareerStats/steph_curry.csv')
    # for df in lebron_career_stats:
    #     print(df.head())
    # print(lebron_career_stats[0].columns)
    # data_i_want = lebron_career_stats[0]
    # data_i_want.to_csv('/Users/nickdugal/Dev/python3/BookieBot/Data/CareerStats/lebron_james.csv')
    # # data_i_want['REB'].plot()

def runDisMotherFucker():
    # steph = pd.read_csv('/Users/nickdugal/Dev/python3/BookieBot/Data/CareerStats/steph_curry.csv', index_col='SEASON_ID')
    steph = pd.read_csv('/Users/nickdugal/Dev/python3/BookieBot/Data/CareerStats/steph_curry.csv')
    # lebron = pd.read_csv('/Users/nickdugal/Dev/python3/BookieBot/Data/CareerStats/lebron_james.csv', index_col='SEASON_ID')
    # createAverage(steph)
    # createAverage(lebron)
    # steph['PTS_AVG'].plot()
    # lebron['PTS_AVG'].plot()
    # data_i_want['REBOUND_AVG'].plot()
    # data_i_want['STEAL_AVG'].plot()
    # data_i_want['ASSIST_AVG'].plot()
    # plt.legend()
    # plt.show()


def createAverage(data_frame):
    data_frame['PTS_AVG'] = data_frame.apply(lambda row: (row['PTS'] / row['GP']),
                                               axis=1)
    data_frame['REBOUND_AVG'] = data_frame.apply(lambda row: (row['REB'] / row['GP']),
                                                   axis=1)
    data_frame['STEAL_AVG'] = data_frame.apply(lambda row: (row['STL'] / row['GP']),
                                                 axis=1)
    data_frame['ASSIST_AVG'] = data_frame.apply(lambda row: (row['AST'] / row['GP']),
                                                  axis=1)

if __name__ == '__main__':
    # runDisMotherFucker()
    steph = pd.read_csv('/Users/nickdugal/Dev/python3/BookieBot/Data/CareerStats/steph_curry.csv', index_col='SEASON_ID')
    steph2 = steph.T
    years = list(map(lambda x: (x.split('-')[0]), steph2.columns))
    steph2.columns = years
    steph3 = steph2.T
    # scratchWork()

def getYear(year):
    return year.split('-')[0]