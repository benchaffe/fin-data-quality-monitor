import shutil

import duckdb

FAULTS = {
    "duplicate_rows": {
        "expect": ["duplicate_facts"],
        "sql": ["INSERT INTO fact_financials SELECT * FROM fact_financials USING SAMPLE 5%"],
    },
    "drop_company_revenue": {
        "expect": ["company_missing_core_metric"],
        "sql": ["DELETE FROM fact_financials WHERE cik = '{cik}' AND metric = 'revenue'"],
    },
    "unit_error_x1000": {
        "expect": ["revenue_unit_jump", "revenue_growth_outlier"],
        "sql": [
            "UPDATE fact_financials SET value = value * 1000 "
            "WHERE cik = '{cik}' AND metric = 'revenue' AND period_end = ("
            "SELECT max(period_end) FROM fact_financials WHERE cik = '{cik}' AND metric = 'revenue')"
        ],
    },
    "stale_company": {
        "expect": ["stale_company"],
        "sql": ["DELETE FROM fact_financials WHERE cik = '{cik}' AND period_end > current_date - INTERVAL 500 DAY"],
    },
    "schema_drift": {
        "expect": ["schema_drift"],
        "sql": ["ALTER TABLE fact_financials ADD COLUMN source_system VARCHAR"],
    },
    "break_balance_sheet": {
        "expect": ["balance_sheet_equation"],
        "sql": ["UPDATE fact_financials SET value = value * 1.5 WHERE cik = '{cik}' AND metric = 'total_assets'"],
    },
}


def target_cik(con) -> str:
    """The company with the most revenue rows, so every fault has something to hit."""
    return con.execute(
        "SELECT cik FROM fact_financials WHERE metric = 'revenue' "
        "GROUP BY cik ORDER BY count(*) DESC LIMIT 1"
    ).fetchone()[0]


def apply_fault(src_db: str, dst_db: str, name: str) -> None:
    shutil.copy(src_db, dst_db)  # never touch the clean warehouse
    con = duckdb.connect(dst_db)
    cik = target_cik(con)
    for stmt in FAULTS[name]["sql"]:
        con.execute(stmt.format(cik=cik))
    con.close()