insert into ingestion.apiary_environment (
    apiary_id,
    terrain_type,
    vegetation_type,
    elevation,
    distance_to_forest,
    fire_risk_zone
)
values
    (1, 'Forest edge', 'Mixed forest', 145.50, 0.80, 'Medium')
on conflict (apiary_id) do nothing;