insert into ingestion.severity_level
(severity_level_id, severity_name, description)
values
(1, 'low', 'Low wildfire intensity'),
(2, 'medium', 'Moderate wildfire intensity'),
(3, 'high', 'High wildfire intensity')
on conflict (severity_level_id) do nothing;