CREATE TABLE IF NOT EXISTS ingestion.notification (
    notification_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES ingestion.user(user_id),
    event_id INT NOT NULL REFERENCES ingestion.alarm_event(event_id),
    notification_status VARCHAR(20) NOT NULL DEFAULT 'pending',
    is_read BOOLEAN NOT NULL DEFAULT false,
    title VARCHAR(200),
    message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP NULL,
    sent_at TIMESTAMP NULL,
    CONSTRAINT uq_notification_user_event UNIQUE (user_id, event_id),
    CONSTRAINT ck_notification_status CHECK (
        notification_status IN ('pending', 'sent', 'failed')
    )
);

ALTER TABLE
    ingestion.notification
ADD
    COLUMN channel_id SMALLINT;

UPDATE
    ingestion.notification
SET
    channel_id = 1
WHERE
    channel_id IS NULL;

ALTER TABLE
    ingestion.notification
ALTER COLUMN
    channel_id
SET
    NOT NULL;

ALTER TABLE
    ingestion.notification
ADD
    CONSTRAINT fk_notification_channel FOREIGN KEY (channel_id) REFERENCES ingestion.notification_channel(channel_id);