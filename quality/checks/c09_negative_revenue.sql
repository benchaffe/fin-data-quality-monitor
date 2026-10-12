-- name: negative_revenue
-- dimension: validity
-- table: fact_financials
-- tolerance: 0.001
-- tested: SELECT count(*) FROM fact_financials WHERE metric = 'revenue'
SELECT *
FROM fact_financials
WHERE metric = 'revenue' AND value < 0