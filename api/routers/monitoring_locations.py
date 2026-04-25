from typing import Optional

from fastapi import APIRouter, Depends, Query
from psycopg2.extensions import connection

from api.deps import get_db_connection
from dashboard.services.location_service import get_location_overview, get_filter_options

router = APIRouter(
    prefix="/api/monitoring/locations",
    tags=["monitoring-locations"],
)


@router.get("/overview")
def read_location_overview(
    conn: connection = Depends(get_db_connection),
):
    return get_location_overview(conn)


@router.get("/filter-options")
def read_filter_options(
    location_id: Optional[int] = Query(default=None),
    apiary_id: Optional[int] = Query(default=None),
    hive_id: Optional[int] = Query(default=None),
    conn: connection = Depends(get_db_connection),
):
    """
    Get hierarchical filter options for location, apiary, hive, and sensor.
    
    Returns all available options based on the provided filters.
    """
    return get_filter_options(
        conn,
        location_id=location_id,
        apiary_id=apiary_id,
        hive_id=hive_id,
    )
