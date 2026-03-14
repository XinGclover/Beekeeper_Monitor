SELECT
    n.notification_id,
    u.username,
    n.title,
    n.message,
    n.created_at,
    n.is_read
FROM ingestion.notification n
JOIN ingestion.user u
ON n.user_id = u.user_id
ORDER BY n.created_at DESC;