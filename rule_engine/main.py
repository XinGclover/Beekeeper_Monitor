from rule_engine.pipeline.sensor_pipeline import process_sensor_alarms
from rule_engine.pipeline.weather_pipeline import process_weather_alarms
#from rule_engine.pipeline.wildfire_pipeline import process_wildfire_alarms
from db import get_db_conn


def main():
    conn = get_db_conn()
    try:
        #process_sensor_alarms(conn)
        process_weather_alarms(conn)
        #process_wildfire_alarms(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()