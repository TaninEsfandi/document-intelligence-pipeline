from fastapi import FastAPI
from app.connectors.fda import fetch_reports
from app.transformers.fda_transformers import transform_reports
import uvicorn
from app.models.report import ReportOutput
from app.rag.extractor import extract_causal_chain
from app.rag.evaluator import evaluate_extraction
from app.models.extraction import CausalChainExtraction, ExtractionRequest, ExtractionResponse
from app.models.critic import CriticOutput

app = FastAPI(
    title = "Connector API",
    description= "This is DocuLens FastAPI application"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Doculens"}

@app.get("/reports")
def get_reports(device_name: str, limit: int = 10):
    reports = fetch_reports(device_name, limit)
    return reports

@app.get("/extracted_fields", response_model=list[ReportOutput])
def get_extracted_fields(device_name: str, limit: int = 10):
    raw = fetch_reports(device_name, limit)
    extracted = transform_reports(raw)
    return extracted

@app.post("/extract", response_model=ExtractionResponse)
def extract_report(request: ExtractionRequest):
    extraction = extract_causal_chain(request.report_text)
    evaluation = evaluate_extraction(request.report_text, extraction)
    return ExtractionResponse(extraction=extraction, evaluation=evaluation)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)