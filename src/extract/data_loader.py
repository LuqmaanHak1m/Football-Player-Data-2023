import pandas as pd
import os

RAW_DATA_FILE = "../../data/raw/raw_player_data.csv"

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, RAW_DATA_FILE)


def load():
    player_data = pd.read_csv(filename)

    print(player_data.shape)
    print(player_data.head(1))
    
    return player_data

