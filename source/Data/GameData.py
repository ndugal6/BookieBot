import pandas as pd
from nba_api.stats.endpoints import playbyplayv2


def get_game_stats(game_id: str) -> pd.DataFrame:
    pbp = playbyplayv2.PlayByPlayV2(game_id)
    pbp = pbp.get_data_frames()[0]
    return pbp


if __name__ == '__main__':
    a = get_game_stats('0021701171')
