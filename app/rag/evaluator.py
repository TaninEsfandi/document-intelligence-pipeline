import ollama
import json
from app.models.extraction import CausalChainExtraction
from app.models.critic import CriticOutput
from app.rag.extractor import extract_causal_chain
from pathlib import Path

def evaluate_extraction(report_text: str, extraction: CausalChainExtraction) -> CriticOutput:
    prompt_path = Path("configs/prompts/critic_prompt.txt")
    system_prompt = prompt_path.read_text()

    user_message = f"{system_prompt}\n\nThe Extracted field to evaluate against the report text:\n{extraction}\n{report_text}"
    
    response = ollama.chat(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": user_message}],
        format=CriticOutput.model_json_schema()
    )
    return CriticOutput.model_validate(json.loads(response.message.content))

if __name__ == "__main__":
    test_report = "IT WAS REPORTED THAT THE RIGHT ATRIAL (RA) LEAD EXHIBITED UNDERSENSING LEADING TO THE EARLY TERMINATION OF THE ATRIAL TACHYCARDIA/ATRIAL FIBRILLATION (AT/AF) EPISODES. THE LEAD REMAINS IN USE. NO PATIENT COMPLICATIONS HAVE BEEN REPORTED AS A RESULT OF THIS EVENT."
    extracted_fields = extract_causal_chain(test_report)
    result = evaluate_extraction(test_report, extracted_fields)
    print("\n=== EXTRACTION ===")
    print(f"Root Cause:          {extracted_fields.root_cause}")
    print(f"Hazardous Situation: {extracted_fields.hazardous_situation}")
    print(f"Hazard Outcome:      {extracted_fields.hazard_outcome}")
    print(f"Corrective Action:   {extracted_fields.corrective_action}")
    print(f"Domain:              {extracted_fields.domain}")
    print(f"Traceability:        {extracted_fields.traceability}")

    print("\n=== EVALUATION ===")
    print(f"Overall Flag:              {result.overall_flag}")
    print(f"Self-validation detected:  {result.self_validation_detected}")
    print(f"Speculative language:      {result.speculative_language_detected}")
    print(f"Escape phrase appropriate: {result.escape_phrase_appropriate}")
    print(f"Notes:                     {result.notes}")