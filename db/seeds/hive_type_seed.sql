insert into ingestion.hive_type (name, description)
values
    ('Langstroth', 'Standard modern beehive with removable frames'),
    ('Top-bar', 'Horizontal hive with top bars instead of frames'),
    ('Warre', 'Vertical hive designed to mimic natural bee living conditions')
on conflict (name) do nothing;