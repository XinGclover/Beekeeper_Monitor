insert into ingestion.external_source
(source_name, base_url, data_type, update_frequency)
values
('SMHI Weather API', 'https://opendata.smhi.se', 'weather', 'hourly');