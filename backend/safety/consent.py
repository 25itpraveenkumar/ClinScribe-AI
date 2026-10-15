"""Fail-closed consent guard for transcript processing."""


def validate_consent(consent_given: bool) -> dict[str, object]:
    if consent_given is not True:
        return {
            "allowed": False,
            "message": "Patient consent is required before processing audio or transcripts.",
        }
    return {"allowed": True, "message": "Consent confirmed for this request."}
