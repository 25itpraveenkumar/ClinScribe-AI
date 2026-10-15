"""Fail-closed consent guard for transcript processing."""


def validate_consent(consent_given: bool) -> dict[str, object]:
    if consent_given is not True:
        return {
            "allowed": False,
            "message": "Patient consent is required before processing audio or transcripts.",
        }
    return {"allowed": True, "message": "Consent confirmed for this request."}

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
