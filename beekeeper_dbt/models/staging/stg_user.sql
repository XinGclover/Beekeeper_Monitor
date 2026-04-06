with source as (
  select * from {{ source('ingestion', 'user') }}
),

cleaned as (
  select 
    cast(user_id as integer) as user_id,
    nullif(trim(username), '') as user_name,
    nullif(trim(email), '') as email,
    notifications_enabled,
    cast(last_login_at as timestamp) as last_login_at,
    cast(role_id as integer) as role_id
  from source
)

select * from cleaned 