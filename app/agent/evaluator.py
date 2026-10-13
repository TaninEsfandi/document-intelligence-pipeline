import time
import json
from app.agent.graph import run_agent

TEST_CASES = [
    ("What went wrong with pacemakers?", "search_documents"),
    ("Find reports for insulin pump", "retrieve_report"),
    ("Extract the causal chain from: The lead exhibited undersensing leading to AT/AF termination.", "extract_structured_fields"),
    ("What malfunctions have been reported for defibrillators?", "search_documents"),
    ("Show me reports for ventilator devices", "retrieve_report"),
]

def get_tool_called(messages: list) -> str:
    for msg in messages:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            return msg.tool_calls[0]["name"]
        if hasattr(msg, "name") and msg.name:
            return msg.name
    return "unknown"

def evaluate_agent(question: str, expected_tool: str) -> dict:
    start = time.time()
    result = run_agent(question)
    latency = round(time.time() - start, 2)

    raw_messages = result.get("raw_messages", [])
    tool_used = get_tool_called(raw_messages)
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

def run_evaluation():
    results = []
    for question, expected_tool in TEST_CASES:
        print(f"\nRunning: {question[:50]}...")
        result = evaluate_agent(question, expected_tool)
        results.append(result)
        print(f"Expected: {result['expected_tool']} | Got: {result['tool_used']} | Correct: {result['correct_tool_selection']}")
        print(f"Grounded: {result['grounded']} | Latency: {result['latency_seconds']}s")

    correct = sum(1 for r in results if r["correct_tool_selection"])
    grounded = sum(1 for r in results if r["grounded"])
    avg_latency = round(sum(r["latency_seconds"] for r in results) / len(results), 2)

    print(f"\n=== EVALUATION SUMMARY ===")
    print(f"Tool selection accuracy: {correct}/{len(results)} ({round(correct/len(results)*100)}%)")
    print(f"Groundedness: {grounded}/{len(results)} ({round(grounded/len(results)*100)}%)")
    print(f"Average latency: {avg_latency}s")

    with open("results/agent_eval.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to results/agent_eval.json")

if __name__ == "__main__":
    run_evaluation()