CREATE TABLE IF NOT EXISTS ingestion.location (
    location_id SERIAL PRIMARY KEY,
    country_id INT,
    city VARCHAR(50),
    address VARCHAR(255),
    postal_code VARCHAR(20),
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6)
);