create table if not exists ingestion.external_source (
    source_id serial primary key,
    source_name varchar(100) not null,
    base_url varchar(255),
    data_type varchar(50),
    update_frequency varchar(50)
);