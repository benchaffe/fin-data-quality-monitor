import glob
import json
from pathlib import Path
import duckdb
import pandas as pd
from quality.explain import explain_run
from quality.faults.faults import FAULTS

rows = []
for db in sorted(glob.glob("warehouse/faulty_*.duckdb")):
    fault = Path(db).stem.removeprefix("faulty_")
    con = duckdb.connect(db, read_only=True)
    run = con.execute("SELECT max(dq_run_id) FROM dq_results").fetchone()[0]
    con.close()
    expected = FAULTS[fault]["expect"]
    explain_run(db, run, only=expected)
    con = duckdb.connect(db, read_only=True)
    for check, expl in con.execute(
        "SELECT check_name, explanation FROM dq_explanations WHERE dq_run_id = ?", [run]
    ).fetchall():
        e = json.loads(expl)
        rows.append({"fault": fault, "check": check, "summary": e["summary"], "likely_cause": e["likely_cause"], "correct_cause": ""})
    con.close()

pd.DataFrame(rows).to_csv("eval/explanation_review.csv", index=False)
print(f"Wrote {len(rows)} explanations to review")