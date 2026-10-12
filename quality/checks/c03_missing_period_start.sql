-- name: missing_period_start
-- dimension: completeness
-- table: fact_financials
-- tolerance: 0.001
-- tested: SELECT count(*) FROM fact_financials WHERE metric IN ('revenue', 'net_income', 'operating_income')
SELECT *
FROM fact_financials
WHERE metric IN ('revenue', 'net_income', 'operating_income') AND period_start IS NULL
