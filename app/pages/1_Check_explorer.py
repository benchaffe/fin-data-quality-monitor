import io
import pandas as pd
import streamlit as st
from db import query
from quality.run_checks import CHECKS, parse

st.title("Check explorer")
run = query("SELECT max(dq_run_id) AS r FROM dq_results").r[0]
df = query(
    "SELECT check_name, dimension, table_name, rows_tested, rows_failed, status "
    "FROM dq_results WHERE dq_run_id = ? ORDER BY status, dimension", [run],
)
statuses = st.multiselect("Status", ["pass", "fail", "error"], default=["fail", "error"])
shown = df[df.status.isin(statuses)]
st.dataframe(shown, hide_index=True)

if not shown.empty:
    choice = st.selectbox("Inspect a check", shown.check_name)
    sql_by_name = {parse(p)[0]["name"]: parse(p)[1] for p in CHECKS.glob("*.sql")}
    st.code(sql_by_name[choice], language="sql")
    sample = query("SELECT sample_rows FROM dq_results WHERE dq_run_id = ? AND check_name = ?", [run, choice]).sample_rows[0]
    st.dataframe(pd.read_json(io.StringIO(sample)), hide_index=True)