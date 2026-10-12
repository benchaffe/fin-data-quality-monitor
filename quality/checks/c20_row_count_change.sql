-- name: row_count_change
-- dimension: consistency
-- table: loads
-- tested: SELECT greatest(count(*) - 1, 0) FROM loads
WITH ordered AS (
    SELECT run_id, loaded_at, row_count,
           lag(row_count) OVER (ORDER BY loaded_at) AS prev_count
    FROM loads
)
SELECT run_id, row_count, prev_count,
       abs(row_count - prev_count) * 1.0 / prev_count AS pct_change
FROM ordered
WHERE prev_count IS NOT NULL
  AND loaded_at = (SELECT max(loaded_at) FROM loads)
  AND abs(row_count - prev_count) * 1.0 / prev_count > 0.2