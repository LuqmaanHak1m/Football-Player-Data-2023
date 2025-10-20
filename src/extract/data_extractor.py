import pandas as pd
import os

RAW_DATA_FILE = "../../data/raw/raw_player_data_2023.csv"

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, RAW_DATA_FILE)



def extract() -> pd.DataFrame:
    player_data = pd.read_csv(filename)

    print(player_data.shape)
    print(player_data.head(1))
    
    return player_data

