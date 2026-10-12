import json
from datetime import datetime, timezone
from pathlib import Path
import duckdb
import pandas as pd

RAW = Path("data/raw")
DB = "warehouse/warehouse.duckdb"
KEEP = {
    "Revenues",
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "SalesRevenueNet",
    "RevenuesNetOfInterestExpense",
    "NetIncomeLoss",
    "OperatingIncomeLoss",
    "Assets",
    "Liabilities",
    "StockholdersEquity",
    "SalesRevenueGoodsNet",
}

def flatten(path: Path, run_id: str) -> list[dict]:
    d = json.loads(path.read_text())
    out = []
    for tag, body in d["facts"].get("us-gaap", {}).items():
        if tag not in KEEP:
            continue
        for unit, facts in body["units"].items():
            for f in facts:
                out.append({
                    "run_id": run_id,
                    "cik": str(d["cik"]).zfill(10),
                    "entity_name": d["entityName"],
                    "tag": tag,
                    "unit": unit,
                    "period_start": f.get("start"),
                    "period_end": f["end"],
                    "fiscal_year": f.get("fy"),
                    "fiscal_period": f.get("fp"),
                    "form": f.get("form"),
                    "filed_date": f.get("filed"),
                    "accession": f.get("accn"),
                    "value": f["val"],
                })
    return out

def main() -> None:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    rows = []
    for p in sorted(RAW.glob("CIK*.json")):
        rows.extend(flatten(p, run_id))
    df = pd.DataFrame(rows)
    for col in ("period_start", "period_end", "filed_date"):
        df[col] = pd.to_datetime(df[col])

    Path("warehouse").mkdir(exist_ok=True)
    con = duckdb.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS raw_facts AS SELECT * FROM df WHERE 1=0")
    con.execute("INSERT INTO raw_facts SELECT * FROM df")
    con.execute(
        "CREATE TABLE IF NOT EXISTS loads (run_id VARCHAR, loaded_at TIMESTAMP, row_count BIGINT)"
    )
    con.execute("INSERT INTO loads VALUES (?, now(), ?)", [run_id, len(df)])
    print(f"Loaded {len(df):,} rows as run {run_id}")

if __name__ == "__main__":
    main()