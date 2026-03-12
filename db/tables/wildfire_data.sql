drop table if exists ingestion.wildfire_data;

create table if not exists ingestion.wildfire_data (
    wildfire_id serial primary key,
    job_id int not null references ingestion.scraping_job(job_id),
    location_id int references ingestion.location(location_id),

    latitude decimal(8,5) not null,
    longitude decimal(8,5) not null,

    brightness decimal(8,2),
    confidence char(1),
    frp decimal(10,2),

    satellite varchar(10),
    instrument varchar(20),
    daynight char(1),

    severity_level_id int references ingestion.severity_level(severity_level_id),
    status varchar(20),

    detected_at timestamp not null,
    fetched_at timestamp not null default current_timestamp,

    constraint uq_wildfire_lat_lon_detected
        unique (latitude, longitude, detected_at)
);