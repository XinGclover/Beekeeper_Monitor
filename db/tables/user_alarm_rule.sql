CREATE TABLE IF NOT EXISTS ingestion.user_alarm_rule (
  user_id INT NOT NULL REFERENCES ingestion.user(user_id),
  rule_id INT NOT NULL REFERENCES ingestion.alarm_rule(rule_id),
  PRIMARY KEY (user_id, rule_id)
);