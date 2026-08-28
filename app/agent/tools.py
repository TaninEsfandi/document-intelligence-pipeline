from langchain_core.tools import tool
from app.rag.retriever import answer_question
from app.rag.extractor import extract_causal_chain
from app.rag.evaluator import evaluate_extraction
from app.connectors.fda import fetch_reports
from app.report_transformers.fda_transformers import transform_reports

@tool
def search_documents(query: str) -> str:
    """Search FDA adverse event reports and answer questions using RAG."""
    return answer_question(query)

@tool
def retrieve_report(device_name: str) -> str:
    """Retrieve and structure FDA reports for a specific device."""
    raw = fetch_reports(device_name, limit=3)
    results = transform_reports(raw)
    return str(results)

@tool
def extract_structured_fields(text: str) -> dict:
    """Extract validated causal-chain fields from a report narrative."""
    extraction = extract_causal_chain(text)
    evaluation = evaluate_extraction(text, extraction)
    return {
        "extraction": extraction.model_dump(),
        "evaluation": evaluation.model_dump()
    }