from pydantic import BaseModel
from typing import Literal

class CriticOutput(BaseModel):
    self_validation_detected: bool
    escape_phrase_appropriate: bool  
    speculative_language_detected: bool
    overall_flag: Literal["clean", "minor", "major"]
    notes: str