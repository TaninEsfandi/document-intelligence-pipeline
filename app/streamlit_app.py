import streamlit as st
from app.connectors.fda import fetch_reports
from app.transformers.fda_transformers import transform_reports
from app.rag.retriever import answer_question

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