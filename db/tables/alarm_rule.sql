CREATE TABLE IF NOT EXISTS ingestion.alarm_rule (
    rule_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    metric_type_id INT NOT NULL REFERENCES ingestion.metric_type(metric_type_id),
    condition_type VARCHAR(10) NOT NULL,
    threshold DECIMAL(11, 5) NOT NULL,
    severity_level_id INT REFERENCES ingestion.severity_level(severity_level_id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

ALTER TABLE ingestion.alarm_rule
RENAME COLUMN name TO rule_name;