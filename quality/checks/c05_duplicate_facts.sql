-- name: duplicate_facts
-- dimension: uniqueness
-- table: fact_financials
-- tested: SELECT count(*) FROM fact_financials
SELECT cik, metric, period_start, period_end, count(*) AS n
FROM fact_financials
GROUP BY ALL
HAVING count(*) > 1