from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from app.agent.tools import search_documents, retrieve_report, extract_structured_fields

llm = ChatOllama(model="llama3.1:8b", base_url="http://localhost:11434")
tools = [search_documents, retrieve_report, extract_structured_fields]
agent = create_react_agent(llm, tools)

def run_agent(question: str) -> dict:
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return {
        "answer": result["messages"][-1].content,
        "messages": [m.content for m in result["messages"]]
    }

if __name__ == "__main__":
    response = run_agent("What went wrong with pacemakers?")
    print(response["answer"])