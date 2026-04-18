from typing import Optional

from fastapi import APIRouter, Depends, Query
from psycopg2.extensions import connection

from api.deps import get_db_connection
from dashboard.services.weather_service import (
    get_weather_data,
    get_weather_timeline,
)
from dashboard.utils.filter_utils import Filters

router = APIRouter(
    prefix="/api/monitoring/weather",
    tags=["monitoring-weather"],
)


@router.get("/")
def read_weather_data(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    conn: connection = Depends(get_db_connection),
):
    return get_weather_data(conn, limit=limit, offset=offset)


# Overview page
@router.get("/overview/timeline")
def read_weather_timeline_overview(
    location_id: Optional[int] = Query(default=None),
    time_range: Optional[str] = Query(default="24 Hours"),
    conn: connection = Depends(get_db_connection),
):
    filters = Filters(
        location_id=location_id,
        time_range=time_range,
    )
    return get_weather_timeline(conn, filters=filters)

