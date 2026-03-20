import pandas as pd

def format_value(value, suffix=""):
    if pd.isna(value):
        return "N/A"
    return f"{value}{suffix}"


def get_risk_color(severity):
    if severity == 5:
        return "darkred"
    elif severity == 4:
        return "red"
    elif severity == 3:
        return "orange"
    elif severity == 2:
        return "yellow"
    elif severity == 1:
        return "green"
    return "gray"
