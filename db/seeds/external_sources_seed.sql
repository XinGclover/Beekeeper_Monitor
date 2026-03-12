insert into ingestion.external_source
(source_name, base_url, data_type, update_frequency)
values
('SMHI Weather API', 'https://opendata.smhi.se', 'weather', 'hourly'),;

insert into ingestion.external_source
(source_id, source_name, base_url, data_type, update_frequency)
values
(2, 'NASA FIRMS API', 'https://firms.modaps.eosdis.nasa.gov/api/', 'wildfire', 'daily');