import pandas as pd


SENSOR_UNITS = {
    "temperature": "°C",
    "humidity": "%",
    "weight": "kg",
}


def _normalize_sensor_type(value: str | None) -> str:
    if not value:
        return ""
    return value.strip().lower()


def _safe_round(value, digits: int = 1):
    if value is None:
        return None
    if pd.isna(value):
        return None
    return round(float(value), digits)


def _build_metric_kpi(series: pd.Series, label: str, unit: str = "") -> dict:
    if series.empty:
        return {
            "label": label,
            "value": None,
            "unit": unit,
        }

    return {
        "label": label,
        "value": _safe_round(series.mean()),
        "unit": unit,
    }


def build_sensor_kpis(
    df_timeline: pd.DataFrame,
    df_latest: pd.DataFrame,
) -> dict:
    """
    Build KPI dictionary for sensor overview section.

    Expected timeline columns:
    - sensor_type_name
    - measurement
    - measured_at (optional for KPI)
    - sensor_id (optional)

    Expected latest columns:
    - sensor_id
    - measurement
    """

    empty_result = {
        "avg_temperature": {"label": "AVG TEMPERATURE", "value": None, "unit": "°C"},
        "avg_humidity": {"label": "AVG HUMIDITY", "value": None, "unit": "%"},
        "min_measurement": {"label": "MIN VALUE", "value": None, "unit": ""},
        "max_measurement": {"label": "MAX VALUE", "value": None, "unit": ""},
        "sensor_count": {"label": "SENSORS", "value": 0, "unit": ""},
    }

    if df_timeline is None or df_timeline.empty:
        if df_latest is not None and not df_latest.empty:
            empty_result["sensor_count"]["value"] = int(df_latest["sensor_id"].nunique())
        return empty_result

    df = df_timeline.copy()

    if "measurement" in df.columns:
        df["measurement"] = pd.to_numeric(df["measurement"], errors="coerce")

    if "sensor_type_name" in df.columns:
        df["sensor_type_normalized"] = df["sensor_type_name"].apply(_normalize_sensor_type)
    else:
        df["sensor_type_normalized"] = ""

    temp_df = df[df["sensor_type_normalized"] == "temperature"]
    humidity_df = df[df["sensor_type_normalized"] == "humidity"]

    result = {
        "avg_temperature": _build_metric_kpi(
            temp_df["measurement"],
            label="AVG TEMPERATURE",
            unit="°C",
        ),
        "avg_humidity": _build_metric_kpi(
            humidity_df["measurement"],
            label="AVG HUMIDITY",
            unit="%",
        ),
        "min_measurement": {
            "label": "MIN VALUE",
            "value": _safe_round(df["measurement"].min()),
            "unit": "",
        },
        "max_measurement": {
            "label": "MAX VALUE",
            "value": _safe_round(df["measurement"].max()),
            "unit": "",
        },
        "sensor_count": {
            "label": "SENSORS",
            "value": int(df_latest["sensor_id"].nunique()) if df_latest is not None and not df_latest.empty else 0,
            "unit": "",
        },
    }

    return result