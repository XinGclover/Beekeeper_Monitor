CREATE TABLE ingestion.role (
    role_id SMALLINT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255)
);