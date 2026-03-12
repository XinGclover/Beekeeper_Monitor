create table if not exists ingestion.severity_level (
    severity_level_id smallint primary key,
    severity_name varchar(10) not null,
    description varchar(100)
);