INSERT INTO ingestion.alarm_rule_target (rule_id, target_type_id, target_id)
VALUES

-- ======================
-- SENSOR RULES → HIVE
-- ======================

-- rule 1: temperature high → hive 1
(1, 3, 1),

-- rule 2: temperature low → hive 2
(2, 3, 2),

-- rule 3: humidity high → hive 3
(3, 3, 3),

-- rule 4: weight low → hive 1
(4, 3, 1),

-- rule 5: weight critical → hive 2
(5, 3, 2),

-- rule 6: weight very high → hive 3
(6, 3, 3),

-- ======================
-- WEATHER RULES → LOCATION
-- ======================

-- rule 7: extreme temperature → location 1
(7, 1, 1),

-- rule 8: cold weather → location 3
(8, 1, 3),

-- rule 9: strong wind → location 4
(9, 1, 4),

-- ======================
-- WILDFIRE RULE → LOCATION
-- ======================

-- rule 10: wildfire risk → location 5
(10, 1, 5);



DELETE FROM ingestion.alarm_rule_target
WHERE rule_id IN (1,2,3,4,5,6);


INSERT INTO ingestion.alarm_rule_target (rule_id, target_type_id, target_id)
VALUES
(1, 3, 1),
(2, 3, 1),
(3, 3, 1),
(4, 3, 2),
(5, 3, 2),
(6, 3, 2);