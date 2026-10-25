import streamlit as st
st.title("Lineage")
st.image("docs/lineage.png", caption="dbt lineage: raw_facts to stg_facts to the star schema")
st.markdown(
    "EDGAR company facts JSON → `raw_facts` → `stg_facts` → `dim_company`, `dim_metric`, `fact_financials` "
    "→ 20 SQL checks → `dq_results` → health score and LLM explanations."
)