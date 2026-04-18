from fastapi import APIRouter, Depends
from pydantic import BaseModel
from psycopg2.extensions import connection

from api.deps import get_db_connection
from dashboard.services.rule_management_service import (
    fetch_alarm_rules,
    update_alarm_rule,
)

router = APIRouter(
    prefix="/api/monitoring/alarm-rules",
    tags=["monitoring-alarm-rules"],
)


class AlarmRuleUpdateRequest(BaseModel):
    threshold: float
    is_active: bool


@router.get("/")
def read_alarm_rules(
    conn: connection = Depends(get_db_connection),
):
    return fetch_alarm_rules(conn)


@router.post("/{rule_id}")
def update_alarm_rule_endpoint(
    rule_id: int,
    payload: AlarmRuleUpdateRequest,
    conn: connection = Depends(get_db_connection),
):
    return update_alarm_rule(
        conn,
        rule_id=rule_id,
        threshold=payload.threshold,
        is_active=payload.is_active,
    )