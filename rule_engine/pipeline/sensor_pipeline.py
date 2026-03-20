from rule_engine.repository import fetch_sensor_data, fetch_sensor_rules, insert_sensor_alarm_event

from rule_engine.evaluator import is_rule_matched

SENSOR_TYPE_TO_METRIC_TYPE = {
    1: 1,  # TEMPERATURE
    2: 2,  # HUMIDITY
    3: 6,  # WEIGHT
}

def process_sensor_alarms(conn):
    sensor_rows = fetch_sensor_data(conn)
    rules = fetch_sensor_rules(conn)

    for row in sensor_rows:
        sensor_data_id = row["sensor_data_id"]
        sensor_id = row["sensor_id"]
        sensor_type_id = row["sensor_type_id"]
        measurement = row["measurement"]

        expected_metric_type_id = SENSOR_TYPE_TO_METRIC_TYPE.get(sensor_type_id)
        if expected_metric_type_id is None:
            continue

        for rule in rules:
            if rule["sensor_id"] != sensor_id:
                continue

            if rule["metric_type_id"] != expected_metric_type_id:
                continue

            if not is_rule_matched(
                measurement,
                rule["condition_type"],
                rule["threshold"]
            ):
                continue

            insert_sensor_alarm_event(
                conn=conn,
                rule_id=rule["rule_id"],
                sensor_data_id=sensor_data_id
            )          
