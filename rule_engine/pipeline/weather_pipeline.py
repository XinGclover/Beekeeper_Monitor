from rule_engine.evaluator import is_rule_matched
from rule_engine.repository import (
    fetch_weather_data,
    fetch_weather_rules,
    insert_weather_alarm_event,
)

WEATHER_METRIC_FIELD_MAP = {
    "air_temperature": "air_temperature",
    "relative_humidity": "relative_humidity",
    "wind_speed": "wind_speed",
}


def process_weather_alarms(conn) -> None:
    rules = fetch_weather_rules(conn)
    weather_rows = fetch_weather_data(conn)

    rules_by_location: dict[int, list[dict]] = {}
    for rule in rules:
        location_id = rule["location_id"]
        rules_by_location.setdefault(location_id, []).append(rule)

    for row in weather_rows:
        weather_id = row["weather_id"]
        location_id = row["location_id"]

        matching_rules = rules_by_location.get(location_id, [])
        for rule in matching_rules:
            metric_name = rule["metric_type_name"]
            field_name = WEATHER_METRIC_FIELD_MAP.get(metric_name)

            if not field_name:
                continue

            value = row.get(field_name)
            if value is None:
                continue

            if is_rule_matched(
                float(value),
                rule["condition_type"],
                float(rule["threshold"]),
            ):
                insert_weather_alarm_event(conn, rule["rule_id"], weather_id)
                print(
                    f"WEATHER ALARM: weather_id={weather_id}, "
                    f"location_id={location_id}, "
                    f"rule={rule['name']}, "
                    f"{metric_name}={value}"
                )