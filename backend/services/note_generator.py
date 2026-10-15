"""Conservative, auditable SOAP draft generation.

This baseline intentionally avoids clinical inference. The supplied transcript
is preserved in Subjective; other sections clearly state when evidence is
missing. Replace/extend only with clinically validated extraction and evaluation.
"""
from __future__ import annotations
from backend.schemas.clinical_note import SOAPNote
from backend.services.transcription import normalize_transcript


def generate_soap_note(transcript: str) -> dict[str, object]:
    clean_transcript = normalize_transcript(transcript)
    note = SOAPNote(
        subjective=f"Patient/caller statement (verbatim source transcript): {clean_transcript}",
        objective="No objective examination findings were supplied in the transcript. Do not infer vital signs or examination results.",
        assessment="Not generated. A qualified clinician must assess the available history and clinical context.",
        plan="Not generated. A qualified clinician must determine and document the plan.",
        limitations=[
            "This is an unverified draft, not medical advice or a final medical record.",
            "No diagnosis, medication, procedure, or treatment recommendation was inferred.",
            "Clinician review and explicit approval are required before clinical use.",
        ],
    )
    return {
        "status": "success",
        "message": "Conservative SOAP draft generated. Clinician review is required.",
        "draft_note": note,
        "clinician_approval_required": True,
    }
