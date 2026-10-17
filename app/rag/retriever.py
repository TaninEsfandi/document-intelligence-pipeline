import ollama
from app.rag.embedder import embed_texts
from app.rag.vector_store import search_reports
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.logger import get_logger

client = ollama.Client(host=OLLAMA_BASE_URL)
logger = get_logger(__name__)

def answer_question(question: str) -> dict:
    logger.info(f"Answering question: {question[:50]}")
    embedded_question = embed_texts([question])[0]
    results = search_reports(embedded_question)
    
    context = "\n\n".join(results["documents"][0])
    metadatas = results["metadatas"][0]
    
    prompt = f"""You are a medical device safety assistant.
Use the following FDA adverse event reports to answer the question.

Reports:
{context}

Question: {question}

Answer:"""
    
    response = client.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    
    sources = [
        {
            "report_number": m.get("report_number", "Unknown"),
            "device_name": m.get("device_name", "Unknown"),
            "event_type": m.get("event_type", "Unknown")
        }
        for m in metadatas
    ]
    
    return {
        "answer": response.message.content,
        "sources": sources
    }

if __name__ == "__main__":
    question = input("Ask a question: ")
    print(answer_question(question))