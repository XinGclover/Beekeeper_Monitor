DROP TABLE IF EXISTS ingestion.user;

create table if not exists ingestion.user (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    notifications_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    last_login_at TIMESTAMP NULL
);