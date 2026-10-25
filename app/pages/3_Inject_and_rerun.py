import os
import streamlit as st
import db
from db import query
from quality.faults.faults import FAULTS, apply_fault
from quality.run_checks import run_all
from quality.scoring import apply_scoring

DEMO = os.environ.get("DQ_DEMO_DB", "warehouse/demo_faulty.duckdb")

st.title("Inject bad data and re-run")
fault = st.selectbox("Fault to inject", list(FAULTS))
st.caption("Expected to be caught by: " + ", ".join(FAULTS[fault]["expect"]))

if st.button("Inject and re-run checks"):
    apply_fault(db.DB, DEMO, fault)
    run = run_all(DEMO)
    apply_scoring(DEMO)
    after = query("SELECT check_name, rows_failed, status FROM dq_results WHERE dq_run_id = ?", [run], db=DEMO)
    score = query("SELECT health_score FROM dq_health WHERE dq_run_id = ?", [run], db=DEMO).health_score[0]
    clean = query("SELECT health_score FROM dq_health ORDER BY dq_run_id DESC LIMIT 1").health_score[0]
    a, b = st.columns(2)
    a.metric("Clean score", f"{clean:.1f}")
    b.metric("After fault", f"{score:.1f}", round(score - clean, 1))
    st.dataframe(after[after.status != "pass"], hide_index=True)