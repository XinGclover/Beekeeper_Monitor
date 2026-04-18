from typing import Optional

from fastapi import APIRouter, Depends, Query
from psycopg2.extensions import connection

from api.deps import get_db_connection
from dashboard.services.notification_service import (
    get_notifications,
    get_all_users,
    get_notifications_latest,
    get_unread_notification_count,
)
from notification.repository import (
    get_notifications_for_user,
    get_unread_notifications_for_user,
    mark_notification_as_read,
)

from dashboard.utils.filter_utils import Filters

router = APIRouter(
    prefix="/api/monitoring/notifications",
    tags=["monitoring-notifications"],
)


@router.get("/")
def read_notifications(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    conn: connection = Depends(get_db_connection),
):
    return get_notifications(conn, limit=limit, offset=offset)

# User list
@router.get("/users")
def read_all_users(
    conn: connection = Depends(get_db_connection),
):
    return get_all_users(conn)


@router.get("/overview/latest")
def read_notifications_latest(
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
    return get_notifications_latest(conn, filters=filters)


@router.get("/overview/unread-count")
def read_unread_notification_count(
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
    return {"unread_count": get_unread_notification_count(conn, filters=filters)}



# User notification
@router.get("/user/{user_id}")
def read_notifications_for_user(
    user_id: int,
    conn: connection = Depends(get_db_connection),
):
    return get_notifications_for_user(conn, user_id)


@router.get("/user/{user_id}/unread")
def read_unread_notifications_for_user(
    user_id: int,
    conn: connection = Depends(get_db_connection),
):
    return get_unread_notifications_for_user(conn, user_id)


# Mark notification readed
@router.post("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    conn: connection = Depends(get_db_connection),
):
    updated = mark_notification_as_read(conn, notification_id)
    return {"updated": updated}