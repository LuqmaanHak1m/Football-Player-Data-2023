import sqlite3
from pathlib import Path
import pandas as pd

def load_to_sqlite(df: pd.DataFrame, table_name: str = "players") -> None:
    base_dir = Path(__file__).resolve().parents[2]
    db_path = base_dir / "data" / "clean" / "football.db"

    conn = sqlite3.connect(db_path)

    try:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Loaded {len(df)} records into '{table_name}' table in {db_path}")
    finally:
        conn.close()
