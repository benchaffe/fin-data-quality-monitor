import json
import streamlit as st
from db import query

st.title("Failure detail")
run = query("SELECT max(dq_run_id) AS r FROM dq_results").r[0]
try:
    fails = query(
        """SELECT r.check_name, r.rows_failed, e.explanation
           FROM dq_results r
           LEFT JOIN dq_explanations e ON e.dq_run_id = r.dq_run_id AND e.check_name = r.check_name
           WHERE r.dq_run_id = ? AND r.status IN ('fail', 'error')""", [run]
    )
except Exception:
    st.info("No explanations yet.")
    st.stop()

if fails.empty:
    st.success("No failing checks in the latest run.")
for _, row in fails.iterrows():
    with st.expander(f"{row.check_name}: {row.rows_failed} rows failed"):
        if row.explanation:
            e = json.loads(row.explanation)
            st.markdown(f"**Severity:** {e['severity']}")
            st.write(e["summary"])
            st.markdown(f"**Likely cause:** {e['likely_cause']}")
            st.markdown(f"**Suggested fix:** {e['suggested_fix']}")
        else:
            st.write("No explanation stored for this check yet")