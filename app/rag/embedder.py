from sentence_transformers import SentenceTransformer
import json

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: list[str]) -> list:
    return model.encode(texts).tolist()

if __name__ == "__main__":
    with open("results/transformed_reports.json", "r") as f:
        data = json.load(f)
    texts = [report["text"] for report in data]
    result = embed_texts(texts)         
    print(result[0])                           
