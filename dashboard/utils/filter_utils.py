# Shared filter model and helpers for dashboard pages.

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Filters:
    location_id: int | None = None
    apiary_id: int | None = None
    hive_id: int | None = None
    sensor_id: int | None = None
    time_range: str = "24 Hours"
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


def get_time_from(filters: Filters | None) -> datetime | None:
    if not filters:
        return None

    time_range = filters.time_range

    now = datetime.now()

    if time_range == "24 Hours":
        return now - timedelta(hours=24)
    if time_range == "7 Days":
        return now - timedelta(days=7)
    if time_range == "30 Days":
        return now - timedelta(days=30)

    return None



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
    if time_column:
        time_from = get_time_from(filters)
        if time_from:
            conditions.append(f"{time_column} >= %s")
            params.append(time_from)

    where_sql = ""
    if conditions:
        where_sql = " where " + " and ".join(conditions)

    return where_sql, params