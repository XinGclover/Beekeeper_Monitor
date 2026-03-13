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