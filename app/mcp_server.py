import os
from pathlib import Path

# Claude Desktop launches the server with cwd="/"; relative paths (chroma_db, results/, configs/) need the project root
os.chdir(Path(__file__).resolve().parent.parent)

from mcp.server.fastmcp import FastMCP
from app.rag.embedder import embed_texts
from app.rag.vector_store import search_reports
from app.connectors.fda import fetch_reports
from app.report_transformers.fda_transformers import transform_reports
from app.rag.extractor import extract_causal_chain
from app.rag.evaluator import evaluate_extraction

mcp = FastMCP("DocuLens")

@mcp.tool()
def search_documents(query: str) -> str:
    """Search the local DocuLens FDA MAUDE database using semantic search. Returns relevant report excerpts."""
    embedded = embed_texts([query])[0]
    results = search_reports(embedded)
    docs = results["documents"][0]
    return "\n\n---\n\n".join(docs)

@mcp.tool()
def retrieve_report(device_name: str) -> str:
    """Retrieve FDA adverse event reports for a specific medical device."""
    raw = fetch_reports(device_name, limit=3)
    results = transform_reports(raw)
    return str(results)

@mcp.tool()
def extract_structured_fields(text: str) -> str:
    """Extract validated causal-chain fields from a report narrative."""
    extraction = extract_causal_chain(text)
    evaluation = evaluate_extraction(text, extraction)
    return f"Extraction: {extraction.model_dump()}\nEvaluation flag: {evaluation.overall_flag}"

if __name__ == "__main__":
    mcp.run()