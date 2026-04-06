with source as (
  select * from {{ source('ingestion', 'notification_channel') }}
),

cleaned as (
  select 
    cast(channel_id as integer) as channel_id,
    nullif(trim(channel_name), '') as channel_name
  from source
)

select * from cleaned 