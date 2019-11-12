# this glorious api has documentation here https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/examples.md

from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo

# Find players by full name.
players.find_players_by_full_name('james')

# Find players by first name.
players.find_players_by_first_name('lebron')

# Find players by last name.
players.find_players_by_last_name('^(james|love)$')

# Get all players.
players.get_players()

player_info = commonplayerinfo.CommonPlayerInfo(player_id=2544)
player_info.get_data_frames()