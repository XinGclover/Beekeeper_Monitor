"""
Demo runner for Beekeeper Monitor - Cloud Compatible

This module implements a controlled 30-minute demo that:
- Cleans up data older than RETENTION_DAYS (30 days)
- Runs sensor simulator, rule engine, and data pipelines
- Logs all activity for cloud debugging (Render, etc.)

Environment Requirements (from Render):
- DATABASE_URL: PostgreSQL connection (Neon)
- FIRMS_API_KEY: For wildfire data ingestion

Subprocess Design:
- Uses sys.executable -m <module> (not uv run or hardcoded python)
- Uses asyncio.create_subprocess_exec (not shell=True)
- All modules runnable from PROJECT_ROOT
- Captures stderr for error reporting
- Logs startup/shutdown events

Modules invoked:
- ingestion.sensors.hive_sensor_simulator
- ingestion.weather.pipeline
- ingestion.wildfire.pipeline
- core.main (rule engine)

All require __init__.py in parent directories ✓
"""

import asyncio
import logging
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from fastapi import HTTPException
from psycopg2.extensions import connection
import os
import json

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEMO_DURATION_SECONDS = 30 * 60
RETENTION_DAYS = 30
DEMO_STATE_FILE = PROJECT_ROOT / ".demo_state.json"

demo_state: dict[str, Any] = {
    "running": False,
    "started_at": None,
    "ends_at": None,
    "processes": [],
    "messages": [],
}

def _write_demo_state_file(started_at: datetime, ends_at: datetime) -> None:
    DEMO_STATE_FILE.write_text(
        json.dumps(
            {
                "started_at": started_at.isoformat(),
                "ends_at": ends_at.isoformat(),
                "pids": [
                    entry["process"].pid
                    for entry in demo_state.get("processes", [])
                    if entry.get("process") is not None
                ],
            }
        )
    )


def _read_demo_state_file() -> dict[str, Any] | None:
    if not DEMO_STATE_FILE.exists():
        return None

    try:
        return json.loads(DEMO_STATE_FILE.read_text())
    except Exception:
        DEMO_STATE_FILE.unlink(missing_ok=True)
        return None


def _pid_is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _remove_demo_state_file() -> None:
    DEMO_STATE_FILE.unlink(missing_ok=True)

def _now() -> datetime:
    return datetime.now(timezone.utc)


def _format_datetime(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def _state_payload() -> dict[str, Any]:
    now = _now()
    remaining_seconds = 0

    if demo_state["running"] and demo_state["ends_at"]:
        remaining_seconds = int(
            max(0, (demo_state["ends_at"] - now).total_seconds())
        )

    return {
        "running": bool(demo_state["running"]),
        "started_at": _format_datetime(demo_state["started_at"]),
        "ends_at": _format_datetime(demo_state["ends_at"]),
        "remaining_seconds": remaining_seconds,
    }


def _cleanup_old_demo_data(conn: connection) -> None:
    statements = [
        f"""
        DELETE FROM ingestion.notification
        WHERE created_at < now() - interval '{RETENTION_DAYS} days'
        """,
        f"""
        DELETE FROM ingestion.alarm_event
        WHERE triggered_at < now() - interval '{RETENTION_DAYS} days'
        """,
        f"""
        DELETE FROM ingestion.sensor_data
        WHERE measured_at < now() - interval '{RETENTION_DAYS} days'
        """,
        f"""
        DELETE FROM ingestion.weather_data
        WHERE valid_time < now() - interval '{RETENTION_DAYS} days'
        """,
        f"""
        DELETE FROM ingestion.wildfire_data
        WHERE detected_at < now() - interval '{RETENTION_DAYS} days'
        """,
    ]

    with conn.cursor() as cursor:
        for statement in statements:
            cursor.execute(statement)
        conn.commit()


async def _execute_command(command: list[str], label: str) -> str:
    logger.info("Executing %s: %s", label, " ".join(command))

    process = await asyncio.create_subprocess_exec(
        *command,
        cwd=str(PROJECT_ROOT),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        error_output = stderr.decode().strip() or stdout.decode().strip()
        logger.error("%s failed: %s", label, error_output)
        demo_state["messages"].append(f"❌ {label} failed: {error_output[:200]}")
        raise RuntimeError(
            f"{label} failed with exit code {process.returncode}: {error_output}"
        )

    logger.info("%s completed successfully", label)
    return stdout.decode().strip()


async def _spawn_background_process(
    command: list[str],
    label: str,
) -> asyncio.subprocess.Process:
    logger.info("Starting %s: %s", label, " ".join(command))

    process = await asyncio.create_subprocess_exec(
        *command,
        cwd=str(PROJECT_ROOT),
        stdout=asyncio.subprocess.DEVNULL,
        stderr=None,
    )

    demo_state["processes"].append({"label": label, "process": process})
    demo_state["messages"].append(f"✅ Started {label}")

    if demo_state.get("started_at") and demo_state.get("ends_at"):
        _write_demo_state_file(demo_state["started_at"], demo_state["ends_at"])

    return process


async def _repeat_pipeline(
    module_path: str,
    interval_seconds: int,
    end_time: datetime,
) -> None:
    label = module_path.split(".")[-1]
    iteration = 0

    while _now() < end_time:
        iteration += 1

        try:
            await _execute_command(
                [sys.executable, "-m", module_path],
                f"{label} pipeline",
            )
            demo_state["messages"].append(
                f"✅ {label} pipeline executed #{iteration}"
            )
        except Exception as exc:
            logger.error("%s pipeline error: %s", label, exc, exc_info=True)
            demo_state["messages"].append(
                f"⚠️ {label} pipeline error: {str(exc)[:200]}"
            )

        if _now() >= end_time:
            break

        await asyncio.sleep(interval_seconds)


async def _terminate_process(
    proc: asyncio.subprocess.Process,
    label: str,
) -> None:
    try:
        logger.info("Terminating %s", label)
        proc.terminate()
        await asyncio.wait_for(proc.wait(), timeout=5)
    except asyncio.TimeoutError:
        logger.warning("%s did not terminate, killing", label)
        proc.kill()
        await proc.wait()
    except Exception as exc:
        logger.error("Failed to stop %s: %s", label, exc)
        demo_state["messages"].append(f"⚠️ Failed to stop {label}: {exc}")


async def _shutdown_demo() -> None:
    logger.info("Shutting down demo")

    for entry in demo_state.get("processes", [])[:]:
        proc = entry.get("process")
        label = entry.get("label", "process")

        if proc and proc.returncode is None:
            await _terminate_process(proc, label)

    demo_state["processes"] = []
    demo_state["running"] = False
    demo_state["started_at"] = None
    demo_state["ends_at"] = None
    _remove_demo_state_file()


async def _run_demo_job() -> None:
    logger.info("Demo job started")

    end_time = demo_state["ends_at"]

    try:
        if end_time is None:
            raise RuntimeError("Demo end time is not defined")

        await _spawn_background_process(
            [
                sys.executable,
                "-m",
                "ingestion.sensors.hive_sensor_simulator",
                "--interval",
                "300",
            ],
            "sensor simulator",
        )

        await _spawn_background_process(
            [
                sys.executable,
                "-m",
                "core.main",
            ],
            "rule engine",
        )

        await _execute_command(
            [sys.executable, "-m", "ingestion.weather.pipeline"],
            "weather pipeline",
        )

        await _execute_command(
            [sys.executable, "-m", "ingestion.wildfire.pipeline"],
            "wildfire pipeline",
        )

        weather_task = asyncio.create_task(
            _repeat_pipeline("ingestion.weather.pipeline", 600, end_time)
        )

        wildfire_task = asyncio.create_task(
            _repeat_pipeline("ingestion.wildfire.pipeline", 600, end_time)
        )

        await asyncio.gather(weather_task, wildfire_task)

        demo_state["messages"].append("✅ Demo completed")

    except Exception as exc:
        logger.error("Demo job error: %s", exc, exc_info=True)
        demo_state["messages"].append(f"❌ Demo job error: {exc}")
    finally:
        await _shutdown_demo()


async def start_demo_job(conn: connection) -> dict[str, Any]:
    logger.info("Demo start request received")

    if demo_state["running"]:
        return {
            "running": True,
            "message": "Demo already running",
            "started_at": _format_datetime(demo_state["started_at"]),
            "ends_at": _format_datetime(demo_state["ends_at"]),
        }

    try:
        _cleanup_old_demo_data(conn)
    except Exception as exc:
        logger.error("Cleanup failed: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Cleanup failed: {exc}",
        ) from exc

    started_at = _now()
    ends_at = started_at + timedelta(seconds=DEMO_DURATION_SECONDS)

    demo_state.update(
        {
            "running": True,
            "started_at": started_at,
            "ends_at": ends_at,
            "processes": [],
            "messages": [
                f"🚀 Demo scheduled for 30 minutes "
                f"({RETENTION_DAYS}-day retention)"
            ],
        }
    )
    _write_demo_state_file(started_at, ends_at)
    asyncio.create_task(_run_demo_job())

    return {
        "running": True,
        "message": "Demo started",
        "started_at": _format_datetime(started_at),
        "ends_at": _format_datetime(ends_at),
    }


def get_demo_status() -> dict[str, Any]:
    payload = _state_payload()

    if payload["running"]:
        return payload

    saved_state = _read_demo_state_file()
    if not saved_state:
        return payload

    try:
        started_at = datetime.fromisoformat(saved_state["started_at"])
        ends_at = datetime.fromisoformat(saved_state["ends_at"])
        pids = saved_state.get("pids", [])

        now = _now()
        still_in_time = now < ends_at
        has_running_process = any(_pid_is_running(int(pid)) for pid in pids)

        if still_in_time and not pids:
            remaining_seconds = int((ends_at - now).total_seconds())
            return {
                "running": True,
                "started_at": started_at.isoformat(),
                "ends_at": ends_at.isoformat(),
                "remaining_seconds": remaining_seconds,
            }

        if still_in_time and has_running_process:
            remaining_seconds = int((ends_at - now).total_seconds())
            return {
                "running": True,
                "started_at": started_at.isoformat(),
                "ends_at": ends_at.isoformat(),
                "remaining_seconds": remaining_seconds,
            }

        _remove_demo_state_file()
        return payload

    except Exception:
        _remove_demo_state_file()
        return payload