create table if not exists ingestion.wildfire_data (
    wildfire_id serial primary key,
    job_id int not null
        references ingestion.scraping_job(job_id),
    location_id int not null,
    severity varchar(30),
    status varchar(30),
    detected_at timestamp
);