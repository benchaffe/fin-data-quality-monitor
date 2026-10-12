-- name: company_missing_core_metric
-- dimension: completeness
-- table: dim_company
-- tested: SELECT count(*) * 3 FROM dim_company
SELECT c.cik, c.entity_name, m.metric
FROM dim_company c
CROSS JOIN (VALUES ('revenue'), ('net_income'), ('total_assets')) AS m(metric)
LEFT JOIN fact_financials f on f.cik = c.cik AND f.metric = m.metric
WHERE f.cik IS NULL