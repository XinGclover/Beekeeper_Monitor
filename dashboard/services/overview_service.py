from dashboard.services.sensor_service import (
    get_sensor_data_timeline_overview,
    get_latest_sensor_data_overview
)
# from dashboard.services.weather_service import (
#     get_weather_overview_summary,
#     get_weather_overview_timeseries,
# )
# from dashboard.services.alarm_event_service import (
#     get_alarm_events,
#     get_alarm_events_hourly,
#     get_active_alarm_count,
# )
# from dashboard.services.notification_service import (
#     get_latest_notifications_for_overview,
#     get_unread_notification_count_for_overview,
# )
# from dashboard.services.wildfire_service import get_wildfire_risk_summary
# from dashboard.services.location_service import get_location_count
# from dashboard.services.sensor_service import get_sensor_count
from psycopg2.extras import RealDictCursor


def load_overview_data(conn, filters):
    return {
        # "summary": {
        #     "sensor_count": get_sensor_count(conn, filters),
        #     "location_count": get_location_count(conn, filters),
        # },
        # "kpis": {
        #     "avg_temperature": get_avg_temperature(conn, filters),
        #     "avg_humidity": get_avg_humidity(conn, filters),
        #     "active_alarms": get_active_alarm_count(conn, filters),
        #     "wildfire_risk": get_wildfire_risk(conn, filters),
        #     "notifications": get_unread_notification_count(conn, filters),
        # },
        "sensor": {
            "timeseries": get_sensor_data_timeline_overview(conn, filters),
            "latest": get_latest_sensor_data_overview(conn, filters)
        },
        # "weather": {
        #     "summary": get_latest_weather_summary(conn, filters),
        #     "timeseries": get_weather_timeline(conn, filters),
        # },
        # "wildfire": {
        #     "latest": get_latest_wildfire_events(conn, filters),
        #     "map_points": get_wildfire_map_points(conn, filters),
        # },
        # "alarms": {
        #     "latest": get_alarm_events(conn, filters),
        #     "hourly": get_alarm_events_hourly(conn, filters),
        # },
        # "notifications": {
        #     "latest": get_notifications_for_scope(conn, filters),
        #     "unread_count": get_unread_notification_count(conn, filters),
        # },
    }




