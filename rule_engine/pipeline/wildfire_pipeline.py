from rule_engine.evaluator import is_rule_matched
from rule_engine.repository import (
    fetch_wildfire_data,
    fetch_wildfire_rules,
    insert_wildfire_alarm_event,
)

WILDFIRE_METRIC_FIELD_MAP = {
    "wildfire_brightness": "brightness",
    "wildfire_frp": "frp",
    "wildfire_severity": "severity_level_id",
}


def process_wildfire_alarms(conn) -> None:
    rules = fetch_wildfire_rules(conn)
    wildfire_rows = fetch_wildfire_data(conn)

    rules_by_location: dict[int, list[dict]] = {}
    for rule in rules:
        location_id = rule["location_id"]
        rules_by_location.setdefault(location_id, []).append(rule)

    for row in wildfire_rows:
        wildfire_id = row["wildfire_id"]
        location_id = row["location_id"]

        matching_rules = rules_by_location.get(location_id, [])
        for rule in matching_rules:
            metric_name = rule["metric_type_name"]
            field_name = WILDFIRE_METRIC_FIELD_MAP.get(metric_name)

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
                insert_wildfire_alarm_event(
                    conn, 
                    rule["rule_id"], 
                    wildfire_id,
                    observed_value=float(value),
                    threshold_value=float(rule["threshold"]),
                    )
                