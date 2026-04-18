from typing import Optional

from fastapi import APIRouter, Depends, Query
from psycopg2.extensions import connection

from api.deps import get_db_connection
from dashboard.services.wildfire_service import (
    get_wildfire_data,
    get_wildfire_map_points,
    get_latest_wildfire_events,
)
from dashboard.utils.filter_utils import Filters

router = APIRouter(
    prefix="/api/monitoring/wildfire",
    tags=["monitoring-wildfire"],
)


@router.get("/")
def read_wildfire_data(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    conn: connection = Depends(get_db_connection),
):
    return get_wildfire_data(conn, limit=limit, offset=offset)


@router.get("/map")
def read_wildfire_map_points(
    location_id: Optional[int] = Query(default=None),
    time_range: Optional[str] = Query(default="24 Hours"),
    conn: connection = Depends(get_db_connection),
):
    filters = Filters(
        location_id=location_id,
        time_range=time_range,
    )
    return get_wildfire_map_points(conn, filters=filters)


@router.get("/latest")
def read_latest_wildfire_events(
    location_id: Optional[int] = Query(default=None),
    time_range: Optional[str] = Query(default="24 Hours"),
    conn: connection = Depends(get_db_connection),
):
    filters = Filters(
        location_id=location_id,
        time_range=time_range,
    )
    return get_latest_wildfire_events(conn, filters=filters)