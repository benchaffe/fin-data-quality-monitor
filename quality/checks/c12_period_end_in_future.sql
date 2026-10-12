-- name: period_end_in_future
-- dimension: validity
-- table: fact_financials
-- tested: SELECT count(*) FROM fact_financials
SELECT *
FROM fact_financials
WHERE period_end > current_date