-- name: balance_sheet_equation
-- dimension: consistency
-- table: fact_financials
-- tested: SELECT count(*) FROM (SELECT cik, period_end FROM fact_financials WHERE metric IN ('total_assets', 'total_liabilities', 'shareholders_equity') GROUP BY 1, 2 HAVING count(DISTINCT metric) = 3 AND count(DISTINCT accession) = 1)
WITH bs AS (
    SELECT cik, period_end,
           max(value) FILTER (WHERE metric = 'total_assets') AS assets,
           max(value) FILTER (WHERE metric = 'total_liabilities') AS liabilities,
           max(value) FILTER (WHERE metric = 'shareholders_equity') AS equity,
           count(DISTINCT accession) AS n_filings
    FROM fact_financials
    WHERE metric IN ('total_assets', 'total_liabilities', 'shareholders_equity')
    GROUP BY cik, period_end
)
SELECT cik, period_end, assets, liabilities, equity,
       abs(assets - (liabilities + equity)) / nullif(assets, 0) AS rel_gap
FROM bs
WHERE assets IS NOT NULL AND liabilities IS NOT NULL AND equity IS NOT NULL
  AND n_filings = 1
  AND abs(assets - (liabilities + equity)) / nullif(assets, 0) > 0.05