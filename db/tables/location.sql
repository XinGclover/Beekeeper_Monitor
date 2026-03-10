create table if not exists ingestion.location (
    location_id serial primary key,
    country_id int,
    city varchar(50),
    address varchar(255),
    postal_code varchar(20),
    latitude decimal(9,6),
    longitude decimal(9,6)
);