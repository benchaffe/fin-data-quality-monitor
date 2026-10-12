-- name: revenue_growth_outlier
-- dimension: validity
-- table: fact_financials
-- tested: SELECT count(*) FROM fact_financials WHERE metric = 'revenue' AND date_diff('day', period_start, period_end) BETWEEN 350 AND 380
WITH annual AS (
    SELECT cik, period_end, value
    FROM fact_financials
    WHERE metric = 'revenue'
      AND date_diff('day', period_start, period_end) BETWEEN 350 AND 380
      AND value > 0
),
growth AS (
    SELECT cik, period_end, value,
           ln(value / lag(value) OVER (PARTITION BY cik ORDER BY period_end)) AS log_growth
    FROM annual
),
scored AS (
    SELECT *,
           avg(log_growth) OVER w AS mu,
           stddev_samp(log_growth) OVER w AS sd
    FROM growth
    WINDOW w AS (PARTITION BY cik ORDER BY period_end ROWS BETWEEN 8 PRECEDING AND 1 PRECEDING)
)
SELECT cik, period_end, value, log_growth, (log_growth - mu) / sd AS z
FROM scored
WHERE sd > 0
  AND abs((log_growth - mu) / sd) > 4
  AND abs(log_growth) > ln(2)