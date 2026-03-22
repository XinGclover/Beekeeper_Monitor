--admin (1)

-- follows all rules

INSERT INTO ingestion.user_alarm_rule (user_id, rule_id)
SELECT 1, rule_id FROM ingestion.alarm_rule;

-- beekeeper (2)
-- care about hive + weather (rule 1–9)

INSERT INTO ingestion.user_alarm_rule (user_id, rule_id)
SELECT 2, rule_id
FROM ingestion.alarm_rule
WHERE rule_id BETWEEN 1 AND 9;

-- anna (3)

-- only wildfire

INSERT INTO ingestion.user_alarm_rule (user_id, rule_id)
VALUES
    (3, 10),
    (3, 11);

-- andra users (4–7)

-- only hive (sensor)

INSERT INTO ingestion.user_alarm_rule (user_id, rule_id)
SELECT u.user_id, r.rule_id
FROM ingestion."user" u
JOIN ingestion.alarm_rule r
    ON r.metric_type_id IN (1, 2, 6)  -- temp, humidity, weight
WHERE u.user_id IN (4,5,6,7);