import streamlit as st
from app.connectors.fda import fetch_reports
from app.report_transformers.fda_transformers import transform_reports
from app.rag.retriever import answer_question
from app.rag.extractor import extract_causal_chain
from app.rag.evaluator import evaluate_extraction

st.title("DocuLens 🔍")
device_name = st.text_input("Search device name", placeholder="e.g. pacemaker")

if st.button("Search"):
    data = fetch_reports(device_name)
    result = transform_reports(data)
    st.dataframe(result)

st.divider()
st.subheader("Ask a Question")
question = st.text_input("Your question", placeholder="e.g. What went wrong with pacemakers?")
if st.button("Ask"):
    answer = answer_question(question)
    st.write(answer)
    
st.divider()
st.subheader("Extract Causal Chain")
report_text = st.text_area("Paste a report text", placeholder="Paste FDA adverse event narrative here...")

if st.button("Extract"):
    extraction = extract_causal_chain(report_text)
    evaluation = evaluate_extraction(report_text, extraction)
    
    st.markdown("**Extraction**")
    st.write(f"**Root Cause:** {extraction.root_cause}")
    st.write(f"**Hazardous Situation:** {extraction.hazardous_situation}")
    st.write(f"**Hazard Outcome:** {extraction.hazard_outcome}")
    st.write(f"**Corrective Action:** {extraction.corrective_action}")
    st.write(f"**Domain:** {extraction.domain}")
    st.write(f"**Traceability:** {extraction.traceability}")
    
    st.markdown("**Evaluation**")
    st.write(f"**Overall Flag:** {evaluation.overall_flag}")
    st.write(f"**Notes:** {evaluation.notes}")