insert into ingestion.hives (apiary_id, hive_type_id, installation_date)
values
    (1, 1, '2025-05-01'),
    (1, 1, '2025-05-03'),
    (1, 2, '2025-05-10')
on conflict do nothing;

INSERT INTO ingestion.hives (apiary_id, hive_type_id, installation_date)
VALUES

    -- Apiary 10
    (10, 1, '2025-05-05'),
    (10, 3, '2025-05-08'),

    -- Apiary 11
    (11, 1, '2025-05-02'),
    (11, 1, '2025-05-06'),
    (11, 2, '2025-05-09'),
    (11, 3, '2025-05-12'),

    -- Apiary 12
    (12, 2, '2025-05-04'),
    (12, 3, '2025-05-11')
ON CONFLICT DO NOTHING;