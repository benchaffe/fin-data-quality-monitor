-- name: revenue_unit_jump
-- dimension: validity
-- table: fact_financials
-- tested: SELECT count(*) FROM fact_financials WHERE metric = 'revenue' AND value > 0 AND (date_diff('day', period_start, period_end) BETWEEN 350 AND 380 OR date_diff('day', period_start, period_end) BETWEEN 80 AND 100)
WITH rev AS (
    SELECT cik, period_end, value,
           CASE
               WHEN date_diff('day', period_start, period_end) BETWEEN 350 AND 380 THEN 'annual'
               WHEN date_diff('day', period_start, period_end) BETWEEN 80 AND 100 THEN 'quarter'
           END AS length_bucket
    FROM fact_financials
    WHERE metric = 'revenue' AND value > 0
),
prev AS (
    SELECT *,
           lag(value) OVER (PARTITION BY cik, length_bucket ORDER BY period_end) AS prev_value
    FROM rev
    WHERE length_bucket IS NOT NULL
)
SELECT cik, length_bucket, period_end, value, prev_value, value / prev_value AS ratio
FROM prev
WHERE prev_value IS NOT NULL
  AND (value / prev_value > 100 OR value / prev_value < 0.01)