from pathlib import Path

import duckdb


def apply_scoring(db: str) -> None:
    con = duckdb.connect(db)
    con.execute(Path("quality/health_score.sql").read_text())
    con.close()


def latest_health(db: str) -> float:
    con = duckdb.connect(db, read_only=True)
    score = con.execute(
        "SELECT health_score FROM dq_health ORDER BY dq_run_id DESC LIMIT 1"
    ).fetchone()[0]
    con.close()
    return score