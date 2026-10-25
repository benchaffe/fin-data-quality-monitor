import os
import sys
from pathlib import Path
import duckdb
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))
DB = os.environ.get("DQ_DB", "warehouse/warehouse.duckdb")

def query(sql: str, params=None, db: str = DB) -> pd.DataFrame:
    con = duckdb.connect(db, read_only=True)
    try:
        return con.execute(sql, params or []).df()
    finally:
        con.close()