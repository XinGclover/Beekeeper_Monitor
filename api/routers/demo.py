import asyncio
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from psycopg2.extensions import connection

from api.deps import get_db_connection

router = APIRouter(prefix="/api/demo", tags=["demo"])

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEMO_DURATION_SECONDS = 30 * 60
RETENTION_DAYS = 30


demo_state: dict[str, Any] = {
    "running": False,
    "started_at": None,
    "ends_at": None,
    "processes": [],
    "messages": [],
}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _format_datetime(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def _state_payload() -> dict[str, Any]:
    now = _now()
    remaining_seconds = 0

    if demo_state["running"] and demo_state["ends_at"]:
        remaining_seconds = int(max(0, (demo_state["ends_at"] - now).total_seconds()))

    return {
        "running": bool(demo_state["running"]),
        "started_at": _format_datetime(demo_state["started_at"]),
        "ends_at": _format_datetime(demo_state["ends_at"]),
        "remaining_seconds": remaining_seconds,
    }


def _cleanup_old_demo_data(conn: connection) -> None:
    statements = [
        f"DELETE FROM ingestion.notification WHERE created_at < now() - interval '{RETENTION_DAYS} days'",
        f"DELETE FROM ingestion.alarm_event WHERE triggered_at < now() - interval '{RETENTION_DAYS} days'",
        f"DELETE FROM ingestion.sensor_data WHERE measured_at < now() - interval '{RETENTION_DAYS} days'",
        f"DELETE FROM ingestion.weather_data WHERE valid_time < now() - interval '{RETENTION_DAYS} days'",
        f"DELETE FROM ingestion.wildfire_data WHERE detected_at < now() - interval '{RETENTION_DAYS} days'",
    ]

    with conn.cursor() as cursor:
        for statement in statements:
            cursor.execute(statement)
        conn.commit()


async def _execute_command(command: list[str], label: str) -> str:
    process = await asyncio.create_subprocess_exec(
        *command,
        cwd=str(PROJECT_ROOT),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        output = stderr.decode().strip() or stdout.decode().strip()
        raise RuntimeError(f"{label} command failed with exit code {process.returncode}: {output}")

    return stdout.decode().strip()


async def _spawn_background_process(command: list[str], label: str) -> asyncio.subprocess.Process:
    process = await asyncio.create_subprocess_exec(
        *command,
        cwd=str(PROJECT_ROOT),
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    demo_state["processes"].append({"label": label, "process": process})
    return process


async def _repeat_pipeline(module_path: str, interval_seconds: int, end_time: datetime) -> None:
    label = module_path.split(".")[-1]

    while _now() < end_time:
        try:
            await _execute_command([sys.executable, "-m", module_path], f"{label} pipeline")
            demo_state["messages"].append(f"{label} pipeline executed successfully.")
        except Exception as exc:
            demo_state["messages"].append(f"{label} pipeline error: {exc}")

        if _now() >= end_time:
            break

        await asyncio.sleep(interval_seconds)


async def _terminate_process(proc: asyncio.subprocess.Process, label: str) -> None:
    try:
        proc.terminate()
        await asyncio.wait_for(proc.wait(), timeout=5)
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
    except Exception as exc:
        demo_state["messages"].append(f"Failed to stop {label}: {exc}")


async def _shutdown_demo() -> None:
    processes = demo_state.get("processes", [])[:]

    for entry in processes:
        proc = entry.get("process")
        label = entry.get("label", "process")
        if proc and proc.returncode is None:
            await _terminate_process(proc, label)

    demo_state["processes"] = []
    demo_state["running"] = False
    demo_state["started_at"] = None
    demo_state["ends_at"] = None


async def _run_demo_job() -> None:
    demo_state["messages"].append("Demo job has started.")
    end_time = demo_state["ends_at"]

    try:
        await _spawn_background_process(
            [sys.executable, "-m", "ingestion.sensors.hive_sensor_simulator", "--interval", "300"],
            "sensor simulator",
        )
        await _spawn_background_process(
            [sys.executable, "-m", "core.main"],
            "rule engine",
        )

        await _execute_command([sys.executable, "-m", "ingestion.weather.pipeline"], "weather pipeline")
        await _execute_command([sys.executable, "-m", "ingestion.wildfire.pipeline"], "wildfire pipeline")

        if end_time is None:
            raise RuntimeError("Demo end time is not defined")

        weather_task = asyncio.create_task(_repeat_pipeline("ingestion.weather.pipeline", 600, end_time))
        wildfire_task = asyncio.create_task(_repeat_pipeline("ingestion.wildfire.pipeline", 600, end_time))

        await asyncio.gather(weather_task, wildfire_task)

    except Exception as exc:
        demo_state["messages"].append(f"Demo job error: {exc}")
    finally:
        await _shutdown_demo()


@router.post("/start")
async def start_demo(conn: connection = Depends(get_db_connection)) -> dict[str, Any]:
    if demo_state["running"]:
        print("🔥 DEMO START TRIGGERED")
        return {
            "running": True,
            "message": "Demo already running",
            "started_at": _format_datetime(demo_state["started_at"]),
            "ends_at": _format_datetime(demo_state["ends_at"]),
        }

    try:
        _cleanup_old_demo_data(conn)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {exc}") from exc

    started_at = _now()
    ends_at = started_at + timedelta(seconds=DEMO_DURATION_SECONDS)

    demo_state.update(
        {
            "running": True,
            "started_at": started_at,
            "ends_at": ends_at,
            "processes": [],
            "messages": ["Demo scheduled to run for 30 minutes."],
        }
    )

    asyncio.create_task(_run_demo_job())

    return {
        "running": True,
        "message": "Demo started",
        "started_at": _format_datetime(started_at),
        "ends_at": _format_datetime(ends_at),
    }


@router.get("/status")
def demo_status() -> dict[str, Any]:
    return _state_payload()
