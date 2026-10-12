-- name: filed_before_period_end
-- dimension: consistency
-- table: fact_financials
-- tested: SELECT count(*) FROM fact_financials WHERE filed_date IS NOT NULL
SELECT *
FROM fact_financials
WHERE filed_date IS NOT NULL
  AND filed_date < period_end