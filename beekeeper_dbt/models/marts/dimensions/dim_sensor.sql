WITH sensor AS (
    SELECT
        *
    FROM
        { { ref('stg_sensor') } }
),
sensor_type AS (
    SELECT
        *
    FROM
        { { ref('stg_sensor_type') } }
),
hive AS (
    SELECT
        *
    FROM
        { { ref('stg_hive') } }
),
hive_type AS (
    SELECT
        *
    FROM
        { { ref('stg_hive_type') } }
),
apiary AS (
    SELECT
        *
    FROM
        { { ref('stg_apiary') } }
),
location AS (
    SELECT
        *
    FROM
        { { ref('stg_location') } }
),
country AS (
    SELECT
        *
    FROM
        { { ref('stg_country') } }
)
SELECT
    row_number() over (order by s.sensor_id) AS sensor_key,
    s.sensor_id,
    st.sensor_type_name AS sensor_type,
    s.is_hive_level,
    s.hive_id,
    ht.hive_type_name AS hive_type,
    a.apiary_id,
    l.location_id,
    l.city,
    c.country_name AS country,
    s.installed_at,
    s.status,
    s.installed_at AS valid_from,
    cast(NULL AS timestamp) AS valid_to,
    TRUE AS current_flag
FROM
    sensor s
    LEFT JOIN sensor_type st ON s.sensor_type_id = st.sensor_type_id
    LEFT JOIN hive h ON s.hive_id = h.hive_id
    LEFT JOIN hive_type ht ON h.hive_type_id = ht.hive_type_id
    LEFT JOIN apiary a ON h.apiary_id = a.apiary_id
    LEFT JOIN location l ON a.location_id = l.location_id
    LEFT JOIN country c ON l.country_id = c.country_id