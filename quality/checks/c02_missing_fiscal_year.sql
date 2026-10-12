-- name: missing_fiscal_year
-- dimension: completeness
-- table: fact_financials
-- tested: SELECT count(*) FROM fact_financials
SELECT *
FROM fact_financials
WHERE fiscal_year IS NULL