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