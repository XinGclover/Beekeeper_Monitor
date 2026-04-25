from dashboard.utils.api_client import fetch_json
from dashboard.utils.filter_utils import build_api_params
from dashboard.services.kpi_service import build_sensor_kpis
import pandas as pd


def load_overview_data(filters):
    """
    Load overview data via API endpoints.
    
    Args:
        filters: Filters object with location, apiary, hive, sensor, and time_range
        
    Returns:
        Dictionary with kpis, sensor, weather, wildfire, alarms, and notifications data
    """
    params = build_api_params(filters)
    
    # Fetch all data from API endpoints
    sensor_timeline = fetch_json("/api/monitoring/sensors/overview/timeline", params=params)
    sensor_latest = fetch_json("/api/monitoring/sensors/overview/latest", params=params)
    weather_timeline = fetch_json("/api/monitoring/weather/overview/timeline", params=params)
    wildfire_latest = fetch_json("/api/monitoring/wildfire/overview/latest", params=params)
    wildfire_map = fetch_json("/api/monitoring/wildfire/overview/map", params=params)
    alarm_latest = fetch_json("/api/monitoring/alarms/overview/latest", params=params)
    alarm_hourly = fetch_json("/api/monitoring/alarms/overview/hourly", params=params)
    notification_latest = fetch_json("/api/monitoring/notifications/overview/latest", params=params)
    notification_unread = fetch_json("/api/monitoring/notifications/overview/unread-count", params=params)
    
    # Build KPIs from sensor data
    df_timeline = pd.DataFrame(sensor_timeline) if sensor_timeline else pd.DataFrame()
    df_latest = pd.DataFrame(sensor_latest) if sensor_latest else pd.DataFrame()
    
    return {
        "kpis": build_sensor_kpis(df_timeline, df_latest),
        "sensor": {
            "timeseries": sensor_timeline or [],
            "latest": sensor_latest or []
        },
        "weather": {
            "timeseries": weather_timeline or [],
        },
        "wildfire": {
            "latest": wildfire_latest or [],
            "map_points": wildfire_map or [],
        },
        "alarms": {
            "latest": alarm_latest or [],
            "hourly": alarm_hourly or [],
        },
        "notifications": {
            "latest": notification_latest or [],
            "unread_count": notification_unread.get("unread_count", 0) if notification_unread else 0,
        },
    }




