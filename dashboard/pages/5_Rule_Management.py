import streamlit as st
import pandas as pd
from decimal import Decimal

from db import get_db_conn
from dashboard.services.rule_management_service import (
    fetch_alarm_rules,
    update_alarm_rule
)

st.set_page_config(page_title="Rule Management", layout="wide")
st.title("Rule Management")


def load_rules_df() -> pd.DataFrame:
    conn = get_db_conn()
    try:
        rows = fetch_alarm_rules(conn)
        df = pd.DataFrame(rows)
        return df
    finally:
        conn.close()


def normalize_decimal(value) -> Decimal:
    return Decimal(str(value))


def values_changed(old_row, new_row) -> bool:
    old_threshold = normalize_decimal(old_row["threshold"])
    new_threshold = normalize_decimal(new_row["threshold"])

    old_active = bool(old_row["is_active"])
    new_active = bool(new_row["is_active"])

    return old_threshold != new_threshold or old_active != new_active


df = load_rules_df()

st.caption("Edit threshold and active status directly in the table, then click Save changes.")

edited_df = st.data_editor(
    df,
    use_container_width=True,
    hide_index=True,
    num_rows="fixed",
    column_config={
        "rule_id": st.column_config.NumberColumn("Rule ID", disabled=True),
        "name": st.column_config.TextColumn("Rule Name", disabled=True),
        "metric_type_id": st.column_config.NumberColumn("Metric Type ID", disabled=True),
        "condition_type": st.column_config.TextColumn("Condition", disabled=True),
        "threshold": st.column_config.NumberColumn(
            "Threshold",
            min_value=0.0,
            step=0.1,
            format="%.2f",
        ),
        "severity_level_id": st.column_config.NumberColumn("Severity Level ID", disabled=True),
        "is_active": st.column_config.CheckboxColumn("Active"),
    },
    disabled=["rule_id", "name", "metric_type_id", "condition_type", "severity_level_id"],
)

col1, col2 = st.columns([1, 6])

with col1:
    if st.button("Save changes", use_container_width=True):
        changed_rows = []

        for i in range(len(df)):
            old_row = df.iloc[i]
            new_row = edited_df.iloc[i]

            if values_changed(old_row, new_row):
                changed_rows.append(
                    {
                        "rule_id": int(old_row["rule_id"]),
                        "threshold": normalize_decimal(new_row["threshold"]),
                        "is_active": bool(new_row["is_active"]),
                    }
                )

        if not changed_rows:
            st.info("No changes to save.")
        else:
            conn = get_db_conn()
            try:
                for row in changed_rows:
                    update_alarm_rule(
                        conn=conn,
                        rule_id=row["rule_id"],
                        threshold=row["threshold"],
                        is_active=row["is_active"],
                    )

                conn.commit()
                st.success(f"Updated {len(changed_rows)} rule(s).")
                st.rerun()

            except Exception as e:
                conn.rollback()
                st.error(f"Update failed: {e}")

            finally:
                conn.close()

with col2:
    if st.button("Refresh", use_container_width=False):
        st.rerun()