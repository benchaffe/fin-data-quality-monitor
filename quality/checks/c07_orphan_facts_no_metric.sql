-- name: orphan_facts_no_metric
-- dimension: referential_integrity
-- table: fact_financials
-- tested: SELECT count(*) FROM fact_financials
SELECT f.*
FROM fact_financials f
LEFT JOIN (SELECT DISTINCT metric FROM dim_metric) m ON f.metric = m.metric
WHERE m.metric IS NULL