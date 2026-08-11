from pydantic import BaseModel
from typing import Literal

class CausalChainExtraction(BaseModel):
    root_cause: str
    traceability: Literal["report-stated", "partially inferred", "primarily inferred"]
    hazardous_situation: str
    hazard_outcome: str
    corrective_action: str
    domain: Literal["Human", "Built", "Natural", "None/unclear"]