-- name: negative_assets
-- dimension: validity
-- table: fact_financials
-- tolerance: 0.001
-- tested: SELECT count(*) FROM fact_financials WHERE metric = 'total_assets'
SELECT *
FROM fact_financials
WHERE metric = 'total_assets' AND value <= 0