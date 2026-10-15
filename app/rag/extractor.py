import ollama
import json
from pathlib import Path
from app.models.extraction import CausalChainExtraction
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.logger import get_logger

client = ollama.Client(host=OLLAMA_BASE_URL)
logger = get_logger(__name__)

def extract_causal_chain(report_text: str) -> CausalChainExtraction:
    logger.info("Starting causal chain extraction")
    
    prompt_path = Path("configs/prompts/extraction_prompt.txt")
    system_prompt = prompt_path.read_text()
    
    user_message = f"{system_prompt}\n\nReport to analyze:\n{report_text}"
    
    response = client.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": user_message}],
        format=CausalChainExtraction.model_json_schema()
    )
    logger.info("Extraction complete")
    return CausalChainExtraction.model_validate(json.loads(response.message.content))

if __name__ == "__main__":
    test_report = "IT WAS REPORTED THAT THE RIGHT ATRIAL (RA) LEAD EXHIBITED UNDERSENSING LEADING TO THE EARLY TERMINATION OF THE ATRIAL TACHYCARDIA/ATRIAL FIBRILLATION (AT/AF) EPISODES. THE LEAD REMAINS IN USE. NO PATIENT COMPLICATIONS HAVE BEEN REPORTED AS A RESULT OF THIS EVENT."
    result = extract_causal_chain(test_report)
    print(result)