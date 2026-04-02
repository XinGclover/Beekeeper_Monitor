with source as (
        select * from {{ source('ingestion', 'location') }}
  ),
  renamed as (
      select
        {{ adapter.quote("location_id") }},
        {{ adapter.quote("country_id") }},
        {{ adapter.quote("city") }},
        {{ adapter.quote("address") }},
        {{ adapter.quote("postal_code") }},
        {{ adapter.quote("latitude") }},
        {{ adapter.quote("longitude") }}

      from source
  )
  select * from renamed
    