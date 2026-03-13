from psycopg2.extras import RealDictCursor

# ---------- source data ----------
def fetch_sensor_data(conn):
    sql = """
        SELECT sensor_data_id, sensor_id, measurement, measured_at
        FROM ingestion.sensor_data
        ORDER BY measured_at
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()
    

def fetch_weather_data(conn):
    sql = """
        SELECT weather_id, location_id, air_temperature, relative_humidity, wind_speed
        FROM ingestion.weather_data
        ORDER BY fetched_at
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()

def fetch_wildfire_data(conn):
    sql = """
        SELECT wildfire_id, location_id, brightness, frp, severity_level_id
        FROM ingestion.wildfire_data
        ORDER BY fetched_at
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()

# ---------- alarm rules ----------
def fetch_sensor_rules(conn):
    sql = """
        SELECT
            ar.rule_id,
            ar.name,
            ar.condition_type,
            ar.threshold,
            art.target_id AS sensor_id
        FROM ingestion.alarm_rule ar
        JOIN ingestion.alarm_rule_target art
          ON ar.rule_id = art.rule_id
        JOIN ingestion.target_type tt
          ON art.target_type_id = tt.target_type_id
        WHERE tt.target_type_name = 'sensor'
          AND ar.is_active = TRUE
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()

def fetch_weather_rules(conn):
    sql = """
        SELECT
            ar.rule_id,
            ar.name,
            ar.condition_type,
            ar.threshold,
            art.target_id AS location_id,
            mt.metric_type_name
        FROM ingestion.alarm_rule ar
        JOIN ingestion.alarm_rule_target art
          ON ar.rule_id = art.rule_id
        JOIN ingestion.target_type tt
          ON art.target_type_id = tt.target_type_id
        JOIN ingestion.metric_type mt
          ON ar.metric_type_id = mt.metric_type_id
        WHERE tt.target_type_name = 'location'
          AND mt.metric_type_name IN (
              'weather_temperature',
              'weather_wind_speed'
          )
          AND ar.is_active = TRUE
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()


def fetch_wildfire_rules(conn):
    sql = """
        SELECT
            ar.rule_id,
            ar.name,
            ar.condition_type,
            ar.threshold,
            art.target_id AS location_id,
            mt.metric_type_name
        FROM ingestion.alarm_rule ar
        JOIN ingestion.alarm_rule_target art
          ON ar.rule_id = art.rule_id
        JOIN ingestion.target_type tt
          ON art.target_type_id = tt.target_type_id
        JOIN ingestion.metric_type mt
          ON ar.metric_type_id = mt.metric_type_id
        WHERE tt.target_type_name = 'location'
          AND mt.metric_type_name = 'wildfire_severity'
          AND ar.is_active = TRUE
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()
    

# ---------- alarm events ----------
def insert_sensor_alarm_event(conn, rule_id: int, sensor_data_id: int):
    sql = """
        INSERT INTO ingestion.alarm_event (rule_id, sensor_data_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """
    with conn.cursor() as cur:
        cur.execute(sql, (rule_id, sensor_data_id))

def insert_weather_alarm_event(conn, rule_id: int, weather_id: int):
    sql = """
        INSERT INTO ingestion.alarm_event (rule_id, weather_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """
    with conn.cursor() as cur:
        cur.execute(sql, (rule_id, weather_id))


def insert_wildfire_alarm_event(conn, rule_id: int, wildfire_id: int):
    sql = """
        INSERT INTO ingestion.alarm_event (rule_id, wildfire_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """
    with conn.cursor() as cur:
        cur.execute(sql, (rule_id, wildfire_id))