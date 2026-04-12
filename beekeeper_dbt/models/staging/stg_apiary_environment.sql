with source as (
  select * from {{ source('ingestion', 'apiary_environment') }}
),

cleaned as (
  select 
    cast(env_id as integer) as env_id,
    cast(apiary_id as integer) as apiary_id,
    nullif(trim(terrain_type), '') as terrain_type,
    nullif(trim(vegetation_type), '') as vegetation_type,
    cast(elevation as numeric(7,2)) as elevation,
    cast(distance_to_forest as numeric(7,2)) as distance_to_forest,
    nullif(trim(fire_risk_zone), '') as fire_risk_zone
  from source
)

select * from cleaned
