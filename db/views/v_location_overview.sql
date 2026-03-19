CREATE OR REPLACE VIEW ingestion.v_location_overview AS
WITH latest_weather AS (
    SELECT DISTINCT ON (location_id)
        location_id,
        fetched_at AS weather_time,
        air_temperature,
        wind_speed
    FROM ingestion.weather_data
    ORDER BY location_id, fetched_at DESC
),
latest_wildfire AS (
    SELECT DISTINCT ON (location_id)
        location_id,
        detected_at AS wildfire_time,
        severity_level_id,
        brightness,
        confidence,
        frp,
        status
    FROM ingestion.wildfire_data
    ORDER BY location_id, detected_at DESC
)

SELECT
    l.location_id,
    l.city,
    l.address,
    l.postal_code,
    l.latitude,
    l.longitude,

    -- weather
    w.weather_time,
    w.air_temperature,
    w.wind_speed,

    -- wildfire
    wf.wildfire_time,
    wf.severity_level_id,
    wf.brightness,
    wf.confidence,
    wf.frp,
    wf.status

FROM ingestion.location l

LEFT JOIN latest_weather w
    ON l.location_id = w.location_id

LEFT JOIN latest_wildfire wf
    ON l.location_id = wf.location_id

ORDER BY l.city;