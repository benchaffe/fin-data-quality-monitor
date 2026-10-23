import duckdb
from pathlib import Path

def _setup(statuses):
    con = duckdb.connect()
    con.execute(
        "CREATE TABLE dq_results (dq_run_id VARCHAR, run_at TIMESTAMP, check_name VARCHAR, dimension VARCHAR, table_name VARCHAR, rows_tested BIGINT, rows_failed BIGINT, status VARCHAR, sample_rows VARCHAR, error VARCHAR)"
    )
    for i, (dim, status) in enumerate(statuses):
        con.execute(
            "INSERT INTO dq_results VALUES ('r1', now(), ?, ?, 'fact_financials', 100, 0, ?, '[]', NULL)",
            [f"c{i}", dim, status],
        )
    con.execute(Path("quality/health_score.sql").read_text())
    return con

def test_all_pass_scores_100():
    con = _setup([("completeness", "pass"), ("validity", "pass")])
    assert con.execute("SELECT health_score FROM dq_health").fetchone()[0] == 100.0

def test_a_failure_lowers_the_score():
    con = _setup([("completeness", "pass"), ("validity", "fail")])
    assert con.execute("SELECT health_score FROM dq_health").fetchone()[0] < 100.0