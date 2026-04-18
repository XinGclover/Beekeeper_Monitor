import pandas as pd


def parse_datetime(value):
    if value in (None, ""):
        return None
    try:
        return pd.to_datetime(value)
    except Exception:
        return None


def format_datetime(value, fmt="%b %d, %H:%M"):
    dt = parse_datetime(value)
    return dt.strftime(fmt) if dt is not None else ""


def parse_datetime_fields(records, fields):
    for record in records:
        for field in fields:
            if field in record and record[field]:
                record[field] = parse_datetime(record[field])
    return records