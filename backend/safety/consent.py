
from dataclasses import dataclass


@dataclass
class ConsentRecord:
    consent_given: bool
    purpose: str = "clinical_documentation"


def validate_consent(consent: ConsentRecord) -> bool:
    """Allow audio processing only when explicit consent is recorded."""
    return (
        consent.consent_given is True
        and consent.purpose == "clinical_documentation"
    )
