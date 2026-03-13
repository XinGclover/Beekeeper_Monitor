insert into ingestion.external_source
(source_name, base_url, data_type, update_frequency)
values
('SMHI Weather API', 'https://opendata.smhi.se', 'weather', 'hourly'),
('NASA FIRMS API', 'https://firms.modaps.eosdis.nasa.gov/api/', 'wildfire', 'daily'),
('Hive Sensor Network', null, 'sensor', 'realtime');