-- name: stale_load
-- dimension: timeliness
-- table: loads
-- tested: SELECT count(*) FROM loads
SELECT run_id, loaded_at,
       date_diff('day', loaded_at, CAST(now() AS TIMESTAMP)) AS days_old
FROM loads
WHERE loaded_at = (SELECT max(loaded_at) FROM loads)
  AND date_diff('day', loaded_at, CAST(now() AS TIMESTAMP)) > 7