from rule_engine.repository import fetch_sensor_data, fetch_sensor_rules, insert_sensor_alarm_event

from rule_engine.evaluator import is_rule_matched


def process_sensor_alarms(conn):
    rules = fetch_sensor_rules(conn)
    rows = fetch_sensor_data(conn)

    rules_by_sensor = {}
    for rule in rules:
        sensor_id = rule["sensor_id"]
        rules_by_sensor.setdefault(sensor_id, []).append(rule)

    for row in rows:
        sensor_id = row["sensor_id"]
        measurement = float(row["measurement"])
        sensor_data_id = row["sensor_data_id"]

        for rule in rules_by_sensor.get(sensor_id, []):
            if is_rule_matched(measurement, rule["condition_type"], float(rule["threshold"])):
                insert_sensor_alarm_event(conn, rule["rule_id"], sensor_data_id)


