from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.agent.tools import search_documents, retrieve_report, extract_structured_fields
from app.logger import get_logger

logger = get_logger(__name__)

llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
tools = [search_documents, retrieve_report, extract_structured_fields]
agent = create_react_agent(llm, tools)

def run_agent(question: str) -> dict:
    logger.info(f"Agent running: {question[:50]}")
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return {
        "answer": result["messages"][-1].content,
        "messages": [m.content for m in result["messages"]],
        "raw_messages": result["messages"]  # ← add this line
    }

if __name__ == "__main__":
    response = run_agent("What went wrong with pacemakers?")
    print(response["answer"])