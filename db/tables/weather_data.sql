drop table if exists ingestion.weather_data;

create table if not exists ingestion.weather_data (
    weather_id serial primary key,
    job_id int not null references ingestion.scraping_job(job_id),
    location_id int not null references ingestion.location(location_id),

    air_temperature decimal(5,2),
    relative_humidity decimal(5,2),
    wind_speed decimal(6,2),
    wind_direction decimal(6,2),

    valid_time timestamp not null,
    fetched_at timestamp not null default current_timestamp,

    constraint uq_weather_location_valid_time
        unique (location_id, valid_time)
);