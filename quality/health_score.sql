CREATE OR REPLACE TABLE dq_weights AS
SELECT * FROM (VALUES
    ('completeness', 25),
    ('validity', 20),
    ('uniqueness', 15),
    ('referential_integrity', 15),
    ('consistency', 15),
    ('timeliness', 10)
) AS t(dimension, weight);

CREATE OR REPLACE VIEW dq_dimension_scores AS
SELECT dq_run_id,
       dimension,
       count(*) AS n_checks,
       avg(CASE WHEN status = 'pass' THEN 1.0 ELSE 0.0 END) AS dim_score
FROM dq_results
GROUP BY dq_run_id, dimension;

CREATE OR REPLACE VIEW dq_health AS
SELECT d.dq_run_id,
       round(100 * sum(w.weight * d.dim_score) / sum(w.weight), 1) AS health_score
FROM dq_dimension_scores d
JOIN dq_weights w USING (dimension)
GROUP BY d.dq_run_id;

CREATE OR REPLACE VIEW dq_table_health AS
SELECT dq_run_id,
       table_name,
       round(100 * avg(CASE WHEN status = 'pass' THEN 1.0 ELSE 0.0 END), 1) AS health_score
FROM dq_results
GROUP BY dq_run_id, table_name;