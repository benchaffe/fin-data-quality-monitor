from pathlib import Path
import duckdb
from quality.scoring import apply_scoring

SRC, DEST = "warehouse/warehouse.duckdb", "warehouse/demo.duckdb"
Path(DEST).unlink(missing_ok=True)

con = duckdb.connect(DEST)
con.execute(f"ATTACH '{SRC}' AS src (READ_ONLY)")
for table in ["dim_company", "dim_metric", "fact_financials", "loads", "dq_results", "dq_explanations"]:
    con.execute(f"CREATE TABLE {table} AS SELECT * FROM src.{table}")
con.execute("DETACH src")
con.close()
apply_scoring(DEST)