CREATE TABLE IF NOT EXISTS ingestion.hives (
    hive_id SERIAL PRIMARY KEY,
    apiary_id INT NOT NULL REFERENCES ingestion.apiary(apiary_id),
    hive_type_id INT NOT NULL REFERENCES ingestion.hive_type(hive_type_id),
    installation_date DATE
);