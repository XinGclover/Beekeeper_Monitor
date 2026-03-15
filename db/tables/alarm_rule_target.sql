CREATE TABLE IF NOT EXISTS ingestion.alarm_rule_target (
    rule_id INT NOT NULL REFERENCES ingestion.alarm_rule(rule_id),
    target_type_id INT NOT NULL REFERENCES ingestion.target_type(target_type_id),
    target_id INT NOT NULL,
    PRIMARY KEY (rule_id, target_type_id, target_id)
);