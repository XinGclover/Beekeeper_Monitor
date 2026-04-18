from typing import Optional

from fastapi import APIRouter, Depends, Query
from psycopg2.extensions import connection

from api.deps import get_db_connection
from dashboard.services.sensor_service import (
    get_latest_sensor_data,
    get_sensor_data_timeline,
    get_sensor_history,
    get_sensor_data_timeline_overview,
    get_latest_sensor_data_overview
)
from dashboard.utils.filter_utils import Filters

router = APIRouter(prefix="/api/monitoring/sensors", tags=["monitoring-sensors"])


@router.get("/latest")
def read_latest_sensor_data(
    conn: connection = Depends(get_db_connection),
):
    return get_latest_sensor_data(conn)


@router.get("/timeline")
def read_sensor_timeline(
    sensor_id: Optional[int] = Query(default=None),
    conn: connection = Depends(get_db_connection),
):
    return get_sensor_data_timeline(conn, sensor_id=sensor_id)


@router.get("/history")
def read_sensor_history(
    sensor_id: Optional[int] = Query(default=None),
    conn: connection = Depends(get_db_connection),
):
    return get_sensor_history(conn, sensor_id=sensor_id)


# Overview page
@router.get("/overview/timeline")
def read_sensor_timeline_overview(
    location_id: Optional[int] = Query(default=None),
    apiary_id: Optional[int] = Query(default=None),
    hive_id: Optional[int] = Query(default=None),
    sensor_id: Optional[int] = Query(default=None),
    time_range: Optional[str] = Query(default="24 Hours"),
    conn: connection = Depends(get_db_connection),
):
    filters = Filters(
        location_id=location_id,
        apiary_id=apiary_id,
        hive_id=hive_id,
        sensor_id=sensor_id,
        time_range=time_range,
    )
    return get_sensor_data_timeline_overview(conn, filters=filters)


@router.get("/overview/latest")
def read_latest_sensor_data_overview(
    location_id: Optional[int] = Query(default=None),
    apiary_id: Optional[int] = Query(default=None),
    hive_id: Optional[int] = Query(default=None),
    sensor_id: Optional[int] = Query(default=None),
    time_range: Optional[str] = Query(default="24 Hours"),
    conn: connection = Depends(get_db_connection),
):
    filters = Filters(
        location_id=location_id,
        apiary_id=apiary_id,
        hive_id=hive_id,
        sensor_id=sensor_id,
        time_range=time_range,
    )
    return get_latest_sensor_data_overview(conn, filters=filters)
