# Shared filter model and helpers for dashboard pages.

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Filters:
    location_id: int | None = None
    apiary_id: int | None = None
    hive_id: int | None = None
    sensor_id: int | None = None
    time_range: str = "24h"   # "24h" | "7d" | "30d" | "custom"
    start_time: datetime | None = None
    end_time: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "location_id": self.location_id,
            "apiary_id": self.apiary_id,
            "hive_id": self.hive_id,
            "sensor_id": self.sensor_id,
            "time_range": self.time_range,
            "start_time": self.start_time,
            "end_time": self.end_time
        }
    
TIME_RANGE_MAP = {
    "1h": timedelta(hours=1),
    "6h": timedelta(hours=6),
    "24h": timedelta(hours=24),
    "7d": timedelta(days=7),
    "30d": timedelta(days=30),
    "90d": timedelta(days=90),
}

def resolve_time_range(time_range: str):
    end_time = datetime.now()
    delta = TIME_RANGE_MAP.get(time_range, timedelta(hours=24))
    return end_time - delta, end_time


def build_filter_conditions(filters, time_column=None):
    conditions = []
    params = []

    if filters.location_id:
        conditions.append("location_id = %s")
        params.append(filters.location_id)

    if filters.apiary_id:
        conditions.append("apiary_id = %s")
        params.append(filters.apiary_id)

    if filters.hive_id:
        conditions.append("hive_id = %s")
        params.append(filters.hive_id)

    if filters.sensor_id:
        conditions.append("sensor_id = %s")
        params.append(filters.sensor_id)

    # TIME filter flexibel
    if time_column and filters.time_range:
        start_time, end_time = resolve_time_range(filters.time_range)

        conditions.append(f"{time_column} >= %s")
        conditions.append(f"{time_column} <= %s")

        params.extend([start_time, end_time])

    where_sql = ""
    if conditions:
        where_sql = " where " + " and ".join(conditions)

    return where_sql, params


def build_api_params(filters):
    """Build query parameters from Filters object for API calls."""
    params = {}
    if filters.location_id is not None:
        params["location_id"] = filters.location_id
    if filters.apiary_id is not None:
        params["apiary_id"] = filters.apiary_id
    if filters.hive_id is not None:
        params["hive_id"] = filters.hive_id
    if filters.sensor_id is not None:
        params["sensor_id"] = filters.sensor_id
    if filters.time_range:
        params["time_range"] = filters.time_range
    return params