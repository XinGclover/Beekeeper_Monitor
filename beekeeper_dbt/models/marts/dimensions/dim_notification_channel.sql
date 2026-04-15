with channel as (
    select *
    from {{ ref('stg_notification_channel') }}
)

select
    channel_id as channel_key,
    channel_id,
    channel_name
from channel