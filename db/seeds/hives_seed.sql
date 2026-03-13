insert into ingestion.hives (apiary_id, hive_type_id, installation_date)
values
    (1, 1, '2025-05-01'),
    (1, 1, '2025-05-03'),
    (1, 2, '2025-05-10')
on conflict do nothing;