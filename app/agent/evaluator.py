import time
from app.agent.graph import run_agent

TOOL_KEYWORDS = {
    "search_documents": ["what", "why", "how", "went wrong", "explain"],
    "retrieve_report": ["report", "device", "find reports", "show me"],
    "extract_structured_fields": ["extract", "causal chain", "root cause", "structure"]
}

def evaluate_agent(question: str, expected_tool: str) -> dict:
    start = time.time()
    result = run_agent(question)
    latency = round(time.time() - start, 2)
    
    messages = result["messages"]
    tool_used = "unknown"
    for msg in messages:
        for tool, keywords in TOOL_KEYWORDS.items():
            if any(k in msg.lower() for k in keywords):
                tool_used = tool
                break
    
    correct_tool = tool_used == expected_tool
    answer = result["answer"]
    grounded = len(answer) > 50 and "unknown" not in answer.lower()
    
    return {
        "question": question,
        "expected_tool": expected_tool,
        "tool_used": tool_used,
        "correct_tool_selection": correct_tool,
        "grounded": grounded,
        "latency_seconds": latency,
        "answer_preview": answer[:200]
    }

if __name__ == "__main__":
    test_cases = [
        ("What went wrong with pacemakers?", "search_documents"),
        ("Find reports for insulin pump", "retrieve_report"),
        ("Extract the causal chain from: The lead exhibited undersensing leading to AT/AF termination.", "extract_structured_fields"),
    ]
    
    for question, expected_tool in test_cases:
        result = evaluate_agent(question, expected_tool)
        print(f"\nQ: {result['question']}")
        print(f"Expected: {result['expected_tool']} | Got: {result['tool_used']} | Correct: {result['correct_tool_selection']}")
        print(f"Grounded: {result['grounded']} | Latency: {result['latency_seconds']}s")