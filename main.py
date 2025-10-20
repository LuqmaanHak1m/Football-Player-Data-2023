from src.extract.data_extractor import extract
from src.transform.data_transform import transform
from src.load.data_loader import load_to_sqlite

def run_etl() -> None:
    df_raw = extract()
    df_clean = transform(df_raw)
    load_to_sqlite(df_clean, table_name=f"players_2023")

if __name__ == "__main__":
    run_etl()
