import ollama
import json
from pathlib import Path
from app.models.extraction import CausalChainExtraction

def extract_causal_chain(report_text: str) -> CausalChainExtraction:
    
    prompt_path = Path("configs/prompts/extraction_prompt.txt")
    system_prompt = prompt_path.read_text()
    
    user_message = f"{system_prompt}\n\nReport to analyze:\n{report_text}"
    
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": user_message}],
        format=CausalChainExtraction.model_json_schema()
    )
    return CausalChainExtraction.model_validate(json.loads(response.message.content))

if __name__ == "__main__":
    test_report = "IT WAS REPORTED THAT THE RIGHT ATRIAL (RA) LEAD EXHIBITED UNDERSENSING LEADING TO THE EARLY TERMINATION OF THE ATRIAL TACHYCARDIA/ATRIAL FIBRILLATION (AT/AF) EPISODES. THE LEAD REMAINS IN USE. NO PATIENT COMPLICATIONS HAVE BEEN REPORTED AS A RESULT OF THIS EVENT."
    result = extract_causal_chain(test_report)
    print(result)