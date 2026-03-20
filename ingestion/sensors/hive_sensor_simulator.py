import argparse
import random
import time
from datetime import datetime

from core.db import get_db_conn
from ingestion.common.jobs import create_scraping_job ,update_scraping_job_status
from ingestion.sensors.sensor_repository import fetch_sensors, insert_sensor_data


HIVE_SOURCE_ID = 3  # Hive Sensor Network i external_source


def generate_measurement(sensor_type_name: str, previous_value: float | None = None) -> float:
    """
    Genererar realistiska sensorvärden.
    Anpassa gärna intervallen efter dina alarm rules.
    """
    sensor_type = sensor_type_name.lower()

    if "temp" in sensor_type:
        base = 34.0          # 35
        noise = random.uniform(-3.0, 3.0)
        value = base + noise

    elif "humid" in sensor_type:
        base = 68.0         # 70
        noise = random.uniform(-5.0, 5.0)
        value = base + noise

    elif "weight" in sensor_type:
        if previous_value is None:
            value = random.uniform(14.0, 90.0)      # 20, 15, 80
        else:
            # vikt ändras långsamt
            value = previous_value + random.uniform(-0.2, 0.2)

    elif "co2" in sensor_type:
        base = 650.0
        noise = random.uniform(-100.0, 120.0)
        value = base + noise

    else:
        raise ValueError(f"Unknown sensor type: {sensor_type_name}")

    return round(max(value, 0), 2)




def simulate_one_batch(
    conn,
    sensors: list[dict],
    last_values: dict[int, float],
    measured_at: datetime,
) -> int:
    job_id = create_scraping_job(conn, HIVE_SOURCE_ID)
    inserted_count = 0

    try:
        for sensor in sensors:
            sensor_id = sensor["sensor_id"]
            sensor_type_name = sensor["sensor_type_name"]

            measurement = generate_measurement(
                sensor_type_name=sensor_type_name,
                previous_value=last_values.get(sensor_id),
            )

            insert_sensor_data(
                conn=conn,
                job_id=job_id,
                sensor_id=sensor_id,
                measurement=measurement,
                measured_at=measured_at,
            )

            last_values[sensor_id] = measurement
            inserted_count += 1

        update_scraping_job_status(conn, job_id, "success")
        conn.commit()
        return inserted_count

    except Exception:
        conn.rollback()
        try:
            update_scraping_job_status(conn, job_id, "failed")
            conn.commit()
        except Exception:
            conn.rollback()
        raise


def run_simulator(interval_seconds: int, hive_id: int | None = None) -> None:
    conn = get_db_conn()
    last_values: dict[int, float] = {}

    try:
        sensors = fetch_sensors(conn, hive_id=hive_id)

        if not sensors:
            print("Inga sensorer hittades i ingestion.sensor")
            return

        while True:
            measured_at = datetime.now().replace(microsecond=0)

            inserted_count = simulate_one_batch(
                conn=conn,
                sensors=sensors,
                last_values=last_values,
                measured_at=measured_at,
            )

            print(
                f"[{measured_at}] Skapade {inserted_count} sensorrader"
            )

            time.sleep(interval_seconds)

    finally:
        conn.close()


def run_once(hive_id: int | None = None) -> None:
    conn = get_db_conn()
    last_values: dict[int, float] = {}

    try:
        sensors = fetch_sensors(conn, hive_id=hive_id)

        if not sensors:
            print("Inga sensorer hittades i ingestion.sensor")
            return

        measured_at = datetime.now().replace(microsecond=0)

        inserted_count = simulate_one_batch(
            conn=conn,
            sensors=sensors,
            last_values=last_values,
            measured_at=measured_at,
        )

        print(f"[{measured_at}] Skapade {inserted_count} sensorrader")

    finally:
        conn.close()


def parse_args():
    parser = argparse.ArgumentParser(description="Hive sensor live data simulator")
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="How many seconds between two batches",
    )
    parser.add_argument(
        "--hive-id",
        type=int,
        default=None,
        help="Optional: simulate only for a specific hive_id",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Just run a batch and exit",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.once:
        run_once(hive_id=args.hive_id)
    else:
        run_simulator(
            interval_seconds=args.interval,
            hive_id=args.hive_id,
        )


if __name__ == "__main__":
    main()