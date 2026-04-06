CREATE TABLE IF NOT EXISTS ingestion.notification_channel (
  channel_id smallint PRIMARY KEY,
  channel_name varchar(20) NOT NULL UNIQUE
);
