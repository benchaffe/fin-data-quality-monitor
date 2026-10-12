import csv
from pathlib import Path

import duckdb

from quality.faults.faults import FAULTS, apply_fault
from quality.run_checks import run_all
from quality.scoring import apply_scoring

BASE = "warehouse/warehouse.duckdb"


def results(db: str, run_id: str):
    con = duckdb.connect(db, read_only=True)
    rows = con.execute(
        "SELECT check_name, rows_failed, status FROM dq_results WHERE dq_run_id = ?", [run_id]
    ).fetchall()
    score = con.execute("SELECT health_score FROM dq_health WHERE dq_run_id = ?", [run_id]).fetchone()[0]
    con.close()
    return {name: (failed, status) for name, failed, status in rows}, score


def main() -> None:
    base_run = run_all(BASE)
    apply_scoring(BASE)
    base, base_score = results(BASE, base_run)
    false_alarms = sum(1 for _, status in base.values() if status != "pass")

    out = []
    for name, spec in FAULTS.items():
        dst = f"warehouse/faulty_{name}.duckdb"
        apply_fault(BASE, dst, name)
        run = run_all(dst)
        apply_scoring(dst)
        res, score = results(dst, run)
        detected = any(res[c][1] == "fail" and res[c][0] > base[c][0] for c in spec["expect"])
        out.append({"fault": name, "detected": detected, "clean_score": base_score, "faulty_score": score})

    Path("eval").mkdir(exist_ok=True)
    with open("eval/fault_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out[0].keys())
        w.writeheader()
        w.writerows(out)

    caught = sum(r["detected"] for r in out)
    print(f"Detected {caught} of {len(out)} faults")
    print(f"Clean score {base_score}; checks not passing on clean data: {false_alarms} of {len(base)}")


if __name__ == "__main__":
    main()