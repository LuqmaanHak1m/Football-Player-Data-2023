import sqlite3
import pandas as pd

conn = sqlite3.connect("data/football.db")
df = pd.read_sql("SELECT * FROM players_2023 LIMIT 5;", conn)
print(df)
