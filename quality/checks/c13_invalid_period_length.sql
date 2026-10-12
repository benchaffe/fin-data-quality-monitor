-- name: invalid_period_length
-- dimension: validity
-- table: fact_financials
-- tolerance: 0.02
-- tested: SELECT count(*) FROM fact_financials WHERE metric IN ('revenue', 'net_income', 'operating_income') AND period_start IS NOT NULL
SELECT cik, metric, period_start, period_end,
       date_diff('day', period_start, period_end) AS days
FROM fact_financials
WHERE metric IN ('revenue', 'net_income', 'operating_income')
  AND period_start IS NOT NULL
  AND NOT (
        date_diff('day', period_start, period_end) BETWEEN 80 AND 125
      OR date_diff('day', period_start, period_end) BETWEEN 160 AND 200
      OR date_diff('day', period_start, period_end) BETWEEN 245 AND 290
      OR date_diff('day', period_start, period_end) BETWEEN 350 AND 380
  )