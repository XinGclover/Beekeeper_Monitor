with source as (
  select * from {{ source('ingestion', 'notification') }}
),

cleaned as (
  select 
    cast(notification_id as integer) as notification_id,
    cast(user_id as integer) as user_id,
    cast(event_id as integer) as event_id,
    notification_status,
    is_read,
    nullif(trim(title), '') as title,
    nullif(trim(message), '') as message,
    cast(created_at as timestamp) as created_at,
    cast(read_at as timestamp) as read_at,
    cast(sent_at as timestamp) as sent_at,
    cast(channel_id as integer) as channel_id
  from source
)

select * from cleaned  