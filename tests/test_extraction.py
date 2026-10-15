import pytest
from pydantic import ValidationError
from app.models.extraction import CausalChainExtraction
from app.models.critic import CriticOutput

def test_causal_chain_extraction_schema():
    extraction = CausalChainExtraction(
        root_cause="Sonalert alarm wire — intermittent open circuit (inferred)",
        hazardous_situation="The ventilator failed during use without an audio alarm.",
        hazard_outcome="No confirmed hazard outcome — device under monitoring.",
        corrective_action="Device serviced and repaired.",
        traceability="partially inferred",
        domain="Built"
    )
    assert extraction.root_cause == "Sonalert alarm wire — intermittent open circuit (inferred)"
    assert extraction.domain == "Built"
    assert extraction.traceability == "partially inferred"

def test_invalid_domain_rejected():
    with pytest.raises(ValidationError):
        CausalChainExtraction(
            root_cause="test",
            hazardous_situation="test",
            hazard_outcome="test",
            corrective_action="test",
            traceability="partially inferred",
            domain="InvalidDomain"
        )

def test_critic_output_schema():
    critic = CriticOutput(
        self_validation_detected=False,
        escape_phrase_appropriate=True,
        speculative_language_detected=False,
        overall_flag="clean",
        notes="All fields grounded in report."
    )
    assert critic.overall_flag == "clean"
    assert critic.self_validation_detected == False