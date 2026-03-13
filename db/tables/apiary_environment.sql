CREATE TABLE IF NOT EXISTS ingestion.apiary_environment (
    env_id SERIAL PRIMARY KEY,
    apiary_id INT NOT NULL UNIQUE REFERENCES ingestion.apiary(apiary_id),
    terrain_type VARCHAR(50),
    vegetation_type VARCHAR(50),
    elevation DECIMAL(7, 2),
    distance_to_forest DECIMAL(7, 2),
    fire_risk_zone VARCHAR(50),
    CONSTRAINT chk_apiary_environment_elevation CHECK (
        elevation IS NULL
        OR elevation >= 0
    ),
    CONSTRAINT chk_apiary_environment_distance_to_forest CHECK (
        distance_to_forest IS NULL
        OR distance_to_forest >= 0
    )
);