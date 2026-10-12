-- name: missing_annual_periods
-- dimension: timeliness
-- table: fact_financials
-- tested: SELECT count(DISTINCT (cik, period_end)) FROM fact_financials WHERE metric = 'revenue' AND date_diff('day', period_start, period_end) BETWEEN 350 AND 380
WITH annual AS (
    SELECT DISTINCT cik, period_end
    FROM fact_financials
    WHERE metric = 'revenue'
      AND date_diff('day', period_start, period_end) BETWEEN 350 AND 380
),
gaps AS (
    SELECT cik, period_end,
           lag(period_end) OVER (PARTITION BY cik ORDER BY period_end) AS prev_end
    FROM annual
)
SELECT cik, prev_end, period_end, date_diff('day', prev_end, period_end) AS gap_days
FROM gaps
WHERE prev_end IS NOT NULL AND date_diff('day', prev_end, period_end) > 400