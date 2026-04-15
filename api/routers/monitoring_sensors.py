from typing import Optional

from fastapi import APIRouter, Depends, Query
from psycopg2.extensions import connection

from api.deps import get_db_connection
from dashboard.services.sensor_service import (
    get_latest_sensor_data,
    get_sensor_data_timeline,
    get_sensor_history,
)

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