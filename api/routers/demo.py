from fastapi import APIRouter, Depends
from psycopg2.extensions import connection

from api.deps import get_db_connection
from api.services.demo_service import start_demo_job, get_demo_status

router = APIRouter(prefix="/api/demo", tags=["demo"])


@router.post("/start")
async def start_demo(conn: connection = Depends(get_db_connection)):
    return await start_demo_job(conn)


@router.get("/status")
def demo_status():
    return get_demo_status()
