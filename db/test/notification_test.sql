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


BEGIN;
TRUNCATE ingestion.notification;
SELECT COUNT(*) FROM ingestion.notification;
COMMIT;

select
  notification_id,
  user_id,
  event_id,
  title,
  created_at
from ingestion.notification
where user_id = 2
order by created_at desc;


SELECT current_database();

SELECT COUNT(*) 
FROM ingestion.notification;

DELETE FROM ingestion.notification;
DELETE FROM ingestion.alarm_event;
COMMIT;

SELECT *
FROM ingestion.notification;