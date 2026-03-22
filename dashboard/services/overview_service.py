from dashboard.services.sensor_service import (
    get_sensor_data_timeline_overview,
    get_latest_sensor_data_overview
)
from dashboard.services.kpi_service import build_sensor_kpis
from dashboard.services.weather_service import get_weather_timeline
from dashboard.services.wildfire_service import (get_latest_wildfire_events, get_wildfire_map_points)
from psycopg2.extras import RealDictCursor
import pandas as pd



def load_overview_data(conn, filters):
    timeline_rows = get_sensor_data_timeline_overview(conn, filters)
    latest_rows = get_latest_sensor_data_overview(conn, filters)

    df_timeline = pd.DataFrame(timeline_rows)
    df_latest = pd.DataFrame(latest_rows)
    return {
        # "summary": {
        #     "sensor_count": get_sensor_count(conn, filters),
        #     "location_count": get_location_count(conn, filters),
        # },
        "kpis": build_sensor_kpis(df_timeline, df_latest),
        "sensor": {
            "timeseries": timeline_rows,
            "latest": latest_rows
        },
        "weather": {
        #     "summary": get_latest_weather_summary(conn, filters),
            "timeseries": get_weather_timeline(conn, filters),
         },
        "wildfire": {
            "latest": get_latest_wildfire_events(conn, filters),
            "map_points": get_wildfire_map_points(conn, filters),
        },
        # "alarms": {
        #     "latest": get_alarm_events(conn, filters),
        #     "hourly": get_alarm_events_hourly(conn, filters),
        # },
        # "notifications": {
        #     "latest": get_notifications_for_scope(conn, filters),
        #     "unread_count": get_unread_notification_count(conn, filters),
        # },
    }




