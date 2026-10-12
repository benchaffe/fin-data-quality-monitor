-- name: orphan_facts_no_company
-- dimension: referential_integrity
-- table: fact_financials
-- tested: SELECT count(*) FROM fact_financials
SELECT f.*
FROM fact_financials f
LEFT JOIN dim_company c ON f.cik = c.cik
WHERE c.cik IS NULL