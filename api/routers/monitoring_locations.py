from fastapi import APIRouter, Depends
from psycopg2.extensions import connection

from api.deps import get_db_connection
from dashboard.services.location_service import get_location_overview

router = APIRouter(
    prefix="/api/monitoring/locations",
    tags=["monitoring-locations"],
)


@router.get("/overview")
def read_location_overview(
    conn: connection = Depends(get_db_connection),
):
    return get_location_overview(conn)