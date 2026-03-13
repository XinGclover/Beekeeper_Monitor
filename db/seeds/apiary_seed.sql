insert into ingestion.apiary (location_id, amount_units)
values
    (1, 12)
on conflict (location_id) do nothing;