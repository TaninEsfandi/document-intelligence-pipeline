import ollama
from app.rag.embedder import embed_texts
from app.rag.vector_store import search_reports

def answer_question(question: str) -> str:
    # Step 1: embed the question
    embedded_question = embed_texts([question])[0]
    
    # Step 2: search ChromaDB
    results = search_reports(embedded_question)
    
    # Step 3: build prompt
    context = "\n\n".join(results["documents"][0])
    prompt = f"""You are a medical device safety assistant.
Use the following FDA adverse event reports to answer the question.

Reports:
{context}

Question: {question}

Answer:"""
    
    # Step 4: call Ollama
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Step 5: return answer
    return response.message.content

if __name__ == "__main__":
    question = input("Ask a question: ")
    print(answer_question(question))