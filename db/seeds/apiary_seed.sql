INSERT INTO ingestion.apiary (location_id, amount_units)
VALUES
    (1, 12),
    (1, 8),
    (3, 15),
    (4, 6),
    (5, 7)
ON CONFLICT (location_id) DO NOTHING;
