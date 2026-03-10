create table if not exists ingestion.scraping_job (
    job_id serial primary key,
    source_id int not null references ingestion.external_source(source_id),
    run_timestamp timestamp not null default current_timestamp,
    status varchar(30),
    records_collected int default 0
);