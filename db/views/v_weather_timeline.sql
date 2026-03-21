create or replace view ingestion.v_weather_timeline as
select
    wd.weather_id,
    wd.location_id,
    l.city,
    wd.air_temperature,
    wd.relative_humidity,
    wd.wind_speed,
    wd.wind_direction,
    wd.valid_time,
    wd.fetched_at
from ingestion.weather_data wd
join ingestion.location l
    on wd.location_id = l.location_id;