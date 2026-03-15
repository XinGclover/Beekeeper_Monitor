INSERT INTO ingestion.alarm_rule_target (rule_id, target_type_id, target_id)
VALUES
    -- Sensor / hive related rules -> APIARY targets
    (1, 2, 1),
    (1, 2, 2),
    (1, 2, 3),
    (1, 2, 4),

    (2, 2, 1),
    (2, 2, 2),
    (2, 2, 3),
    (2, 2, 4),

    (3, 2, 1),
    (3, 2, 2),
    (3, 2, 3),
    (3, 2, 4),

    (4, 2, 1),
    (4, 2, 2),
    (4, 2, 3),
    (4, 2, 4),

    (5, 2, 1),
    (5, 2, 2),
    (5, 2, 3),
    (5, 2, 4),

    (6, 2, 1),
    (6, 2, 2),
    (6, 2, 3),
    (6, 2, 4),

    -- Weather rules -> LOCATION targets
    (7, 1, 1),
    (7, 1, 2),
    (7, 1, 3),
    (7, 1, 4),

    (8, 1, 1),
    (8, 1, 2),
    (8, 1, 3),
    (8, 1, 4),

    (9, 1, 1),
    (9, 1, 2),
    (9, 1, 3),
    (9, 1, 4),

    -- Wildfire rules -> LOCATION targets
    (10, 1, 1),
    (10, 1, 2),
    (10, 1, 3),
    (10, 1, 4),

    (11, 1, 1),
    (11, 1, 2),
    (11, 1, 3),
    (11, 1, 4)
ON CONFLICT DO NOTHING;


INSERT INTO ingestion.alarm_rule_target
(rule_id, target_type_id, target_id)
VALUES
-- sensor 1
(1, 4, 1),
(2, 4, 1),
(3, 4, 1),

-- sensor 2
(1, 4, 2),
(3, 4, 2),
(4, 4, 2),

-- sensor 3
(1, 4, 3),
(5, 4, 3),
(6, 4, 3)
ON CONFLICT DO NOTHING;