with dates as (

    select generate_series(
        date '2026-01-01',
        date '2035-12-31',
        interval '1 day'
    )::date as date_day

)

select

    to_char(date_day, 'YYYYMMDD')::int as date_key,
    date_day as full_date,

    extract(year from date_day) as year,
    extract(quarter from date_day) as quarter,
    extract(month from date_day) as month,
    to_char(date_day, 'Month') as month_name,

    extract(day from date_day) as day,
    extract(dow from date_day) as day_of_week,
    to_char(date_day, 'Day') as day_name,

    extract(week from date_day) as week_of_year,

    case
        when extract(dow from date_day) in (0,6)
        then true
        else false
    end as is_weekend

from dates