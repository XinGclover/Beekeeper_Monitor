insert into ingestion.user
(username, email, password_hash, notifications_enabled, last_login_at)
values
(
    'admin',
    'admin@beekeeper.local',
    'admin123',
    true,
    null
),
(
    'beekeeper',
    'beekeeper@beekeeper.local',
    'beekeeper123',
    true,
    null
);


INSERT INTO ingestion."user"
(username, email, password_hash, notifications_enabled)
VALUES
('anna', 'anna@beekeeper.local', 'anna123', TRUE),
('erik', 'erik@beekeeper.local', 'erik123', TRUE),
('lars', 'lars@beekeeper.local', 'lars123', TRUE),
('sofia', 'sofia@beekeeper.local', 'sofia123', TRUE),
('maria', 'maria@beekeeper.local', 'maria123', TRUE);


UPDATE ingestion."user"
SET role_id = CASE
    WHEN username = 'admin' THEN 1
    WHEN username = 'beekeeper' THEN 2
    WHEN username IN ('anna', 'erik', 'lars', 'sofia', 'maria') THEN 2
    ELSE 3
END;