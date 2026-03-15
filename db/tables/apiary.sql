CREATE TABLE IF NOT EXISTS ingestion.apiary (
    apiary_id SERIAL PRIMARY KEY,
    location_id INT NOT NULL UNIQUE REFERENCES ingestion.location(location_id),
    amount_units INT NOT NULL CHECK (amount_units >= 0)
);