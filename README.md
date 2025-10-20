# 🧱 Football Player Data ETL Pipeline

### 📊 End-to-End Football Data Processing and Loading to SQLite

This project implements a modular **ETL (Extract, Transform, Load)** pipeline for football player datasets collected from multiple years (2017, 2020, 2023). The pipeline automates reading raw CSV files, cleaning and transforming the data, and loading the final processed dataset into a **SQLite database** for further **machine learning and analysis**.

---

## 📂 Project Structure

```
Football-Player-Data-2023/
 ┣ 📂data
 ┃ ┣ 📂raw/                # Raw CSVs for 2017, 2020, 2023
 ┃ ┣ 📂clean/              # SQLite database (output)
 ┃ ┃ ┗ 📜football.db
 ┣ 📂src
 ┃ ┣ 📂extract/            # Extraction logic (CSV -> DataFrame)
 ┃ ┣ 📂transform/          # Transformation logic (data cleaning)
 ┃ ┣ 📂load/               # Loading logic (DataFrame -> SQLite)
 ┣ 📜main.py               # Main ETL runner
 ┣ 📜read_from_database.py # Utility to read from SQLite
 ┣ 📜data_exploration.ipynb# Jupyter exploration & ML prep
 ┗ 📜README.md             # You're here!
```

---

## ⚙️ ETL Pipeline Overview

The ETL pipeline is modularized across three main steps:

### 1. **Extract**
**File:** `src/extract/data_extractor.py`  
Reads raw player CSV files for a specific year from `data/raw/`.

```python
from pathlib import Path
import pandas as pd

def extract(year: int = 2023) -> pd.DataFrame:
    base_dir = Path(__file__).resolve().parents[2]
    file_path = base_dir / "data" / "raw" / f"raw_player_data_{year}.csv"
    df = pd.read_csv(file_path)
    print(f"✅ Extracted {len(df)} records from {file_path.name}")
    return df
```

---

### 2. **Transform**
**File:** `src/transform/data_transform.py`  
Performs column normalization, data cleaning, and consistency checks.

```python
import pandas as pd

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df = df.dropna(subset=["name"])
    print(f"✅ Transformed dataset shape: {df.shape}")
    return df
```

---

### 3. **Load**
**File:** `src/load/data_loader.py`  
Loads the cleaned data into a **SQLite** database stored in `data/clean/football.db`.

```python
import sqlite3
from pathlib import Path

def load_to_sqlite(df, table_name="players_2023"):
    base_dir = Path(__file__).resolve().parents[2]
    db_path = base_dir / "data" / "clean" / "football.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"✅ Loaded {len(df)} records into {table_name} ({db_path})")
```

---

## 🚀 Running the ETL Pipeline

Simply run:

```bash
python main.py
```

The pipeline will:
1. Extract 2023 data from `data/raw/raw_player_data_2023.csv`
2. Clean and transform it
3. Load it into the SQLite database at `data/clean/football.db`  
   (creates it automatically if it doesn’t exist)

---

## 🧠 Future Expansion

You can extend the pipeline to include multiple datasets for time-based ML analysis:

```python
def run_all_years():
    for year in [2017, 2020, 2023]:
        df_raw = extract(year)
        df_clean = transform(df_raw)
        load_to_sqlite(df_clean, table_name=f"players_{year}")
```

This will store each dataset in its own table:
- `players_2017`
- `players_2020`
- `players_2023`

---

## 🧾 Viewing the Database

You can inspect your database using **[DB Browser for SQLite](https://sqlitebrowser.org/)**.

Here’s an example view of the loaded 2023 data:

![Screenshot: DB Browser showing `players_2023` table](screenshots/dbBrowser.png)
```
data/clean/football.db
└── Table: players_2023
      ├── uid
      ├── name
      ├── club
      ├── nat
      ├── age
      ├── position
      └── ...
```

---

## 📈 Next Steps: Machine Learning & Analytics

Once all yearly datasets are loaded into SQLite:
- You can query them directly using `pandas.read_sql()`:
  ```python
  import sqlite3, pandas as pd
  conn = sqlite3.connect("data/clean/football.db")
  df = pd.read_sql("SELECT * FROM players_2023", conn)
  ```
- Combine datasets to build ML models for:
  - Player performance prediction
  - Career trajectory analysis
  - Feature correlation and scouting insights

---

## 🧰 Requirements

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

Recommended libraries:
```
pandas
sqlite3
pathlib
```

---

## 🧑‍💻 Author
**Your Name**  
Data Engineer & Football Analytics Enthusiast ⚽  
📧 *[your.email@example.com]*

---

## 📜 License
This project is licensed under the **MIT License**.  
See [LICENSE](LICENSE) for details.
