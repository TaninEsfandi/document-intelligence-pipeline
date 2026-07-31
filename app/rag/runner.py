import json
from app.rag.embedder import embed_texts
from app.rag.vector_store import store_reports

def extract_texts(reports: list[dict]) -> list[str]:
    return [report.get("text") for report in reports]


if __name__ == "__main__":
    with open("./results/transformed_reports.json", "r") as f:
        data = json.load(f)
        metadatas = [
            {
            "report_number" : report.get("report_number"),
            "device_name" : report.get("device_name"),
            "event_type" : report.get("event_type"),
            "date_received" : report.get("date_received")
        }
        for report in data
        ]
        texts = extract_texts(data)
        embeddings = embed_texts(texts)
        store_reports(texts, embeddings, metadatas)