from fastapi import APIRouter, Depends, Query
from psycopg2.extensions import connection

from api.deps import get_db_connection
from dashboard.services.alarm_event_service import (
    get_alarm_events,
    get_alarm_events_hourly,
    get_alarm_events_latest,
    get_alarm_events_hourly_overview,
)
from dashboard.utils.filter_utils import Filters

router = APIRouter(
    prefix="/api/monitoring/alarms",
    tags=["monitoring-alarms"],
)


@router.get("/")
def read_alarm_events(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    conn: connection = Depends(get_db_connection),
):
    return get_alarm_events(conn, limit=limit, offset=offset)

@router.get("/hourly")
def read_alarm_events_hourly(
    limit: int = Query(default=100, ge=1, le=1000),
    conn: connection = Depends(get_db_connection),
):
    return get_alarm_events_hourly(conn, limit=limit)

@router.get("/overview/latest")
def read_alarm_events_latest(
    location_id: int | None = Query(default=None),
    apiary_id: int | None = Query(default=None),
    hive_id: int | None = Query(default=None),
    sensor_id: int | None = Query(default=None),
    time_range: str | None = Query(default="24 Hours"),
    conn: connection = Depends(get_db_connection),
):
    filters = Filters(
        location_id=location_id,
        apiary_id=apiary_id,
        hive_id=hive_id,
        sensor_id=sensor_id,
        time_range=time_range,
    )
    return get_alarm_events_latest(conn, filters=filters)


@router.get("/overview/hourly")
def read_alarm_events_hourly_overview(
    location_id: int | None = Query(default=None),
    apiary_id: int | None = Query(default=None),
    hive_id: int | None = Query(default=None),
    sensor_id: int | None = Query(default=None),
    time_range: str | None = Query(default="24 Hours"),
    conn: connection = Depends(get_db_connection),
):
    filters = Filters(
        location_id=location_id,
        apiary_id=apiary_id,
        hive_id=hive_id,
        sensor_id=sensor_id,
        time_range=time_range,
    )
    return get_alarm_events_hourly_overview(conn, filters=filters)