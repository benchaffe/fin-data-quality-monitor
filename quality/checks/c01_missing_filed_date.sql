-- name: missing_filed_date
-- dimension: completeness
-- table: fact_financials
-- tested: SELECT count(*) FROM fact_financials
SELECT *
FROM fact_financials 
WHERE filed_date IS NULL