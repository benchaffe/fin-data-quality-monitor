import plotly.express as px
import streamlit as st

from db import query

st.set_page_config(page_title="Data Quality Monitor", layout="wide")
st.title("Financial Data Quality Monitor")

health = query(
    """SELECT h.dq_run_id, h.health_score, min(r.run_at) AS run_at
       FROM dq_health h JOIN dq_results r USING (dq_run_id)
       GROUP BY h.dq_run_id, h.health_score ORDER BY run_at"""
)

latest = health.iloc[-1]
change = round(latest.health_score - health.iloc[-2].health_score, 1) if len(health) > 1 else None
st.metric("Health score (latest run)", f"{latest.health_score:.1f}", change)

st.plotly_chart(px.line(health, x="run_at", y="health_score", markers=True, title="Health score by run"))

left, right = st.columns(2)
dims = query("SELECT dimension, round(100 * dim_score, 1) AS score FROM dq_dimension_scores WHERE dq_run_id = ?", [latest.dq_run_id])
left.plotly_chart(px.bar(dims, x="dimension", y="score", range_y=[0, 100], title="Score by dimension"))
tables = query("SELECT table_name, health_score FROM dq_table_health WHERE dq_run_id = ? ORDER BY health_score", [latest.dq_run_id])
right.dataframe(tables, hide_index=True)