with apiary as (
    select *
    from {{ ref('sn_apiary') }}
),

location as (
    select *
    from {{ ref('stg_location') }}
),

country as (
    select *
    from {{ ref('stg_country') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['apiary_id', 'dbt_valid_from']) }} as apiary_key,
    a.apiary_id,
    a.location_id,
    a.amount_units,
    l.country_id,
    l.city,
    l.address,
    l.postal_code,
    l.latitude,
    l.longitude,
    c.country_name as country,
    a.dbt_valid_from as valid_from,
    a.dbt_valid_to as valid_to,
    case
        when a.dbt_valid_to is null then true
        else false
    end as is_current
from apiary a
left join location l
    on a.location_id = l.location_id
left join country c
    on l.country_id = c.country_id