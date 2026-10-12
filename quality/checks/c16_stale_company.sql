-- name: stale_company
-- dimension: timeliness
-- table: dim_company
-- tested: SELECT count(*) FROM dim_company
SELECT c.cik, c.entity_name,
       max(f.period_end) AS latest_period_end,
       date_diff('day', max(f.period_end), current_date) AS days_old
FROM dim_company c
JOIN fact_financials f ON f.cik = c.cik
GROUP BY c.cik, c.entity_name
HAVING date_diff('day', max(f.period_end), current_date) > 400