import re
from datetime import datetime, timezone
from pathlib import Path
import duckdb

DB = "warehouse/warehouse.duckdb"
CHECKS = Path("quality/checks")

def parse(path: Path):
    text = path.read_text()
    meta = dict(re.findall(r"^-- (\w+): (.*)$", text, flags=re.M))
    sql = "\n".join(line for line in text.splitlines() if not line.startswith("-- "))
    return meta, sql

def run_all(db: str = DB) -> str:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%Sf")
    con = duckdb.connect(db)
    con.execute(
        """CREATE TABLE IF NOT EXISTS dq_results (
        dq_run_id VARCHAR, run_at TIMESTAMP, check_name VARCHAR, dimension VARCHAR,
        table_name VARCHAR, rows_tested BIGINT, rows_failed BIGINT, status VARCHAR,
        sample_rows VARCHAR, error VARCHAR)"""
    )
    for path in sorted(CHECKS.glob("*.sql")):
        meta, sql = parse(path)
        try:
            tested = con.execute(meta["tested"]).fetchone()[0]
            failed_df = con.execute(sql).df()
            failed = len(failed_df)
            sample = failed_df.head(5).to_json(orient="records", date_format="iso")
            error = None
        except Exception as e:
            tested, failed, sample, error = 0, 0, "[]", str(e)
        tolerance = float(meta.get("tolerance", 0))
        within = tested > 0 and failed / tested <= tolerance
        status = "error" if error else ("pass" if failed == 0 or within else "fail")
        con.execute(
            "INSERT INTO dq_results VALUES (?, now(), ?, ?, ?, ?, ?, ?, ?, ?)",
            [run_id, meta["name"], meta["dimension"], meta["table"], tested, failed, status, sample, error],
        )
        print(f"{status:5} {meta['name']}: {failed}/{tested}")
    con.close()
    return run_id

if __name__ == "__main__":
    run_all()