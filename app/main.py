from fastapi import FastAPI
from app.connectors.fda import fetch_reports

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)