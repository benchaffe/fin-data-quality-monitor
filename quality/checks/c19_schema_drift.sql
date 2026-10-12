-- name: schema_drift
-- dimension: consistency
-- table: fact_financials
-- tested: SELECT count(*) FROM information_schema.columns WHERE table_name = 'fact_financials'
WITH expected(col) AS (
    VALUES ('cik'), ('metric'), ('period_start'), ('period_end'), ('fiscal_year'),
           ('fiscal_period'), ('form'), ('filed_date'), ('accession'), ('value')
),
actual AS (
    SELECT column_name AS col FROM information_schema.columns WHERE table_name = 'fact_financials'
)
SELECT 'missing' AS issue, col FROM (SELECT col FROM expected EXCEPT SELECT col FROM actual)
UNION ALL
SELECT 'unexpected', col FROM (SELECT col FROM actual EXCEPT SELECT col FROM expected)